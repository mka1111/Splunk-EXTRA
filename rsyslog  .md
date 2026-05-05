Deep

Ref:
https://www.youtube.com/watch?v=KJbIH7egdVI&t=1s
https://rogierdijkman.medium.com/log-rotation-for-syslog-cef-collector-servers-5ec6ba27b7f6



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
