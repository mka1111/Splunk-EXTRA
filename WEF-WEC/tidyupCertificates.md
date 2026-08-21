All three landed with the correct thumbprints — 2CFBC70E… in Root, B320815C… in My, B538B862… in TrustedPeople. WEC-Marcin-1's certificate state is clean.

Confirm the private key came across with the pfx:

powershell
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEC-Marcin-1"} | Select-Object Subject, HasPrivateKey

HasPrivateKey must be True. Then grant NETWORK SERVICE read on it via certlm.msc → Personal → Certificates → WEC-Marcin-1 → All Tasks → Manage Private Keys → Add → NETWORK SERVICE → Read.

Then the remaining collector config:

powershell
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint "B320815C2A34A8AC14588F01C6E6A601A41CB490" -Force
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true

net user WEFClient "AnotherStr0ngP@ss!" /add
net localgroup "Event Log Readers" WEFClient /add

winrm create "winrm/config/service/certmapping?Issuer=2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA+Subject=CN=WEF-Marcin-1+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

wecutil qc /q

The mapping should succeed this time — the issuer it needs is now genuinely in Trusted Root, which was the blocker before.

If net user says the account already exists from the earlier round, that's fine — just make sure the password matches what's in the mapping:

powershell
net user WEFClient "AnotherStr0ngP@ss!"

Verify the lot:

powershell
Get-ChildItem WSMan:\localhost\Listener
Get-ChildItem WSMan:\localhost\ClientCertificate | Format-List *
Get-Service Wecsvc, WinRM

===============
===============


Two things to confirm before moving on:

powershell
netsh http show sslcert ipport=0.0.0.0:5986

Should show certificate hash B320815C2A34A8AC14588F01C6E6A601A41CB490. If it shows an old thumbprint, the HTTP.SYS binding didn't update with the listener and you'd need to fix it separately.

And the NETWORK SERVICE private key permission, if you haven't done it yet — certlm.msc → Personal → WEC-Marcin-1 → All Tasks → Manage Private Keys → Add → NETWORK SERVICE → Read.

Also worth noting there's an HTTP listener (Listener_1184937132) alongside the HTTPS one. That's the default WinRM listener on 5985, unencrypted. Not breaking anything, but since the whole point of this build is certificate-based TLS, it's an open unauthenticated-transport path you probably don't want:

powershell
Remove-Item -Path "WSMan:\localhost\Listener\Listener_1184937132" -Recurse -Force

Next up is WEF-Marcin-1 — import its two certs, grant the key permission, add the hosts entry for WEC-Cluster pointing at .142, set the SubscriptionManager key, then test with winrm identify. That test is the real proof the collector side works, before you layer a subscription on top.
