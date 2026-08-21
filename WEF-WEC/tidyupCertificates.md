This is WEC-Marcin-1, and the stores are now empty — the two queries returned nothing, so the cleanup worked. Fresh start.

Import the three certs this collector needs:

powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEC-Marcin-1.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
Import-Certificate -FilePath C:\WEF-Certs\WEF-Marcin-1.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople

Verify all three, with private key on the server cert:

powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|Marcin"} |
  Select-Object @{n='Store';e={$_.PSParentPath -replace '.*\\',''}}, Subject, Thumbprint, HasPrivateKey |
  Format-Table -AutoSize

Expecting exactly:

Store	Subject	Thumbprint	HasPrivateKey
Root	CN=WEF-Lab-RootCA	2CFBC70E…	False
My	CN=WEC-Marcin-1	B320815C…	True
TrustedPeople	CN=WEF-Marcin-1	B538B862…	False

Then the private key permission — certlm.msc → Personal → Certificates → WEC-Marcin-1 → right-click → All Tasks → Manage Private Keys → Add → NETWORK SERVICE → Read.

Then the listener, auth, account, and mapping:

powershell
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint "B320815C2A34A8AC14588F01C6E6A601A41CB490" -Force
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true

net user WEFClient "AnotherStr0ngP@ss!" /add
net localgroup "Event Log Readers" WEFClient /add

winrm create "winrm/config/service/certmapping?Issuer=2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA+Subject=CN=WEF-Marcin-1+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

wecutil qc /q

If the listener already exists from the earlier round, New-Item will error — in that case rebind instead:

powershell
$l = Get-ChildItem WSMan:\localhost\Listener | Where-Object {$_.Keys -contains "Transport=HTTPS"}
Set-Item -Path "WSMan:\localhost\Listener\$($l.Name)\CertificateThumbprint" -Value "B320815C2A34A8AC14588F01C6E6A601A41CB490"
Restart-Service WinRM
