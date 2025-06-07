# SSL
## Create PrivateKey

` /opt/splunk/etc/auth/mycerts `

` openssl genrsa -aes256 -out CAPrivateKey.key 2048 `
![image](https://github.com/user-attachments/assets/bac20b9c-998b-409e-b8a3-767ee47f23e3)

## Create CSR
` openssl req -new -key CAPrivateKey.key -out CACertificate.csr ` 

![image](https://github.com/user-attachments/assets/d99bd887-dcc6-47bf-a81b-dc756627183a)

## Signing a CSR with a CA (Certificate Authority)

`
openssl x509 -req -in CACertificate.csr -sha512 -signkey CAPrivateKey.key -CAcreateserial -out CAPCertificate.pem -days 1000
`

## Testing

`
openssl s_server -accept 9997 -cert CAPCertificate.pem
`
