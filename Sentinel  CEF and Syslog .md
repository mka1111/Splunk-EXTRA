https://www.youtube.com/watch?v=bHw8BkEpYzs


Ingesting Syslog and CEF 
https://www.youtube.com/watch?v=BLqNvaF5nXg&t=2376s

## Search to see all logs

<img width="669" height="468" alt="image" src="https://github.com/user-attachments/assets/1834fe29-1b20-4873-878e-cff4fc388032" />


<img width="1190" height="319" alt="image" src="https://github.com/user-attachments/assets/4e914671-819b-4cc0-8c64-1866150d6315" />




Place where DCR is created on linux device. 
<img width="980" height="162" alt="image" src="https://github.com/user-attachments/assets/67db3ed4-fa8e-40be-88b8-2500d5c07a45" />



for CEF 
whe you install you need to run the command that can be found


# All steps 

<img width="1236" height="718" alt="image" src="https://github.com/user-attachments/assets/401c4006-dc77-4a2c-8b57-5a2902245223" />










<img width="1185" height="671" alt="image" src="https://github.com/user-attachments/assets/35dcb7e2-30a4-4a3f-95f8-075d02a6d307" />


<img width="509" height="110" alt="image" src="https://github.com/user-attachments/assets/af66a0d1-b24b-489e-aa61-51bcb54e0aff" />


<img width="1242" height="446" alt="image" src="https://github.com/user-attachments/assets/b014ba4c-5857-4e09-80ee-709598f6ae83" />


nost likly rsyslog will be broken after script

<img width="989" height="443" alt="image" src="https://github.com/user-attachments/assets/ca479d2e-47c0-4f89-87a1-c83bba7442e8" />

## to fix the issue you need to 
<img width="1323" height="188" alt="image" src="https://github.com/user-attachments/assets/07f9f6e8-35c7-403e-96fb-36f79861fa6b" />




<img width="1247" height="581" alt="image" src="https://github.com/user-attachments/assets/3bf19df7-ff7b-4aaa-919b-67071f68c397" />




<img width="1153" height="173" alt="image" src="https://github.com/user-attachments/assets/488e0473-2892-4698-8347-62af3d929739" />



<img width="1413" height="788" alt="image" src="https://github.com/user-attachments/assets/d5221a66-c5df-4891-9f8e-67f7325e1a4b" />


<img width="872" height="330" alt="image" src="https://github.com/user-attachments/assets/d3a97268-23db-4f7b-ae3d-2d7fef06e8e5" />




# Syslog vs CEF

<img width="1569" height="833" alt="image" src="https://github.com/user-attachments/assets/f34611e7-ce4a-4fac-8c88-025078dc62f6" />





## To test
<img width="1450" height="146" alt="image" src="https://github.com/user-attachments/assets/381406ee-4b39-405a-aafb-e83ce2bf6fe0" />


<img width="1562" height="841" alt="image" src="https://github.com/user-attachments/assets/d71ff4bf-4edf-43c9-97e8-a4ca3e4c0b9c" />

1. CEF (10 examples)
logger 'CEF:0|Cisco|ASA|9.18|1001|Connection Built|3|src=192.168.1.10 dst=8.8.8.8 spt=52344 dpt=53 proto=UDP act=allow'

logger 'CEF:0|Palo Alto|NGFW|11.1|1002|URL Filtering Block|7|src=10.1.1.25 dst=104.26.1.1 request=https://malicious.example act=blocked'

logger 'CEF:0|Microsoft|Defender|2025|1003|Malware Detected|9|dhost=PC01 fileName=invoice.exe fileHash=abcd1234567890 act=quarantine'

logger 'CEF:0|CrowdStrike|Falcon|7.5|1004|Credential Dumping|10|dhost=SERVER01 suser=administrator act=blocked'

logger 'CEF:0|Fortinet|FortiGate|7.4|1005|VPN Login Success|2|src=203.0.113.5 suser=alice outcome=Success'

