Deep

Ref:
https://www.youtube.com/watch?v=KJbIH7egdVI&t=1s
https://rogierdijkman.medium.com/log-rotation-for-syslog-cef-collector-servers-5ec6ba27b7f6

<img width="692" height="790" alt="image" src="https://github.com/user-attachments/assets/e34483d8-6a61-4784-a19a-6ee519d49d27" />






IyBNb2R1bGUgbG9hZGluZwptb2R1bGUobG9hZD0iaW11eHNvY2siKSAgICAjIGxvY2FsIHN5c3RlbSBsb2dnaW5nCm1vZHVsZShsb2FkPSJpbWtsb2ciKSAgICAgICMga2VybmVsIGxvZ2dpbmcKCm1vZHVsZShsb2FkPSJpbXVkcCIpCmlucHV0KHR5cGU9ImltdWRwIiBwb3J0PSIxNTE0IikKCm1vZHVsZShsb2FkPSJpbXRjcCIpCgppbnB1dCh0eXBlPSJpbXRjcCIgcG9ydD0iMTUxNCIpCgoKIyBHbG9iYWwgZGlyZWN0aXZlcwokQWN0aW9uRmlsZURlZmF1bHRUZW1wbGF0ZSBSU1lTTE9HX1RyYWRpdGlvbmFsRmlsZUZvcm1hdAokUmVwZWF0ZWRNc2dSZWR1Y3Rpb24gb2ZmCgoKJEZpbGVPd25lciBzeXNsb2cKJEZpbGVHcm91cCBhZG0KJEZpbGVDcmVhdGVNb2RlIDA2NDAKJERpckNyZWF0ZU1vZGUgMDc1NQokVW1hc2sgMDAyMgokUHJpdkRyb3BUb1VzZXIgc3lzbG9nCiRQcml2RHJvcFRvR3JvdXAgc3lzbG9nCgoKJFdvcmtEaXJlY3RvcnkgL3Zhci9zcG9vbC9yc3lzbG9nCgokdGVtcGxhdGUgUGVySG9zdExvZ1NwbHVuaywgIi9zcGx1bmsvJUZST01IT1NULUlQJS5sb2ciCgoKcnVsZXNldChuYW1lPSJQZXJIb3N0TG9nU3BsdW5rWCIpIHsKICAgIGFjdGlvbigKICAgICAgICB0eXBlPSJvbWZ3ZCIKICAgICAgICB0YXJnZXQ9IjE5Mi4xNjguMS44NCIKICAgICAgICBwb3J0PSI5OTk5IgogICAgICAgIHByb3RvY29sPSJ0Y3AiCiAgICApCn0KCgoKCgojIGlmICRmcm9taG9zdC1pcCA9PSAnMTkyLjE2OC4xLjg0J3RoZW4gLT9QZXJIb3N0TG9nU3BsdW5rCgojIGlmICgkZnJvbWhvc3QtaXAgPT0gIjE5Mi4xNjguMS44NCIgYW5kICRtc2cgY29udGFpbnMgImdvb2QiICApIHRoZW4gYWN0aW9uKAppZiAoJGZyb21ob3N0LWlwID09ICIxOTIuMTY4LjEuODQiICApIHRoZW4gYWN0aW9uKAogICAgICAgIHR5cGU9Im9tZndkIgogICAgICAgIHRhcmdldD0iMTkyLjE2OC4xLjg0IgogICAgICAgIHBvcnQ9Ijk5OTkiCiAgICAgICAgcHJvdG9jb2w9InRjcCIKICAgICkKCiYgfgoKCgoKIyBVc2UgdHJhZGl0aW9uYWwgdGltZXN0YW1wIGZvcm1hdAokQWN0aW9uRmlsZURlZmF1bHRUZW1wbGF0ZSBSU1lTTE9HX1RyYWRpdGlvbmFsRmlsZUZvcm1hdAoKIyBJbmNsdWRlIGNvbmZpZyBzbmlwcGV0cwokSW5jbHVkZUNvbmZpZyAvZXRjL3JzeXNsb2cuZC8qLmNvbmYKCiMgTG9nIGFsbCBtZXNzYWdlcyB0byBtYWluIGxvZyBmaWxlCiouaW5mbzttYWlsLm5vbmU7YXV0aHByaXYubm9uZTtjcm9uLm5vbmUgICAgL3Zhci9sb2cvbWVzc2FnZXMKCiMgQXV0aGVudGljYXRpb24gbG9ncwphdXRocHJpdi4qICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC92YXIvbG9nL3NlY3VyZQoKIyBNYWlsIGxvZ3MKbWFpbC4qICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAvdmFyL2xvZy9tYWlsbG9nCgojIENyb24gbG9ncwpjcm9uLiogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC92YXIvbG9nL2Nyb24KCiMgRW1lcmdlbmN5IG1lc3NhZ2VzIHRvIGFsbCB1c2VycwoqLmVtZXJnICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDpvbXVzcm1zZzoqCgojIFNhdmUgYm9vdCBtZXNzYWdlcyB0byBib290LmxvZwpsb2NhbDcuKiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC92YXIvbG9nL2Jvb3QubG9nCgoKCgoKCgojIFNlbmQgbG9ncyB0byByZW1vdGUgc2VydmVyIChvcHRpb25hbCAtIHVuY29tbWVudCB0byBlbmFibGUpCiMgKi4qIEBAcmVtb3RlLWhvc3Q6NTE0ICAgICAgICAgICAjIFRDUAojICouKiBAcmVtb3RlLWhvc3Q6NTE0ICAgICAgICAgICAgIyBVRFAK






