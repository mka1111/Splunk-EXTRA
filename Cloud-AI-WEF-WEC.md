1786283727175_image.png
Here's the full WEC-side (collector, WEC-Marcin, 192.168.222.142) setup to pair with the WEF config from the last message — workgroup, no domain, certificate-based auth.

Prerequisite check — you should already have from earlier steps:

powershell
Get-ChildItem Cert:\LocalMachine\Root | Where-Object {$_.Subject -like "*Homelab Root CA*"}
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -like "*WEC-Marcin*"}
winrm enumerate winrm/config/Listener
Confirm the HTTPS listener is present and bound to the WEC-Marcin cert (Server Auth EKU). If not, re-run:

powershell
$wecCert = Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -like "*WEC-Marcin*"}
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address IP:192.168.222.142 -Hostname "WEC-Marcin" -CertificateThumbPrint $wecCert.Thumbprint -Force
Step 1 — Enable and configure the Windows Event Collector service

powershell
wecutil qc /q
Step 2 — Create a local user account to represent the WEF machine's identity

Since there's no domain, cert-mapped connections need a local account to authenticate as:

powershell
$pwd = ConvertTo-SecureString "P@ssw0rd!ComplexEnough123" -AsPlainText -Force
New-LocalUser -Name "WEF-Marcin" -Password $pwd -PasswordNeverExpires -Description "Mapped identity for WEF-Marcin cert auth"
Add-LocalGroupMember -Group "Event Log Readers" -Member "WEF-Marcin"
(Event Log Readers on the source is normally what needs rights to read logs — on the collector side this local account instead needs rights to submit events, which by default any authenticated connection with a valid cert mapping can do once certmapping is configured. If you hit access-denied later, also add it to local Administrators temporarily to isolate whether it's a permissions issue.)

Step 3 — Enable WinRM certificate authentication on the service side

powershell
winrm set winrm/config/service/auth '@{Certificate="true"}'
Step 4 — Create the certificate-to-user mapping

This tells WinRM: "a client presenting a cert issued by Homelab Root CA with Subject=WEF-Marcin should be treated as the local WEF-Marcin account."

powershell
$rootThumb = (Get-ChildItem Cert:\LocalMachine\Root | Where-Object {$_.Subject -like "*Homelab Root CA*"}).Thumbprint

winrm create winrm/config/service/certmapping?Issuer=$rootThumb+Subject=WEF-Marcin+URI=* `
  '@{UserName="WEF-Marcin";Password="P@ssw0rd!ComplexEnough123"}'
Verify it registered:

powershell
winrm enumerate winrm/config/service/certmapping
Step 5 — Create the source-initiated subscription (if not already created via GUI)

Via GUI (Event Viewer → Subscriptions → Create Subscription):

Subscription type: Source Initiated
Destination log: Forwarded Events
Select Computer Groups → add the source computer or a group containing it
Advanced → select the correct Certification Authority (the "Certification Authorities" picker you screenshotted earlier — pick Homelab Root CA, not the Microsoft/DigiCert ones)
Or via CLI with an XML definition — let me know if you'd rather script it and I'll give you the full subscription XML.

Step 6 — Firewall

powershell
New-NetFirewallRule -DisplayName "WinRM HTTPS In" -Direction Inbound -Protocol TCP -LocalPort 5986 -Action Allow
Step 7 — Restart services

powershell
Restart-Service WinRM
Restart-Service Wecsvc
Step 8 — Retry the subscription and watch the log

cmd
wecutil rs aaaaa
Then check:

Event Viewer → Applications and Services → Microsoft → Windows → EventCollector → Operational
One thing worth flagging honestly: getting workgroup source-initiated + certificate auth fully correct (cert mapping, EKUs, subscription manager URL, hostname resolution all lining up simultaneously across two machines) is one of the fussier WEF/WEC configs — if you keep hitting auth errors after this, it's often faster to fall back to collector-initiated (pull) subscriptions with Basic/local-account auth over HTTPS instead of source-initiated cert auth, since it removes the cert-mapping variable entirely. Want that alternative as a fallback path in case Step 4/5 gives you grief?

give me all commands to crate certificats and hot to import to specif host

WEC 
 WEC-Marcin 192.168.222.142
------
WEF

WEF-Marcin ip 192.168.222.144
Here's the complete, consolidated set — create everything on WEC-Marcin (acting as your mini-CA), then import the right pieces on each host.

PART 1 — Run on WEC-Marcin (192.168.222.142): Create all 3 certificates
powershell
# Create export folder
New-Item -Path "C:\shareMarcin\certs" -ItemType Directory -Force

# --- 1. Create Root CA ---
$rootCA = New-SelfSignedCertificate `
    -Type Custom `
    -KeyUsage CertSign,CRLSign,DigitalSignature `
    -Subject "CN=Homelab Root CA" `
    -KeyExportPolicy Exportable `
    -NotAfter (Get-Date).AddYears(10) `
    -CertStoreLocation Cert:\LocalMachine\My `
    -TextExtension @("2.5.29.19={text}CA=true")

Write-Host "Root CA thumbprint: $($rootCA.Thumbprint)"

# --- 2. Create WEC server certificate (Server Authentication EKU), signed by Root CA ---
$wecCert = New-SelfSignedCertificate `
    -Type Custom `
    -Subject "CN=WEC-Marcin" `
    -DnsName "WEC-Marcin","192.168.222.142" `
    -KeyUsage DigitalSignature,KeyEncipherment `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1") `
    -Signer $rootCA `
    -CertStoreLocation Cert:\LocalMachine\My `
    -NotAfter (Get-Date).AddYears(5)

Write-Host "WEC cert thumbprint: $($wecCert.Thumbprint)"

# --- 3. Create WEF client certificate (Client Authentication EKU), signed by Root CA ---
$wefCert = New-SelfSignedCertificate `
    -Type Custom `
    -Subject "CN=WEF-Marcin" `
    -DnsName "WEF-Marcin","192.168.222.144" `
    -KeyUsage DigitalSignature,KeyEncipherment `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2") `
    -Signer $rootCA `
    -CertStoreLocation Cert:\LocalMachine\My `
    -NotAfter (Get-Date).AddYears(5)

Write-Host "WEF cert thumbprint: $($wefCert.Thumbprint)"

# --- 4. Export Root CA public cert (no private key needed anywhere but here) ---
Export-Certificate -Cert "Cert:\LocalMachine\My\$($rootCA.Thumbprint)" `
    -FilePath "C:\shareMarcin\certs\RootCA.cer"

# --- 5. Export WEF cert WITH private key (.pfx) — this needs to travel to WEF-Marcin ---
$pfxPwd = ConvertTo-SecureString -String "TempP@ss123!" -AsPlainText -Force
Export-PfxCertificate -Cert "Cert:\LocalMachine\My\$($wefCert.Thumbprint)" `
    -FilePath "C:\shareMarcin\certs\WEF-Marcin.pfx" -Password $pfxPwd

Write-Host "Done. Files in C:\shareMarcin\certs :"
Get-ChildItem C:\shareMarcin\certs
Note: the WEC cert ($wecCert) stays in LocalMachine\My on this machine already — no export/import needed for it, it's used locally for the listener.

PART 2 — Run on WEC-Marcin: trust the Root CA locally
powershell
Import-Certificate -FilePath "C:\shareMarcin\certs\RootCA.cer" -CertStoreLocation Cert:\LocalMachine\Root
PART 3 — Copy these 2 files to WEF-Marcin (192.168.222.144)
C:\shareMarcin\certs\RootCA.cer
C:\shareMarcin\certs\WEF-Marcin.pfx
(via network share, USB, Copy-Item over an existing PS session, whatever's available)

PART 4 — Run on WEF-Marcin (192.168.222.144): import both
powershell
# Trust the Root CA
Import-Certificate -FilePath "C:\path\to\RootCA.cer" -CertStoreLocation Cert:\LocalMachine\Root

# Import the WEF client cert (with private key)
$pfxPwd = ConvertTo-SecureString -String "TempP@ss123!" -AsPlainText -Force
Import-PfxCertificate -FilePath "C:\path\to\WEF-Marcin.pfx" `
    -CertStoreLocation Cert:\LocalMachine\My -Password $pfxPwd

# Verify
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -like "*WEF-Marcin*"} | Format-List Subject, Thumbprint, HasPrivateKey
Confirm HasPrivateKey = True.

PART 5 — Back on WEC-Marcin: bind the listener to the WEC cert
powershell
$wecCert = Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -like "*WEC-Marcin*"}
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address IP:192.168.222.142 `
    -Hostname "WEC-Marcin" -CertificateThumbPrint $wecCert.Thumbprint -Force

winrm enumerate winrm/config/Listener
At this point both machines have the trust chain and correct EKUs in place. Next step is the WinRM/WEF-WEC service config (certmapping, SubscriptionManager URL, subscription creation) I gave you in the two previous messages — those apply on top of this cert foundation. Want me to re-paste the full combined WEF + WEC service-config script now that certs are sorted, so you have one clean end-to-end run?