logger 'CEF:0|Linux|sshd|9.7|1006|SSH Failed Login|5|src=198.51.100.10 suser=root msg=Failed password'

logger 'CEF:0|Apache|ModSecurity|3.0|1007|XSS Attempt|8|src=45.10.10.5 request=/search?q=<script> act=blocked'

logger 'CEF:0|Suricata|IDS|7.0|1008|ET Malware Activity|9|src=172.16.1.20 dst=91.189.91.20 proto=TCP act=alert'

logger 'CEF:0|Okta|Identity|2025|1009|MFA Failure|6|src=192.0.2.20 suser=jdoe outcome=Failure'

logger 'CEF:0|VMware|ESXi|8.0|1010|Host Configuration Changed|4|dhost=esxi01 suser=root msg=Firewall rules modified'
2. NetFlow-like text logs (10 examples)

These are not real NetFlow packets, but many SIEM parsers use similar text for testing.

logger 'NETFLOW src=192.168.1.10 dst=8.8.8.8 sport=52344 dport=53 proto=UDP packets=2 bytes=180 duration=1'

logger 'NETFLOW src=10.0.0.15 dst=172.217.20.14 sport=50122 dport=443 proto=TCP packets=18 bytes=14560 duration=12'

logger 'NETFLOW src=192.168.100.5 dst=192.168.100.1 sport=5353 dport=5353 proto=UDP packets=4 bytes=720 duration=2'

logger 'NETFLOW src=172.16.10.25 dst=13.107.42.16 sport=62015 dport=443 proto=TCP packets=45 bytes=56000 duration=25'

logger 'NETFLOW src=192.168.0.12 dst=185.199.108.153 sport=51000 dport=443 proto=TCP packets=11 bytes=9500 duration=8'

logger 'NETFLOW src=10.1.1.44 dst=10.1.1.1 sport=49152 dport=22 proto=TCP packets=25 bytes=1800 duration=45'

logger 'NETFLOW src=192.168.2.15 dst=224.0.0.251 sport=5353 dport=5353 proto=UDP packets=5 bytes=980 duration=3'

logger 'NETFLOW src=172.20.1.100 dst=52.96.12.5 sport=60001 dport=443 proto=TCP packets=89 bytes=124000 duration=62'

logger 'NETFLOW src=192.168.50.7 dst=1.1.1.1 sport=60222 dport=53 proto=UDP packets=1 bytes=90 duration=1'

logger 'NETFLOW src=10.10.10.50 dst=203.0.113.50 sport=33455 dport=80 proto=TCP packets=120 bytes=98000 duration=120'
3. Traditional Syslog (RFC3164 style)
logger 'Jul 19 12:01:15 web01 sshd[1234]: Accepted password for admin from 192.168.1.20 port 52112 ssh2'

logger 'Jul 19 12:02:01 firewall kernel: IN=eth0 OUT= MAC= SRC=10.1.1.10 DST=8.8.8.8 LEN=60 PROTO=TCP SPT=50000 DPT=443'

logger 'Jul 19 12:03:55 apache httpd[2211]: GET /index.html 200'

logger 'Jul 19 12:05:01 postfix/smtpd[5432]: connect from mail.example.com[203.0.113.22]'

logger 'Jul 19 12:06:18 sudo: john : TTY=pts/0 ; PWD=/home/john ; COMMAND=/usr/bin/systemctl restart nginx'

logger 'Jul 19 12:07:10 kernel: CPU temperature above threshold'

logger 'Jul 19 12:08:25 systemd[1]: Started Docker Application Container Engine.'

logger 'Jul 19 12:09:14 named[998]: client 192.168.1.10#44221: query: example.com IN A +'

logger 'Jul 19 12:10:33 CRON[7777]: (root) CMD (/usr/local/bin/backup.sh)'

logger 'Jul 19 12:11:42 NetworkManager[888]: device eth0 successfully activated'
Real NetFlow generation






