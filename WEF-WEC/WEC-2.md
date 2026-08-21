You're on WEC-Marcin-2 at 192.168.222.144, matching its cert SAN, and all the cert files are present. Here's the full sequence — same as collector 1, different thumbprint.

1. Check for stale certs
powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|Marcin"} |
  Select-Object @{n='Store';e={$_.PSParentPath -replace '.*\\',''}}, Subject, Thumbprint |
  Format-Table -AutoSize

Remove anything found:

powershell
Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\Root, Cert:\LocalMachine\TrustedPeople |
  Where-Object {$_.Subject -match "WEF-Lab-RootCA|Marcin"} | Remove-Item
2. Import
powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\wef-certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\wef-certs\WEC-Marcin-2.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
Import-Certificate -FilePath C:\wef-certs\WEF-Marcin-1.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople
3. Private key permission

certlm.msc → Personal → Certificates → WEC-Marcin-2 → All Tasks → Manage Private Keys → Add → NETWORK SERVICE → Read.

4. Listener and auth
powershell
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint "EE81D9A17D5B4C7C55CC14F77F8ED4A996A95418" -Force
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true
5. Account and mapping
powershell
net user WEFClient "AnotherStr0ngP@ss!" /add
net localgroup "Event Log Readers" WEFClient /add

winrm create "winrm/config/service/certmapping?Issuer=2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA+Subject=CN=WEF-Marcin-1+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'
6. Enable client cert negotiation

The step that caught you on collector 1 — it defaults to disabled:

powershell
netsh http show sslcert ipport=0.0.0.0:5986

Grab the Application ID from that output, then:

powershell
netsh http delete sslcert ipport=0.0.0.0:5986
netsh http add sslcert ipport=0.0.0.0:5986 certhash=EE81D9A17D5B4C7C55CC14F77F8ED4A996A95418 appid="{PASTE-APPID-HERE}" certstorename=MY clientcertnegotiation=enable

Verify:

powershell
netsh http show sslcert ipport=0.0.0.0:5986 | Select-String "Certificate Hash|Negotiate Client Certificate"
7. Collector service and subscription
powershell
wecutil qc /q
wecutil cs C:\share-Marcin\sub-export.xml
wecutil es
8. Verify
powershell
Get-ChildItem WSMan:\localhost\Listener
Get-ChildItem WSMan:\localhost\ClientCertificate | Format-List *

-----------------------
------------------
Mapping created correctly, and the SSL binding has the right cert hash. But Negotiate Client Certificate is Disabled — same as collector 1 before you fixed it.

The appid is the same one: {afebb9ad-9b97-4a91-9ab5-daf4d59122f6}.

powershell
netsh http delete sslcert ipport=0.0.0.0:5986

netsh http add sslcert ipport=0.0.0.0:5986 certhash=EE81D9A17D5B4C7C55CC14F77F8ED4A996A95418 appid="{afebb9ad-9b97-4a91-9ab5-daf4d59122f6}" certstorename=MY clientcertnegotiation=enable

Verify:

powershell
netsh http show sslcert ipport=0.0.0.0:5986 | Select-String "Certificate Hash|Negotiate Client Certificate|Certificate Store Name"

Want Enabled on negotiation and MY as the store name.

powershell
Restart-Service WinRM

Then the collector service and subscription:

powershell
wecutil qc /q
wecutil cs C:\share-Marcin\sub-export.xml
wecutil es

Also still outstanding here: Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true, and the NETWORK SERVICE private key permission on the WEC-Marcin-2 cert — worth confirming both before you test failover, since a miss on either produces the same opaque failure you hit earlier.
Get-Service Wecsvc, WinRM

Two things worth noting. There's a stray HTTP listener on collector 1 that you may want to remove here too once the HTTPS one is up. And RootCA.key is sitting in this directory — the CA private key on a collector isn't where it belongs long-term.

Once this is done, flip the hosts entry on WEF-Marcin-1 to .144, Clear-DnsClientCache, and wecutil gr ac here should show the source connecting.
===================
====================
==============
255 254 confirms it — UTF-16LE BOM, exactly as suspected. The 60 0 after it is < in UTF-16, so the content is fine; only the encoding is wrong.

Convert it:

powershell
$x = Get-Content .\sub-export.xml -Raw
[System.IO.File]::WriteAllText("$PWD\sub-export-utf8.xml", $x, (New-Object System.Text.UTF8Encoding($false)))

Verify the BOM is gone — should now start with 60 63 83 109 (<?xml):

powershell
Get-Content .\sub-export-utf8.xml -Encoding Byte -TotalCount 4

Then import:

powershell
wecutil cs .\sub-export-utf8.xml
wecutil es

For future exports, avoid the problem at source by using Out-File -Encoding utf8 rather than >:

powershell
wecutil gs ac /f:xml | Out-File -FilePath C:\share-Marcin\sub-export.xml -Encoding utf8

If wecutil cs throws a different error after the encoding fix, that's progress — it means the parser is now reading the file and objecting to something in the content. Paste whatever it says and we'll work from there.
