corrections:
Delete the old mapping:

powershell
winrm delete "winrm/config/service/certmapping?Issuer=A907BFAD652039ACAF49A8C0C433F70D7289D128+Subject=CN=WEF-Marcin+URI=*"

Confirm what's left:

powershell
Get-ChildItem WSMan:\localhost\ClientCertificate | Format-List *

Remove any other stale entries the same way. Or via the WSMan provider, which is easier when you're not sure of the exact selectors:

powershell
Get-ChildItem WSMan:\localhost\ClientCertificate | Remove-Item -Recurse -Force

Then create the new one:

powershell
winrm create "winrm/config/service/certmapping?Issuer=2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA+Subject=CN=WEF-Marcin-1+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

Verify:

powershell
Get-ChildItem WSMan:\localhost\ClientCertificate | Format-List *

Worth checking the rest of this box for the same staleness, since the mapping clearly isn't the only thing left over. The listener is probably still bound to the old server cert:

powershell
Get-ChildItem WSMan:\localhost\Listener | ForEach-Object { Get-Item "WSMan:\localhost\Listener\$($_.Name)\CertificateThumbprint" }

If it shows an old thumbprint, rebind:

powershell
Set-Item -Path "WSMan:\localhost\Listener\<listener-name>\CertificateThumbprint" -Value "B320815C2A34A8AC14588F01C6E6A601A41CB490"
Restart-Service WinRM

And clear out the superseded certs so you don't bind the wrong one later:

powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "Marcin|WEF-Lab"} |
  Select-Object PSParentPath, Subject, Thumbprint, NotAfter

Anything with the old thumbprints can be removed with Remove-Item Cert:\LocalMachine\My\<thumbprint>.



----------------------


Consolidated build using the hosts file for the failover switch, since that's what you just confirmed. IPs: WEF-Marcin 192.168.222.100, WEC-Marcin-1 192.168.222.142 (active), WEC-Marcin-2 192.168.222.144 (standby).

Step 1 — Generate all certificates (run once, on any one machine as Admin)
powershell
mkdir C:\WEF-Certs -Force
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText

$rootCA = New-SelfSignedCertificate -Type Custom -Subject "CN=WEF-Lab-RootCA" -KeyExportPolicy Exportable -KeyLength 4096 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(10) -CertStoreLocation Cert:\LocalMachine\My -KeyUsage CertSign,CRLSign,DigitalSignature -TextExtension @("2.5.29.19={text}CA=true&pathlength=1")

$wec1 = New-SelfSignedCertificate -Type Custom -Subject "CN=WEC-Marcin-1" -DnsName "WEC-Marcin-1","WEC-Cluster","192.168.222.142" -KeyExportPolicy Exportable -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(5) -CertStoreLocation Cert:\LocalMachine\My -Signer $rootCA -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1")

$wec2 = New-SelfSignedCertificate -Type Custom -Subject "CN=WEC-Marcin-2" -DnsName "WEC-Marcin-2","WEC-Cluster","192.168.222.144" -KeyExportPolicy Exportable -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(5) -CertStoreLocation Cert:\LocalMachine\My -Signer $rootCA -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1")

$wef = New-SelfSignedCertificate -Type Custom -Subject "CN=WEF-Marcin" -DnsName "WEF-Marcin","192.168.222.100" -KeyExportPolicy Exportable -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(5) -CertStoreLocation Cert:\LocalMachine\My -Signer $rootCA -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2")

Export-Certificate -Cert $rootCA -FilePath C:\WEF-Certs\RootCA.cer
Export-Certificate -Cert $wef -FilePath C:\WEF-Certs\WEF-Marcin.cer
Export-PfxCertificate -Cert $wec1 -FilePath C:\WEF-Certs\WEC-Marcin-1.pfx -Password $pw
Export-PfxCertificate -Cert $wec2 -FilePath C:\WEF-Certs\WEC-Marcin-2.pfx -Password $pw
Export-PfxCertificate -Cert $wef  -FilePath C:\WEF-Certs\WEF-Marcin.pfx  -Password $pw

