# SSL


![image](https://github.com/user-attachments/assets/563d6595-4604-4604-9040-63a34ba9d7e7)

## Create PrivateKey

` /opt/splunk/etc/auth/mycerts `

` openssl genrsa -aes256 -out CAPrivateKey.key 2048 `
![image](https://github.com/user-attachments/assets/bac20b9c-998b-409e-b8a3-767ee47f23e3)

## Generate Certificate Sign Request  CSR
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
## Files 
inputs.conf
server.conf

From https://www.youtube.com/watch?v=8Hbd9BMoM38&t=706s&ab_channel=OctoberLeaf

## For Chrome to accest signed certificate 
![image](https://github.com/user-attachments/assets/af92b740-3a98-4dfc-ab93-3299a866f922)


Create pirivate key
![image](https://github.com/user-attachments/assets/72eda094-6b9a-4958-a60a-1b69eef0a353)

Generate CSR
![image](https://github.com/user-attachments/assets/43bf273f-54f4-49d0-be99-69b36e583536)



