

<img width="611" height="59" alt="image" src="https://github.com/user-attachments/assets/42a5f56e-2431-423e-977e-10b75eded3d2" />
<img width="998" height="64" alt="image" src="https://github.com/user-attachments/assets/9240731e-9aee-463a-8c29-7841c56ebcaf" />

WinRM e winrm/config/listener



```
WinRM e winrm/config/listener
```


```
New-SelfSignedCertificate -DnsName "CLIENT01" -CertStoreLocation Cert:\LocalMachine\My
```


# Export
```
$caCert = Get-ChildItem -Path Cert:\LocalMachine\My | Where-Object {$_.Thumbprint -eq "CE6E8D48E70FA5F901801CDACA0633D216CAB3BA"}

 Export-Certificate -Cert $caCert -FilePath ca-cert.cer -Type CERT

```



```
winrm delete winrm/config/Listener?Address=*+Transport=HTTPS


winrm create winrm/config/Listener?Address=*+Transport=HTTPS '@{Hostname="CLIENT01"; CertificateThumbprint="CE6E8D48E70FA5F901801CDACA0633D216CAB3BA"}'
```


net localgroup "Event Log Readers" "NT Authority\Network Service" /add


# Firewall 
```
New-NetFirewallRule -DisplayName "WEF_HTTPS_5986" -Direction Inbound -Protocol TCP -LocalPort 5986 -Action Allow
```


# ON Client

```
https://CLIENT01:5986/wsman/SubscriptionManager/WEC

Server=https://CLIENT01:5986/wsman/SubscriptionManager/WEC,Refresh=14400,IssuerCA=CE6E8D48E70FA5F901801CDACA0633D216CAB3BA

$caThumbprint = "CE6E8D48E70FA5F901801CDACA0633D216CAB3BA"

```
# Add CLIENT01 in the host

CLIENT01


<img width="1277" height="666" alt="image" src="https://github.com/user-attachments/assets/cd31cacb-a551-4140-8287-bc2d78c34371" />

<img width="1335" height="549" alt="image" src="https://github.com/user-attachments/assets/b4f45953-db06-427f-a385-4cedcf8fbf09" />


<img width="629" height="371" alt="image" src="https://github.com/user-attachments/assets/0d31d136-b3ee-4012-955d-e4a1fa42fb7a" />

<img width="800" height="216" alt="image" src="https://github.com/user-attachments/assets/9fe9117f-8c9d-42b5-8fb0-4123f7becc51" />

<img width="424" height="212" alt="image" src="https://github.com/user-attachments/assets/b347467d-02c4-4a08-ba15-29e3c0761c33" />


From Client
<img width="975" height="307" alt="image" src="https://github.com/user-attachments/assets/1b41525a-830f-4f7d-9ada-5fd53918f1db" />


<img width="1335" height="715" alt="image" src="https://github.com/user-attachments/assets/7317010f-2342-4dbc-ab3e-0a1deeace140" />