"RootCA: $($rootCA.Thumbprint)"
"WEC-1:  $($wec1.Thumbprint)"
"WEC-2:  $($wec2.Thumbprint)"
"WEF:    $($wef.Thumbprint)"

Save the four thumbprints somewhere. Copy the contents of C:\WEF-Certs\ to each of the three machines.

Step 2 — WEC-Marcin-1 (192.168.222.142)
powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEC-Marcin-1.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
Import-Certificate -FilePath C:\WEF-Certs\WEF-Marcin.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople

Grant NETWORK SERVICE read on the private key: certlm.msc → Personal → WEC-Marcin-1 cert → All Tasks → Manage Private Keys → add NETWORK SERVICE, Read.

powershell
$myThumb = (Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEC-Marcin-1"}).Thumbprint
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint $myThumb -Force
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true

net user WEFClient "AnotherStr0ngP@ss!" /add
net localgroup "Event Log Readers" WEFClient /add

$rootCAThumb = (Get-ChildItem Cert:\LocalMachine\Root | Where-Object {$_.Subject -eq "CN=WEF-Lab-RootCA"}).Thumbprint
winrm create "winrm/config/service/certmapping?Issuer=$rootCAThumb+Subject=CN=WEF-Marcin+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

wecutil qc /q
Step 3 — WEC-Marcin-2 (192.168.222.144) — identical, swap the cert file and CN
powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEC-Marcin-2.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
Import-Certificate -FilePath C:\WEF-Certs\WEF-Marcin.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople

Same private-key permission step, on the WEC-Marcin-2 cert this time.

powershell
$myThumb = (Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEC-Marcin-2"}).Thumbprint
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint $myThumb -Force
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true

net user WEFClient "AnotherStr0ngP@ss!" /add
net localgroup "Event Log Readers" WEFClient /add

$rootCAThumb = (Get-ChildItem Cert:\LocalMachine\Root | Where-Object {$_.Subject -eq "CN=WEF-Lab-RootCA"}).Thumbprint
winrm create "winrm/config/service/certmapping?Issuer=$rootCAThumb+Subject=CN=WEF-Marcin+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

wecutil qc /q
Step 4 — Create the subscription on WEC-Marcin-1, copy to WEC-Marcin-2

Build your subscription on collector 1 (Event Viewer or wecutil cs with an XML file) and confirm it works with WEF-Marcin before replicating. Then:

powershell
# on WEC-Marcin-1
wecutil gs <SubscriptionName> /f:xml > C:\WEF-Certs\sub.xml

Copy sub.xml to WEC-Marcin-2:

powershell
# on WEC-Marcin-2
wecutil cs C:\WEF-Certs\sub.xml

Both collectors now hold identical subscriptions.

Step 5 — WEF-Marcin (192.168.222.100)
powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEF-Marcin.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw

Grant NETWORK SERVICE read on the WEF-Marcin cert's private key, same certlm.msc route.

Add the hosts entry, pointing at the active collector:

powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "192.168.222.142`tWEC-Cluster"
Clear-DnsClientCache
Resolve-DnsName WEC-Cluster

Should return 192.168.222.142.

Set the SubscriptionManager key:

powershell
$rootCAThumb = "96C8A3636650D7DF28CFE1C8A7E4C69631847EA1"
$key = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager"
New-Item -Path $key -Force | Out-Null
Set-ItemProperty -Path $key -Name "1" -Value "Server=HTTPS://WEC-Cluster:5986/wsman/SubscriptionManager/WEC,Refresh=60,IssuerCA=$rootCAThumb"
Restart-Service Wecsvc

Test:

powershell
$myThumb = (Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEF-Marcin"}).Thumbprint
winrm identify -remote:https://WEC-Cluster:5986 -certificate:"$myThumb"
Get-WinEvent -LogName "Microsoft-Windows-Eventlog-ForwardPlugin/Operational" -MaxEvents 20
Step 6 — Prove collector 2 independently before trusting it as a real standby
powershell
(Get-Content C:\Windows\System32\drivers\etc\hosts) -replace '192\.168\.222\.142\s+WEC-Cluster', '192.168.222.144    WEC-Cluster' | Set-Content C:\Windows\System32\drivers\etc\hosts
Clear-DnsClientCache
Resolve-DnsName WEC-Cluster
winrm identify -remote:https://WEC-Cluster:5986 -certificate:"$myThumb"

Clean identify response confirms collector 2 genuinely works, not just that the config looks right. Switch back:

powershell
(Get-Content C:\Windows\System32\drivers\etc\hosts) -replace '192\.168\.222\.144\s+WEC-Cluster', '192.168.222.142    WEC-Cluster' | Set-Content C:\Windows\System32\drivers\etc\hosts
Clear-DnsClientCache
Failover procedure — the thing you're actually simulating
powershell
(Get-Content C:\Windows\System32\drivers\etc\hosts) -replace '192\.168\.222\.142\s+WEC-Cluster', '192.168.222.144    WEC-Cluster' | Set-Content C:\Windows\System32\drivers\etc\hosts
Clear-DnsClientCache

WEF-Marcin re-resolves WEC-Cluster immediately on the next connection attempt, or on its own within the Refresh=60 interval regardless. Confirm with:

powershell
Get-WinEvent -LogName "Microsoft-Windows-Eventlog-ForwardPlugin/Operational" -MaxEvents 10

Look for a new subscription/heartbeat entry referencing 192.168.222.144 shortly after the switch.

Known limitations




Good — all four generated. Substituting the real thumbprints into the remaining steps so you're not retyping them:

WEC-Marcin-1 — listener + mapping
powershell
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint "A3F4CD6605259395E58A50D4D6936512FFC226CF" -Force
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true

net user WEFClient "AnotherStr0ngP@ss!" /add
net localgroup "Event Log Readers" WEFClient /add

winrm create "winrm/config/service/certmapping?Issuer=A907BFAD652039ACAF49A8C0C433F70D7289D128+Subject=CN=WEF-Marcin+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

wecutil qc /q
WEC-Marcin-2 — same, different thumbprint
powershell
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint "A7624FB4FB4778AF3BCFBFC0C9BE621D94AE4363" -Force
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true

net user WEFClient "AnotherStr0ngP@ss!" /add
net localgroup "Event Log Readers" WEFClient /add

winrm create "winrm/config/service/certmapping?Issuer=A907BFAD652039ACAF49A8C0C433F70D7289D128+Subject=CN=WEF-Marcin+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

wecutil qc /q
WEF-Marcin — SubscriptionManager and identify test
powershell
$key = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager"
New-Item -Path $key -Force | Out-Null
Set-ItemProperty -Path $key -Name "1" -Value "Server=HTTPS://WEC-Cluster:5986/wsman/SubscriptionManager/WEC,Refresh=60,IssuerCA=A907BFAD652039ACAF49A8C0C433F70D7289D128"
Restart-Service Wecsvc
powershell
winrm identify -remote:https://WEC-Cluster:5986 -certificate:"5CCD3042628151B34DC0C94196A54FE45C73BE1E"

One thing worth flagging on that WEF thumbprint — count the characters: 5CCD3042628151B34DC0C94196A54FE45C73BE1E is 41, one longer than a standard 40-character SHA1 thumbprint. Worth re-pulling it directly rather than retyping, to rule out a transcription slip:

powershell
(Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEF-Marcin"}).Thumbprint

Run that on WEF-Marcin once the cert is imported there, and use whatever it actually prints in the certmapping and identify commands rather than the value transcribed from the screenshot.

Manual failover, not automatic. Nothing detects collector 1 going down — you (or a script) has to flip the hosts entry.

Bookmark gap. Collector 2 has never seen WEF-Marcin, so depending on ReadExistingEvents in the subscription, expect either a gap or a backlog on first connection.

Single source only, by design. With more forwarders you'd want the Debian DNS approach instead, so failover is one change in one place rather than editing hosts files on every source.
