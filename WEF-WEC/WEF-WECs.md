ull set with your confirmed values. Run all of this on the Linux box.

Generate everything
bash
mkdir -p ~/wef-certs && cd ~/wef-certs
PW="ChangeThis123!"

# --- Root CA ---
openssl genrsa -out RootCA.key 4096
openssl req -x509 -new -nodes -key RootCA.key -sha256 -days 3650 \
  -subj "/CN=WEF-Lab-RootCA" -out RootCA.pem

# --- WEC-Marcin-1 (192.168.222.142) ---
openssl genrsa -out WEC-Marcin-1.key 2048
openssl req -new -key WEC-Marcin-1.key -subj "/CN=WEC-Marcin-1" -out WEC-Marcin-1.csr
cat > WEC-Marcin-1.ext <<'EOF'
subjectAltName = DNS:WEC-Marcin-1, DNS:WEC-Cluster, IP:192.168.222.142
extendedKeyUsage = serverAuth
EOF
openssl x509 -req -in WEC-Marcin-1.csr -CA RootCA.pem -CAkey RootCA.key -CAcreateserial \
  -out WEC-Marcin-1.crt -days 1825 -sha256 -extfile WEC-Marcin-1.ext

# --- WEC-Marcin-2 (192.168.222.144) ---
openssl genrsa -out WEC-Marcin-2.key 2048
openssl req -new -key WEC-Marcin-2.key -subj "/CN=WEC-Marcin-2" -out WEC-Marcin-2.csr
cat > WEC-Marcin-2.ext <<'EOF'
subjectAltName = DNS:WEC-Marcin-2, DNS:WEC-Cluster, IP:192.168.222.144
extendedKeyUsage = serverAuth
EOF
openssl x509 -req -in WEC-Marcin-2.csr -CA RootCA.pem -CAkey RootCA.key -CAcreateserial \
  -out WEC-Marcin-2.crt -days 1825 -sha256 -extfile WEC-Marcin-2.ext

# --- WEF-Marcin-1 (192.168.222.158) ---
openssl genrsa -out WEF-Marcin-1.key 2048
openssl req -new -key WEF-Marcin-1.key -subj "/CN=WEF-Marcin-1" -out WEF-Marcin-1.csr
cat > WEF-Marcin-1.ext <<'EOF'
subjectAltName = DNS:WEF-Marcin-1, IP:192.168.222.158
extendedKeyUsage = clientAuth
EOF
openssl x509 -req -in WEF-Marcin-1.csr -CA RootCA.pem -CAkey RootCA.key -CAcreateserial \
  -out WEF-Marcin-1.crt -days 1825 -sha256 -extfile WEF-Marcin-1.ext
Export to Windows formats
bash
openssl x509 -outform der -in RootCA.pem -out RootCA.cer
openssl x509 -outform der -in WEF-Marcin-1.crt -out WEF-Marcin-1.cer

openssl pkcs12 -export -out WEC-Marcin-1.pfx -inkey WEC-Marcin-1.key -in WEC-Marcin-1.crt -certfile RootCA.pem -passout pass:$PW
openssl pkcs12 -export -out WEC-Marcin-2.pfx -inkey WEC-Marcin-2.key -in WEC-Marcin-2.crt -certfile RootCA.pem -passout pass:$PW
openssl pkcs12 -export -out WEF-Marcin-1.pfx -inkey WEF-Marcin-1.key -in WEF-Marcin-1.crt -certfile RootCA.pem -passout pass:$PW
Get thumbprints (Windows format, no colons)
bash
for f in RootCA.pem WEC-Marcin-1.crt WEC-Marcin-2.crt WEF-Marcin-1.crt; do
  printf "%-20s %s\n" "$f" "$(openssl x509 -in $f -noout -fingerprint -sha1 | cut -d= -f2 | tr -d ':')"
done
Verify SANs and EKUs before copying
bash
for f in WEC-Marcin-1 WEC-Marcin-2 WEF-Marcin-1; do
  echo "=== $f ==="
  openssl x509 -in $f.crt -noout -text | grep -A1 "Subject Alternative Name"
  openssl x509 -in $f.crt -noout -text | grep -A1 "Extended Key Usage"
