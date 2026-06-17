Ref:
https://www.youtube.com/watch?v=foYJB1UEcjQ

```

{
  "RawData": "INFO Linux log sample"
}

```















Example logs 

```
Jul 24 08:12:45 web01 sshd[2145]: Failed password for invalid user test from 192.168.1.50 port 51234 ssh2

Jul 24 08:15:03 web01 sshd[2151]: Accepted publickey for ubuntu from 10.10.20.15 port 53321 ssh2: RSA SHA256:AbCdEfGhIjKlMnOpQrStUvWxYz1234567890

Jul 24 09:01:17 web02 sudo[3201]: alice : TTY=pts/0 ; PWD=/home/alice ; USER=root ; COMMAND=/usr/bin/systemctl restart nginx

Jul 24 09:15:42 web02 systemd[1]: Started Nginx HTTP and reverse proxy server.

Jul 24 10:22:58 db01 kernel: Out of memory: Killed process 8421 (java) total-vm:4194304kB, anon-rss:2048000kB

Jul 24 10:45:13 db01 CRON[4218]: (root) CMD (/usr/local/bin/backup.sh)

Jul 24 11:08:26 app01 nginx[5512]: 192.168.10.25 - - [24/Jul/2026:11:08:26 +0000] "GET /login HTTP/1.1" 200 1543 "-" "Mozilla/5.0"

Jul 24 11:27:44 app01 sshd[5621]: Connection closed by authenticating user admin 172.16.5.10 port 60123 [preauth]

Jul 24 12:14:31 mail01 postfix/smtpd[7823]: connect from unknown[203.0.113.45]

Jul 24 12:15:02 mail01 postfix/smtpd[7823]: disconnect from unknown[203.0.113.45] ehlo=1 mail=1 rcpt=1 data=1 quit=1 commands=5
```
