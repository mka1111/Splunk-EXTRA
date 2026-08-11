Windows Event Forwarding over HTTPS (Workgroup / Non-Domain, Certificate Auth)

Topology

WEF-Marcin (192.168.222.144) — source (forwards logs) — Workgroup A
WEC-Marcin (192.168.222.142) — collector (receives logs) — Workgroup B

Since there's no domain, authentication is certificate-based instead of Kerberos:

A self-issued Root CA signs a server certificate (installed on the collector, used for the TLS/HTTPS listener) and a client certificate (installed on the source, used to authenticate the push).
The collector maps the client certificate to a local user account.

All commands are PowerShell run elevated (as Administrator) unless noted otherwise.

Phase 1 — Create the CA and certificates

Run on: WEC-Marcin (simplest — collector holds the CA; you'll export the client cert to WEF-Marcin afterward)

1.1 Create the Root CA
powershell
$rootCA = New-SelfSignedCertificate `
  -Type Custom `
  -Subject "CN=Marcin-Lab-RootCA" `
  -KeyUsage CertSign,CRLSign,DigitalSignature `
  -KeyExportPolicy Exportable `
  -KeyLength 2048 -HashAlgorithm SHA256 `
  -NotAfter (Get-Date).AddYears(10) `
  -CertStoreLocation Cert:\LocalMachine\My `
  -TextExtension @("2.5.29.19={text}CA=1")

$rootCA.Thumbprint

Note the thumbprint — you'll need it repeatedly. Store it in a variable for this session ($rootCA already holds it).

1.2 Export the Root CA public certificate (no private key)
powershell
Export-Certificate -Cert $rootCA -FilePath C:\Certs\RootCA.cer

(Create C:\Certs first if needed: New-Item -ItemType Directory C:\Certs)

1.3 Create the Server certificate (for WEC-Marcin's HTTPS listener)
powershell
$serverCert = New-SelfSignedCertificate `
  -Type Custom `
  -Subject "CN=WEC-Marcin" `
  -DnsName "WEC-Marcin","192.168.222.142" `
  -KeyExportPolicy Exportable `
  -KeyLength 2048 -HashAlgorithm SHA256 `
  -NotAfter (Get-Date).AddYears(5) `
  -CertStoreLocation Cert:\LocalMachine\My `
  -Signer $rootCA `
  -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1")   # Server Authentication EKU

$serverCert.Thumbprint
1.4 Create the Client certificate (for WEF-Marcin)
powershell
$clientCert = New-SelfSignedCertificate `
  -Type Custom `
  -Subject "CN=WEF-Marcin" `
  -KeyExportPolicy Exportable `
  -KeyLength 2048 -HashAlgorithm SHA256 `
  -NotAfter (Get-Date).AddYears(5) `
  -CertStoreLocation Cert:\LocalMachine\My `
  -Signer $rootCA `
  -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2")   # Client Authentication EKU

$clientCert.Thumbprint
1.5 Export the client cert (with private key) to move to WEF-Marcin
powershell
$pwd = ConvertTo-SecureString -String "TempP@ssw0rd!" -Force -AsPlainText
Export-PfxCertificate -Cert $clientCert -FilePath C:\Certs\WEF-Marcin-client.pfx -Password $pwd

Copy C:\Certs\RootCA.cer and C:\Certs\WEF-Marcin-client.pfx to WEF-Marcin (USB, SMB share, etc — pick whatever transfer method is available between the two workgroups).

Optional cleanup on WEC-Marcin — once copied, you can remove the client cert's private key from WEC-Marcin's store (keep only Root CA + Server cert there):

powershell
Remove-Item "Cert:\LocalMachine\My\$($clientCert.Thumbprint)"
Phase 2 — Install certificates
2.1 On WEC-Marcin

Import the Root CA into Trusted Root (server already has its own server cert from Phase 1):

powershell
Import-Certificate -FilePath C:\Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
2.2 On WEF-Marcin
powershell
Import-Certificate -FilePath C:\Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root

$pwd = ConvertTo-SecureString -String "TempP@ssw0rd!" -Force -AsPlainText
Import-PfxCertificate -FilePath C:\Certs\WEF-Marcin-client.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pwd

Then delete the .pfx file from disk once imported (it contains the private key in plaintext-protected form).

2.3 Name resolution (both machines, no shared DNS)

Add hosts file entries so the certificate CN can be resolved:

On WEF-Marcin — add to C:\Windows\System32\drivers\etc\hosts:

192.168.222.142    WEC-Marcin
Phase 3 — Configure WEC-Marcin (Collector)
3.1 Enable WinRM HTTPS listener
powershell
$serverCert = Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEC-Marcin"}

New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * `
  -CertificateThumbPrint $serverCert.Thumbprint -Force
3.2 Enable certificate authentication on the WinRM service
powershell
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true
Set-Item WSMan:\localhost\Service\AllowUnencrypted -Value $false
3.3 Firewall
powershell
New-NetFirewallRule -DisplayName "WinRM HTTPS (5986)" -Direction Inbound -Protocol TCP -LocalPort 5986 -Action Allow
3.4 Create the local account the client cert will map to
powershell
$pw = ConvertTo-SecureString "AnotherStr0ngP@ss!" -AsPlainText -Force
New-LocalUser -Name "WEFClient" -Password $pw -PasswordNeverExpires -UserMayNotChangePassword
Add-LocalGroupMember -Group "Remote Management Users" -Member "WEFClient"
3.5 Map the client certificate to that account
powershell
$rootCAThumb = (Get-ChildItem Cert:\LocalMachine\Root | Where-Object {$_.Subject -eq "CN=Marcin-Lab-RootCA"}).Thumbprint

winrm create winrm/config/service/certmapping?Issuer=$rootCAThumb+Subject="CN=WEF-Marcin"+URI=* `
  '@{Username="WEFClient";Password="AnotherStr0ngP@ss!"}'
3.6 Enable the Windows Event Collector service
powershell
wecutil qc /q
3.7 Create the subscription (source-initiated, non-domain)

Save as C:\Subscriptions\ForwardedEventsSub.xml — replace ROOTCA_THUMBPRINT with $rootCAThumb:

xml
<Subscription xmlns="http://schemas.microsoft.com/2006/03/windows/events/subscription">
  <SubscriptionId>ForwardedEvents-NonDomain</SubscriptionId>
  <SubscriptionType>SourceInitiated</SubscriptionType>
  <Description>Non-domain source-initiated subscription from WEF-Marcin</Description>
  <Enabled>true</Enabled>
  <Uri>http://schemas.microsoft.com/wbem/wsman/1/windows/EventLog</Uri>
  <ConfigurationMode>Custom</ConfigurationMode>
  <Delivery Mode="Push">
    <Batching>
      <MaxItems>5</MaxItems>
      <MaxLatencyTime>900000</MaxLatencyTime>
    </Batching>
    <PushSettings>
      <Heartbeat Interval="900000"/>
    </PushSettings>
  </Delivery>
  <Query>
    <![CDATA[
      <QueryList>
        <Query Id="0">
          <Select Path="Security">*</Select>
          <Select Path="System">*</Select>
        </Query>
      </QueryList>
    ]]>
  </Query>
  <ReadExistingEvents>false</ReadExistingEvents>
  <TransportName>HTTPS</TransportName>
  <ContentFormat>RenderedText</ContentFormat>
  <Locale Language="en-US"/>
  <LogFile>ForwardedEvents</LogFile>
  <AllowedSourceNonDomainComputers>
    <IssuerCAList>
      <IssuerCA>ROOTCA_THUMBPRINT</IssuerCA>
    </IssuerCAList>
  </AllowedSourceNonDomainComputers>
  <AllowedSourceDomainComputers></AllowedSourceDomainComputers>
</Subscription>

Adjust the <Select Path="..."> entries to whichever logs you actually want forwarded.

powershell
wecutil cs C:\Subscriptions\ForwardedEventsSub.xml
Phase 4 — Configure WEF-Marcin (Source)
4.1 Make sure WinRM is running
powershell
Set-Service WinRM -StartupType Automatic
Start-Service WinRM
4.2 Point the source at the collector (Subscription Manager)

This is the registry equivalent of the GPO "Configure target Subscription Manager" — use it directly since there's no domain/GPO:

powershell
$rootCAThumb = (Get-ChildItem Cert:\LocalMachine\Root | Where-Object {$_.Subject -eq "CN=Marcin-Lab-RootCA"}).Thumbprint

New-Item -Path "HKLM:\Software\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager" -Force

New-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager" `
  -Name "1" -PropertyType String `
  -Value "Server=https://WEC-Marcin:5986/wsman/SubscriptionManager/WEC,Refresh=60,IssuerCA=$rootCAThumb"
4.3 Force the Event Log service to re-read the config
powershell
Restart-Service EventLog -Force

(This can briefly restart dependent services — schedule accordingly. Alternatively just wait for the 60-second refresh interval you set above.)

4.4 Firewall (outbound)

Outbound is usually allowed by default, but if WEF-Marcin has a restrictive outbound policy:

powershell
New-NetFirewallRule -DisplayName "WinRM HTTPS Outbound" -Direction Outbound -Protocol TCP -RemotePort 5986 -Action Allow
Phase 5 — Verify

On WEF-Marcin — check the forwarding plugin's operational log for connection attempts:

powershell
Get-WinEvent -LogName "Microsoft-Windows-Eventlog-ForwardingPlugin/Operational" -MaxEvents 20

Event ID 100 = subscription created/active. Errors here usually point to cert trust or SubscriptionManager URL issues.

On WEC-Marcin — check subscription runtime status and incoming events:

powershell
wecutil gr ForwardedEvents-NonDomain
Get-WinEvent -LogName "ForwardedEvents" -MaxEvents 20

Also check Microsoft-Windows-Eventlog/Operational and Windows Remote Management logs on WEC-Marcin if the subscription shows as inactive.

Common gotchas
Cert CN mismatch: the URL in SubscriptionManager (WEC-Marcin) must match the server cert's Subject/SAN and resolve via hosts file — this is the #1 cause of TLS handshake failures.
Clock skew: certificate validation fails if the two machines' clocks drift too far apart — verify time sync.
Firewall: 5986 must be reachable inbound on WEC-Marcin from WEF-Marcin's IP.
wecutil qc must run before creating the subscription, or wecutil cs will fail.
If events don't appear, double-check the mapped local account (WEFClient) is actually in Remote Management Users — this is the most common permission miss.





On WEF-Marcin:

powershell
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEF-Marcin"} | Select Subject, Thumbprint, HasPrivateKey
powershell
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "WEC-Marcin"

On WEC-Marcin:

powershell
winrm enumerate winrm/config/listener





ix — run on WEC-Marcin:

1. Confirm what that wrong thumbprint actually is (helps confirm the theory, optional):

powershell
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Thumbprint -eq "5EEB6B2BE33872893D1EA7628B61464DFB5B2B2B"} | Select Subject, Issuer

2. Delete the existing HTTPS listener:

powershell
Get-ChildItem WSMan:\localhost\Listener | Where-Object {$_.Keys -like "Transport=HTTPS"}

Then remove it — easiest is via the listener's path shown above, or:

Paste back what these three show — particularly HasPrivateKey (a client cert with no private key is a very common cause of exactly this Schannel error) and whether the listener's bound thumbprint actually matches your WEC-Marcin server cert rather than a different/auto-generated one.