done
Distribution
File	WEC-Marcin-1	WEC-Marcin-2	WEF-Marcin-1
RootCA.cer	→ Root	→ Root	→ Root
WEC-Marcin-1.pfx	→ My	—	—
WEC-Marcin-2.pfx	—	→ My	—
WEF-Marcin-1.cer	→ TrustedPeople	→ TrustedPeople	—
WEF-Marcin-1.pfx	—	—	→ My
Import on each Windows box

WEC-Marcin-1:

powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEC-Marcin-1.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
Import-Certificate -FilePath C:\WEF-Certs\WEF-Marcin-1.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople

WEC-Marcin-2: same, with WEC-Marcin-2.pfx.

WEF-Marcin-1:

powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEF-Marcin-1.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw

Note the subject is now CN=WEF-Marcin-1, not CN=WEF-Marcin — so the certmapping command on both collectors needs updating to match:

powershell
winrm create "winrm/config/service/certmapping?Issuer=<RootCA thumbprint>+Subject=CN=WEF-Marcin-1+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

Post the thumbprint output from that for loop and I'll fill in the remaining commands with the real values.

All the certs generated — .crt and .key for each of the three, plus the root CA. But the export step hasn't run yet: there are no .cer or .pfx files, which are the formats Windows needs.

Run this next:

bash
cd ~/wef-certs
PW="ChangeThis123!"

openssl x509 -outform der -in RootCA.pem -out RootCA.cer
openssl x509 -outform der -in WEF-Marcin-1.crt -out WEF-Marcin-1.cer

openssl pkcs12 -export -out WEC-Marcin-1.pfx -inkey WEC-Marcin-1.key -in WEC-Marcin-1.crt -certfile RootCA.pem -passout pass:$PW
openssl pkcs12 -export -out WEC-Marcin-2.pfx -inkey WEC-Marcin-2.key -in WEC-Marcin-2.crt -certfile RootCA.pem -passout pass:$PW
openssl pkcs12 -export -out WEF-Marcin-1.pfx -inkey WEF-Marcin-1.key -in WEF-Marcin-1.crt -certfile RootCA.pem -passout pass:$PW

ls -1 *.cer *.pfx

Then grab the thumbprints:

bash
for f in RootCA.pem WEC-Marcin-1.crt WEC-Marcin-2.crt WEF-Marcin-1.crt; do
  printf "%-20s %s\n" "$f" "$(openssl x509 -in $f -noout -fingerprint -sha1 | cut -d= -f2 | tr -d ':')"
done

And verify the SANs landed correctly before you copy anything to Windows:

bash
for f in WEC-Marcin-1 WEC-Marcin-2 WEF-Marcin-1; do
  echo "=== $f ==="
  openssl x509 -in $f.crt -noout -text | grep -A1 "Subject Alternative Name"
done

Post the thumbprint output and I'll write out the listener binding and certmapping commands with the real values filled in.

Updated memory
Updated memory
Areas
›
Windows Wef Wec
Windows Event Forwarding/Collection design — HTTPS + certificate auth model and HA/redundancy across two collectors.

All four are clean 40-character SHA1 thumbprints. Here's everything filled in.

WEC-Marcin-1 (192.168.222.142)
powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEC-Marcin-1.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
Import-Certificate -FilePath C:\WEF-Certs\WEF-Marcin-1.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople

Grant NETWORK SERVICE read on the private key: certlm.msc → Personal → WEC-Marcin-1 → All Tasks → Manage Private Keys → add NETWORK SERVICE, Read.

powershell
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint "B320815C2A34A8AC14588F01C6E6A601A41CB490" -Force
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true

net user WEFClient "AnotherStr0ngP@ss!" /add
net localgroup "Event Log Readers" WEFClient /add

winrm create "winrm/config/service/certmapping?Issuer=2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA+Subject=CN=WEF-Marcin-1+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

wecutil qc /q
WEC-Marcin-2 (192.168.222.144)
powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEC-Marcin-2.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
Import-Certificate -FilePath C:\WEF-Certs\WEF-Marcin-1.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople

Same private-key permission step, on the WEC-Marcin-2 cert.

powershell
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint "EE81D9A17D5B4C7C55CC14F77F8ED4A996A95418" -Force
Set-Item WSMan:\localhost\Service\Auth\Certificate -Value $true

net user WEFClient "AnotherStr0ngP@ss!" /add
net localgroup "Event Log Readers" WEFClient /add

