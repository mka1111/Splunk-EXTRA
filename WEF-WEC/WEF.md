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