# if $fromhost-ip == '192.168.1.84'then -?PerHostLogSplunk








ruleset(name="PerHostLogSplunkX") {
action(
type="omfwd"
target="192.168.1.84"
port="9999"
protocol="tcp"
)
}


















<img width="1141" height="558" alt="image" src="https://github.com/user-attachments/assets/646c6b2a-9372-4f4b-9758-7e432526b99b" />



***  Rotation of the logs is controlled by configuration files that reside in the /etc/logrotate.d  ***

example

# /etc/logrotate.d/rsyslog
/var/log/syslog
/var/log/messages
/var/log/secure
{
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    postrotate
        # Standardowy reload rsyslog po rotacji [citation:8][citation:10]
        /usr/bin/systemctl kill -s HUP rsyslog.service 2>/dev/null || true
    endscript
}




=================

# /opt/splunkforwarder/etc/system/local/inputs.conf
[monitor:///var/log/syslog]
index = main
sourcetype = syslog
disabled = false
initCrcLength = 1024
crcSalt = syslog_salt
blacklist = \.gz$|\.1$|\.2$










Poniżej przedstawiam kompletną konfigurację `logrotate` dla logów zbieranych przez Splunk Universal Forwarder (UF), wraz z wyjaśnieniem, jak uniknąć najczęstszych problemów.

## 🎯 Kluczowe wyzwanie: Splunk i rotacja logów

Splunk używa CRC (Cyclic Redundancy Check) do śledzenia, które fragmenty plików już przetworzył . Domyślnie sprawdzane jest tylko pierwsze 256 bajtów pliku.

**Problem**: Po rotacji plik logu zmienia nazwę (np. `app.log` → `app.log.1`), a nowy pusty plik `app.log` ma identyczne pierwsze 256 bajtów (np. nagłówek). Splunk może to uznać za **zupełnie nowy plik** i **ponownie zaindeksować wszystkie dane** .

**Rozwiązanie**: Prawidłowa konfiguracja `logrotate` + odpowiednie ustawienia w Splunku.

---

## 📝 Przykład 1: Logrotate.conf dla logów monitorowanych przez Splunk

```bash
# /etc/logrotate.d/splunk-monitored-logs

# Przykład dla logów aplikacji (np. Tomcat, Java, Python)
/var/log/myapp/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 splunk splunk
    
    # KLUCZOWE: Nie używaj copytruncate z logami, które kończą się na .gz!
    # Splunk może ponownie przeczytać skompresowany plik po rotacji
    
    postrotate
        # Opcjonalnie: przeładuj aplikację (np. Tomcat)
        # systemctl reload myapp
        
        # UWAGA: Nie restartuj Splunk Forwardera tutaj
        echo "Logs rotated at $(date)" >> /var/log/logrotate.status
    endscript
}

# Przykład dla logów systemowych (/var/log/messages, /var/log/secure)
/var/log/messages
/var/log/secure
/var/log/maillog
/var/log/cron
{
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    
    postrotate
        # Sygnał USR1 dla rsyslog/syslog-ng (standardowa praktyka)
        /bin/kill -HUP $(cat /var/run/syslogd.pid 2>/dev/null) 2>/dev/null || true
        /bin/kill -HUP $(cat /var/run/rsyslogd.pid 2>/dev/null) 2>/dev/null || true
    endscript
}
```

---

## 🔧 Przykład 2: Konfiguracja Splunk inputs.conf (bez pieczenia)

Kluczowe ustawienie w Splunku, które zapobiega ponownemu indeksowaniu po rotacji:

```bash
# /opt/splunkforwarder/etc/system/local/inputs.conf
# lub /opt/splunkforwarder/etc/apps/<app_name>/local/inputs.conf

# Monitorowanie logów aplikacji
[monitor:///var/log/myapp/*.log]
index = main
sourcetype = myapp_logs
disabled = false

# KLUCZOWE 1: Zwiększ długość CRC, aby uniknąć kolizji
initCrcLength = 1024

# KLUCZOWE 2: Dodaj "sól" do CRC, ale BEZ <SOURCE> (unikaj duplikacji!)
# UWAGA: crcSalt = <SOURCE> JEST ZABRONIONE dla logów z rotacją!
# Spowoduje ponowne indeksowanie po każdej zmianie nazwy pliku 
crcSalt = myapp_unique_salt

# Monitorowanie logów systemowych
[monitor:///var/log/messages]
index = os
sourcetype = linux_messages
disabled = false
initCrcLength = 1024
crcSalt = messages_salt

[monitor:///var/log/secure]
index = os
sourcetype = linux_secure
disabled = false
initCrcLength = 1024
crcSalt = secure_salt
```

### 🚨 WAŻNE: Ostrzeżenie od Splunk

> **Nie używaj `crcSalt = <SOURCE>` z logami, które są regularnie rotowane** (lub zmieniają nazwę/miejsce). To uniemożliwi Splunkowi rozpoznanie plików po rotacji i spowoduje podwójne indeksowanie danych .

---

## 📋 Przykład 3: Blacklista dla skompresowanych logów

Jeśli twoje logi są archiwizowane (`.gz`), skonfiguruj blacklistę w Splunku:

```bash
# /opt/splunkforwarder/etc/system/local/inputs.conf

[monitor:///var/log/myapp]
index = main
sourcetype = myapp_logs
disabled = false

# Wyklucz już skompresowane pliki (zapobiega ponownemu czytaniu)
blacklist = \.gz$|\.zip$|\.bz2$

# Wyklucz również pliki z numerami rotacji (opcjonalnie)
# blacklist = \.\d+$|\.gz$
```

**Dlaczego?** Splunk może rozpoznać skompresowany plik jako nowy i spróbować go przeczytać, co spowoduje duplikację danych .

---

## 🩺 Przykład 4: Scenariusz z rsyslog + Splunk

Częsty wzorzec: `rsyslog` zapisuje logi → `logrotate` rotuje → `Splunk` monitoruje:

```bash
# /etc/logrotate.d/rsyslog
/var/log/syslog
/var/log/messages
/var/log/secure
{
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    postrotate
        # Standardowy reload rsyslog po rotacji 
        /usr/bin/systemctl kill -s HUP rsyslog.service 2>/dev/null || true
    endscript
}
```

```bash
# /opt/splunkforwarder/etc/system/local/inputs.conf
[monitor:///var/log/syslog]
index = main
sourcetype = syslog
disabled = false
initCrcLength = 1024
crcSalt = syslog_salt
blacklist = \.gz$|\.1$|\.2$
```

---

## 🚨 Typowy problem i rozwiązanie: Splunk trzyma uchwyty do usuniętych plików

**Objaw**: Mimo działania `logrotate`, miejsce na dysku nie zwalnia się .

**Przyczyna**: Proces `splunkd` (Splunk Forwarder) trzyma otwarte deskryptory do plików, które zostały już usunięte podczas rotacji.

**Diagnoza**:
```bash
# Sprawdź, czy Splunk trzyma usunięte pliki
lsof | grep deleted | grep splunk

# Oblicz rozmiar zajmowany przez "usunięte" pliki
lsof | grep deleted | grep splunk | awk '{sum += $7} END {print sum/1024/1024 " MB"}'
```

**Rozwiązanie** (wykonaj poza godzinami szczytu):
```bash
# Restart Splunk Forwardera 
systemctl restart splunkforwarder
# lub
/opt/splunkforwarder/bin/splunk restart
```

**Efekt**: Restart uwalnia deskryptory, a system operacyjny rzeczywiście usuwa pliki, zwalniając miejsce .

---

## 📊 Testowanie konfiguracji

```bash
# 1. Sprawdź składnię logrotate
sudo logrotate -d /etc/logrotate.d/splunk-monitored-logs

# 2. Wymuś rotację (debug)
sudo logrotate -vf /etc/logrotate.d/splunk-monitored-logs

# 3. Sprawdź, czy Splunk nadal monitoruje poprawne pliki
ls -la /var/log/myapp/
tail -f /var/log/myapp/app.log

# 4. Monitoruj logi Splunka
tail -f /opt/splunkforwarder/var/log/splunk/splunkd.log | grep -i "crc\|rotate"
```

---

## ✅ Podsumowanie najlepszych praktyk

| Co robić ✅ | Czego unikać ❌ |
|------------|----------------|
| Używaj `delaycompress` w `logrotate` | Nie używaj `copytruncate` (chyba że konieczne) |
| Skonfiguruj `initCrcLength = 1024` w Splunku | Unikaj `crcSalt = <SOURCE>` dla rotowanych logów |
| Dodaj `blacklist = \.gz$` w `inputs.conf` | Nie restartuj Splunka w `postrotate` (chyba że trzeba) |
| Regularnie restartuj Splunk Forwarder (off-peak) | Nie ignoruj problemu "deleted files held open" |
| Testuj konfigurację przed wdrożeniem | Nie mieszaj różnych metod rotacji dla tych samych plików |

Dzięki tej konfiguracji Splunk nie będzie ponownie indeksował danych po rotacji, a logi będą bezpiecznie rotowane bez utraty miejsca na dysku.





<img width="742" height="314" alt="image" src="https://github.com/user-attachments/assets/badad746-7ac8-4f9d-a284-00d960aae1c0" />


# Save everything from port into file 

```


module(load="imtcp")         # TCP receiver
module(load="imudp")         # UDP receiver
input(type="imtcp" port="2514" ruleset="security_ruleset")
input(type="imudp" port="2514" ruleset="security_ruleset")

$FileOwner root
$FileGroup root
$FileCreateMode 0640
$DirCreateMode 0755
$Umask 0022
$WorkDirectory /var/spool/rsyslog
$IncludeConfig /etc/rsyslog.d/*.conf


ruleset(name="security_ruleset"){
action(type="omfile" file="/var/log/xxx.log")

}







ruleset(name="security_ruleset"){
action(type="omfwd"
               target="192.168.1.19"
               port="9999"
               protocol="tcp" )



 

   }

ruleset(name="security_ruleset"){
action(type="omfile" file="/var/log/aaa.log")

}

```


# easy Command

```
echo "Test message on port UDP 2514" | nc  -u 127.0.0.1  2514 -w0
```


# Read file and send to specific ip and port


```
module(load="imfile")  # Load the module to read text files

# Define the input for reading /var/log/mail
input(type="imfile"
      File="/var/log/mail"            # Path to the file to monitor
      Tag="mail-log:"                 # Tag added to messages from this file
      StateFile="state-mail-log"      # File to track the read position
      Facility="mail"                 # Assign the 'mail' facility
      Severity="info")                # Assign severity level

# Define the forwarding action to send logs to the remote server
# This rule will apply to all messages processed by rsyslog.
action(type="omfwd"
       protocol="udp"                 # Use UDP for non-blocking, lower overhead
       target="192.168.131.135"       # Remote server's IP address
       port="514"                     # Destination port
       queue.type="linkedList"        # Recommended for network forwarding, prevents blocking[citation:5][citation:6]
       queue.size="10000")            # Max number of messages to queue

```