winrm create "winrm/config/service/certmapping?Issuer=2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA+Subject=CN=WEF-Marcin-1+URI=*" '@{UserName="WEFClient";Password="AnotherStr0ngP@ss!"}'

wecutil qc /q
WEF-Marcin-1 (192.168.222.158)
powershell
$pw = ConvertTo-SecureString "ChangeThis123!" -Force -AsPlainText
Import-Certificate -FilePath C:\WEF-Certs\RootCA.cer -CertStoreLocation Cert:\LocalMachine\Root
Import-PfxCertificate -FilePath C:\WEF-Certs\WEF-Marcin-1.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw

Grant NETWORK SERVICE read on the WEF-Marcin-1 private key.

powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "192.168.222.142`tWEC-Cluster"
Clear-DnsClientCache
Resolve-DnsName WEC-Cluster

$key = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager"
New-Item -Path $key -Force | Out-Null
Set-ItemProperty -Path $key -Name "1" -Value "Server=HTTPS://WEC-Cluster:5986/wsman/SubscriptionManager/WEC,Refresh=60,IssuerCA=2CFBC70E7FCCF465F31E0F625C4219F0DE1BD6AA"
Restart-Service Wecsvc
Test the transport
powershell
winrm identify -remote:https://WEC-Cluster:5986 -certificate:"B538B86224DD8B465DF236AA14F2A2CE44A97027"
Failover to WEC-Marcin-2
powershell
(Get-Content C:\Windows\System32\drivers\etc\hosts) -replace '192\.168\.222\.142\s+WEC-Cluster', '192.168.222.144    WEC-Cluster' | Set-Content C:\Windows\System32\drivers\etc\hosts
Clear-DnsClientCache
winrm identify -remote:https://WEC-Cluster:5986 -certificate:"B538B86224DD8B465DF236AA14F2A2CE44A97027"

One thing worth doing before you get too far: the .pfx files were generated with -passout pass:$PW, so the password is in your shell history on mk-linux. Once they're imported on the Windows boxes, clear the working directory:

bash
shred -u ~/wef-certs/*.key ~/wef-certs/*.pfx

Keep RootCA.key if you'll need to issue more certs later — but move it somewhere you're comfortable with, since anyone holding it can mint certs your collectors will trust.

root@mk-linux:~/wef-certs# for f in WEC-Marcin-1 WEC-Marcin-2 WEF-Marcin-1; do
  echo "=== $f ==="
  openssl x509 -in $f.crt -noout -text | grep -A1 "Subject Alternative Name"
  openssl x509 -in $f.crt -noout -text | grep -A1 "Extended Key Usage"
done
=== WEC-Marcin-1 ===
            X509v3 Subject Alternative Name:
                DNS:WEC-Marcin-1, DNS:WEC-Cluster, IP Address:192.168.222.142
            X509v3 Extended Key Usage:
                TLS Web Server Authentication
=== WEC-Marcin-2 ===
            X509v3 Subject Alternative Name:
                DNS:WEC-Marcin-2, DNS:WEC-Cluster, IP Address:192.168.222.144
            X509v3 Extended Key Usage:
                TLS Web Server Authentication
=== WEF-Marcin-1 ===
            X509v3 Subject Alternative Name:
                DNS:WEF-Marcin-1, IP Address:192.168.222.158
            X509v3 Extended Key Usage:
                TLS Web Client Authentication
root@mk-linux:~/wef-certs#

Everything checks out:

Both WEC certs carry WEC-Cluster in the SAN alongside their own name and IP — that's what makes the failover work
EKUs are correct: Server Authentication on the collectors, Client Authentication on the source
IPs match the assignments

Certificate generation is done. Copy the files across per the distribution table and work through the import/listener/mapping commands from the previous message — they're all filled in with your real thumbprints.

Order that'll save you backtracking:

WEC-Marcin-1 — import, private key permission, listener, mapping, wecutil qc
WEF-Marcin-1 — import, private key permission, hosts entry, SubscriptionManager
Test with winrm identify before creating any subscription — if mutual TLS isn't working, you want to know now rather than debugging it through a subscription layer
Create and test the subscription on WEC-Marcin-1
WEC-Marcin-2 — full setup, then wecutil cs the exported subscription XML
Flip the hosts entry and prove collector 2 works independently

The step most likely to trip you up is the private key permission — it's easy to skip because nothing fails immediately, and the error you eventually get doesn't point at it.
