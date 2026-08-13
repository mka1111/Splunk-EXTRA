All three thumbprints are clean 40-character values — good.

Root CA:     B551F8F7DEEA761FF7D1958DB4B835F1AD043F04
Server cert: B9844DEF377382027F2F646516803BEF714F22EE
Client cert: EBCF3D97349DE1E321A32056C3DC65C8218D15C6
Step 3 — Finish setup on WEC-Marcin (same machine, same session)

Rebind the HTTPS listener to the new server cert:

powershell
winrm delete winrm/config/Listener?Address=*+Transport=HTTPS 2>$null

New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * `
  -CertificateThumbPrint "B9844DEF377382027F2F646516803BEF714F22EE" -Force

Re-apply the negotiate-client-cert fix at the HTTP.SYS level (this was the earlier fix — needs to be redone since we deleted the listener):

powershell
netsh http show sslcert ipport=0.0.0.0:5986

Note the Application ID GUID shown, then:

powershell
netsh http delete sslcert ipport=0.0.0.0:5986

netsh http add sslcert ipport=0.0.0.0:5986 `
  certhash=B9844DEF377382027F2F646516803BEF714F22EE `
  appid="{PASTE_APPID_GUID_HERE}" `
  clientcertnegotiation=enable

Ensure service-level cert auth is still on:

powershell
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true

Recreate the local account + certmapping with the new thumbprints:

powershell
# Skip if WEFClient user already exists and is fine
$pw = ConvertTo-SecureString "AnotherStr0ngP@ss!" -AsPlainText -Force
New-LocalUser -Name "WEFClient" -Password $pw -PasswordNeverExpires -UserMayNotChangePassword -ErrorAction SilentlyContinue
Add-LocalGroupMember -Group "Remote Management Users" -Member "WEFClient" -ErrorAction SilentlyContinue

winrm create "winrm/config/service/certmapping?Issuer=B551F8F7DEEA761FF7D1958DB4B835F1AD043F04+Subject=CN=WEF-Marcin+URI=*" "@{Username=`"WEFClient`";Password=`"AnotherStr0ngP@ss!`"}"

winrm enumerate winrm/config/service/certmapping

Confirm this shows one populated entry before moving on.

Update the subscription XML — edit C:\Subscriptions\ForwardedEventsSub.xml, set:

xml
<IssuerCA>B551F8F7DEEA761FF7D1958DB4B835F1AD043F04</IssuerCA>

Then recreate the subscription:

powershell
wecutil ds ForwardedEvents-NonDomain 2>$null
wecutil cs C:\Subscriptions\ForwardedEventsSub.xml
Restart-Service Wecsvc -Force
wecutil gr ForwardedEvents-NonDomain
Step 4 — Set up WEF-Marcin

Copy C:\Certs\RootCA.cer and C:\Certs\WEF-Marcin-client.pfx to WEF-Marcin now, then run:

powershell
Import-Certificate -FilePath C:\Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root

$pwd = ConvertTo-SecureString -String "TempP@ssw0rd!" -Force -AsPlainText
Import-PfxCertificate -FilePath C:\Certs\WEF-Marcin-client.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pwd

Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEF-Marcin"} | Select Subject, Thumbprint, HasPrivateKey

Confirm the thumbprint shown is EBCF3D97349DE1E321A32056C3DC65C8218D15C6 with HasPrivateKey: True.

Update the SubscriptionManager (via gpedit, same dialog as before, or registry directly):

powershell
New-Item -Path "HKLM:\Software\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager" -Force

Set-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager" `
  -Name "1" -Value "Server=https://WEC-Marcin:5986/wsman/SubscriptionManager/WEC,Refresh=60,IssuerCA=B551F8F7DEEA761FF7D1958DB4B835F1AD043F04"

gpupdate /force
Restart-Service EventLog -Force

Then check:

powershell
Get-WinEvent -LogName "Microsoft-Windows-Eventlog-ForwardingPlugin/Operational" -MaxEvents 5

Send me the certmapping enumeration output from Step 3 and the fresh ForwardingPlugin event from Step 4 — with everything now sourced from one clean, verified set of thumbprints, this should either succeed or fail with something new and more specific.

Good — both files are there and ready to copy over to WEF-Marcin. Go ahead and transfer RootCA.cer and WEF-Marcin-client.pfx to WEF-Marcin now (USB/share/however you've been moving files between them), then run the Step 4 commands from my last message on WEF-Marcin.

While that's copying, go ahead and finish Step 3 on WEC-Marcin if you haven't already — specifically:

Listener rebind
netsh http cert negotiation fix
Certmapping recreation — paste me the winrm enumerate winrm/config/service/certmapping output, this is the one that's been silently failing before, so I want to see it populated with the new thumbprints before we move to testing
Subscription XML update + recreate

Write-EventLog -LogName Application -Source "Application" -EventId 9999 -EntryType Information -Message "Test event for WEF forwarding validation"

Once both sides are done, send me:

The certmapping enumeration from WEC-Marcin
The latest Microsoft-Windows-Eventlog-ForwardingPlugin/Operational event from WEF-Marcin after the restart
Get-Acl "HKLM:\SOFTWARE\Microsoft\SystemCertificates\ROOT"

Or more readable:

(Get-Acl "HKLM:\SOFTWARE\Microsoft\SystemCertificates\ROOT").Access |
Format-Table IdentityReference, RegistryRights, AccessControlType

and we'll see where it stands.

Get-ChildItem Cert:\LocalMachine\Root |
Where-Object {$_.Subject -like "*Marcin-Lab-RootCA*"} |
Select-Object Subject, Thumbprint, HasPrivateKey
