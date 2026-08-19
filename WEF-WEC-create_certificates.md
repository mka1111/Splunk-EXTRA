Create and export (run as Admin, one after another):

powershell
$rootCA = New-SelfSignedCertificate -Type Custom -Subject "CN=WEF-Lab-RootCA" -KeyExportPolicy Exportable -KeyLength 4096 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(10) -CertStoreLocation Cert:\LocalMachine\My -KeyUsage CertSign,CRLSign,DigitalSignature -TextExtension @("2.5.29.19={text}CA=true&pathlength=1")
powershell
$serverCert = New-SelfSignedCertificate -Type Custom -Subject "CN=WEC-Marcin" -DnsName "WEC-Marcin","192.168.222.142" -KeyExportPolicy Exportable -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(5) -CertStoreLocation Cert:\LocalMachine\My -Signer $rootCA -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1")
powershell
$clientCert = New-SelfSignedCertificate -Type Custom -Subject "CN=WEF-Marcin" -DnsName "WEF-Marcin" -KeyExportPolicy Exportable -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(5) -CertStoreLocation Cert:\LocalMachine\My -Signer $rootCA -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2")
powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
powershell
Export-Certificate -Cert $rootCA -FilePath C:\WEF-Certs\RootCA.cer
Export-Certificate -Cert $clientCert -FilePath C:\WEF-Certs\ClientCert.cer
Export-PfxCertificate -Cert $serverCert -FilePath C:\WEF-Certs\ServerCert.pfx -Password $pw
Export-PfxCertificate -Cert $clientCert -FilePath C:\WEF-Certs\ClientCert.pfx -Password $pw
powershell
$rootCA.Thumbprint; $serverCert.Thumbprint; $clientCert.Thumbprint

Import on WEC-Marcin:

powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\ServerCert.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
Import-Certificate -FilePath C:\WEF-Certs\ClientCert.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople

Import on WEF-Marcin:

powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\ClientCert.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw

mkdir C:\WEF-Certs first if it doesn't exist.



================
winrm set winrm/config/Listener?Address=*+Transport=HTTPS '@{CertificateThumbprint="B9844DEF377382027F2F646516803BEF714F22EE"}'


$rootCAThumb = (Get-ChildItem Cert:\LocalMachine\Root | Where-Object {$_.Subject -like "*WEF-Lab-RootCA*"}).Thumbprint
$rootCAThumb



