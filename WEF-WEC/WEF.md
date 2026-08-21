1. Check for leftovers from the earlier round
powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|Marcin"} |
  Select-Object @{n='Store';e={$_.PSParentPath -replace '.*\\',''}}, Subject, Thumbprint |
  Format-Table -AutoSize

Remove anything that comes back — every other box had stale certs:

powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|Marcin"} |
  Remove-Item
2. Import the two certs this machine needs
powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEF-Marcin-1.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
3. Verify
powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|Marcin"} |
  Select-Object @{n='Store';e={$_.PSParentPath -replace '.*\\',''}}, Subject, Thumbprint, HasPrivateKey |
  Format-Table -AutoSize

Expect exactly two rows: 2CFBC70E… in Root, B538B862… in My with HasPrivateKey = True.

4. Grant NETWORK SERVICE read on the private key

certlm.msc → Personal → Certificates → WEF-Marcin-1 → right-click → All Tasks → Manage Private Keys → Add → NETWORK SERVICE → Read.

5. Point WEC-Cluster at the active collector
powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "192.168.222.142`tWEC-Cluster"
Clear-DnsClientCache
Resolve-DnsName WEC-Cluster

Should return 192.168.222.142.

6. Set SubscriptionManager
powershell
$key = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager"
New-Item -Path $key -Force | Out-Null
Set-ItemProperty -Path $key -Name "1" -Value "Server=HTTPS://WEC-Cluster:5986/wsman/Subscriptio


Paste this into the Value field:

Server=HTTPS://WEC-Cluster:5986/wsman/SubscriptionManager/WEC,Refresh=60,IssuerCA=2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA

Then OK → Apply → OK, and force a policy refresh:

powershell
gpupdate /force
Restart-Service Wecsvc
One thing to be aware of

Setting this via Local Group Policy writes to the same registry location you'd otherwise set directly. If you already ran the Set-ItemProperty command from earlier, you now have two sources managing the same key — and policy wins on every refresh. Pick one approach.

Group Policy is the better one here: it's what you'd use in a real deployment, and the value persists correctly across gpupdate cycles. If you set the registry key manually beforehand, policy will simply overwrite it with whatever's in this dialog, which is fine as long as the values match.

Verify what actually landed:

powershell
Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager"
On the thumbprint

The policy help text describes IssuerCA as the thumbprint of the client authentication certificate, which is misleading — it's actually the issuing CA's thumbprint, which is what 2CFBC70E… is. Your client cert (B538B862…) doesn't go here.

Once applied, watch for the subscription being picked up:

powershell
Get-WinEvent -LogName "Microsoft-Windows-Eventlog-ForwardPlugin/Operational" -MaxEvents 20 |
  Format-Table TimeCreated, Id, LevelDisplayName, Message -AutoSize -Wrap


  ----------------
  -------------------
  -----------------



  Paste this into the Value field:

Server=HTTPS://WEC-Cluster:5986/wsman/SubscriptionManager/WEC,Refresh=60,IssuerCA=2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA

Then OK → Apply → OK, and force a policy refresh:

powershell
gpupdate /force
Restart-Service Wecsvc
One thing to be aware of

Setting this via Local Group Policy writes to the same registry location you'd otherwise set directly. If you already ran the Set-ItemProperty command from earlier, you now have two sources managing the same key — and policy wins on every refresh. Pick one approach.

Group Policy is the better one here: it's what you'd use in a real deployment, and the value persists correctly across gpupdate cycles. If you set the registry key manually beforehand, policy will simply overwrite it with whatever's in this dialog, which is fine as long as the values match.

Verify what actually landed:

powershell
Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager"
On the thumbprint

The policy help text describes IssuerCA as the thumbprint of the client authentication certificate, which is misleading — it's actually the issuing CA's thumbprint, which is what 2CFBC70E… is. Your client cert (B538B862…) doesn't go here.

Once applied, watch for the subscription being picked up:

powershell
Get-WinEvent -LogName "Microsoft-Windows-Eventlog-ForwardPlugin/Operational" -MaxEvents 20 |
  Format-Table TimeCreated, Id, LevelDisplayName, Message -AutoSize -Wrap

--------------
----------------

Hosts entry:

powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "192.168.222.142`tWEC-Cluster"
Clear-DnsClientCache
Resolve-DnsName WEC-Cluster



OR
# WEF/WEC lab
192.168.222.142    WEC-Cluster
192.168.222.142    WEC-Marcin-1
192.168.222.144    WEC-Marcin-2



  
