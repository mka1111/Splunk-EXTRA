tcpdump -q ip src 10.0.2.3 and portrange 9000-9999
tcpdump -A to see plain text

iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 9997 -j DNAT --to-destination 10.0.1.1:9997
tcpdump -i any -n host 8.8.8.8 and port 53
tcpdump -q ip src 10.0.2.3 and portrange 9000-9999


openssl s_client -showcerts -connect www.serverfault.com:443
vmstat -d

ping -I eth0 google.com

traceroute -T -p 443 google.com





https://www.xolphin.com/support/OpenSSL/Frequently_used_OpenSSL_Commands


Frequently used OpenSSL Commands
General OpenSSL Commands
The following commands show how to create CSRs, certificates and private keys, in addition to a few other tasks using OpenSSL.

Generate a new private key and CSR (Unix)
openssl req -utf8 -nodes -sha256 -newkey rsa:2048 -keyout server.key -out server.csr
openssl req -out CSR.csr -pubkey -new -keyout privateKey.key
Generate a new private key and CSR (Windows)
openssl req -out CSR.csr -pubkey -new -keyout privateKey.key -config .shareopenssl.cmf
Generate a CSR for an existing private key
openssl req -out CSR.csr -key privateKey.key -new
Generate a CSR based on an existing certificate
openssl x509 -x509toreq -in MYCRT.crt -out CSR.csr -signkey privateKey.key
Generate a self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privateKey.key -out certificate.crt
Remove a password from a private key
openssl rsa -in privateKey.pem -out newPrivateKey.pem
Check the CSR, Private Key or Certificate using OpenSSL
Use the following commands to check the information of a certificate, CSR or private key. Our online Tools LINK can also be used for this purpose.

Check a CSR
openssl req -text -noout -verify -in CSR.csr
Check a private key
openssl rsa -in privateKey.key -check
Check a certificate
openssl x509 -in certificate.crt -text -noout
Check a PKCS#12 file (.pfx or .p12)
openssl pkcs12 -info -in keyStore.p12
Debugging with OpenSSL
With error messages like 'the Private Key does not match the Certificate' or 'the Certificate is not Trusted' you can use one of the following commands. Please also use our online SSL Check LINK tool to check the certificate.

Check the MD5 hash of the public key to check if it is equal to what is in the CSR or private key.
openssl x509 -noout -modulus -in certificate.crt | openssl md5
openssl rsa -noout -modulus -in privateKey.key | openssl md5
openssl req -noout -modulus -in CSR.csr | openssl md5
Check an SSL connection. All certificates (also intermediate certificates) should be displayed.
openssl s_client -connect www.paypal.com:443
Convert certificates using OpenSSL
With the commands below files can be converted to another format. This is sometimes necessary to make certificates or private keys suitable for different types of servers or software. A PEM file for Apache can, for example, be converted to a PFX (PCKS#12) file for use with Tomcat or IIS.

Convert a DER file (.crt .cer .der) to PEM
openssl x509 -inform der -in certificate.cer -out certificate.pem
Convert a PEM file to DER
openssl x509 -outform der -in certificate.pem -out certificate.der
Convert a PKCS#12 file (.pfx .p12) including the private key and certificate(s) to PEM
openssl pkcs12 -in keyStore.pfx -out keyStore.pem -nodes
Note: Add -nocerts to only convert the private key, or add -nokeys to convert only the certificates.

Convert a PEM certificate file and a private key to PKCS#12 (.pfx .p12)
openssl pkcs12 -export -out certificate.pfx -inkey privateKey.key -in certificate.crt -certfile CACert.crt
