https://www.youtube.com/watch?v=4GSLfxEgQwE


https://github.com/olafhartong/TA-Sysmon-deploy/blob/master/bin/update.bat


<img width="907" height="493" alt="image" src="https://github.com/user-attachments/assets/bdb51c65-7584-4088-87bd-e9acd34dafd1" />



<img width="321" height="107" alt="image" src="https://github.com/user-attachments/assets/993354b0-58e1-4c33-9233-ad07849ae036" />

<img width="224" height="62" alt="image" src="https://github.com/user-attachments/assets/0e992f54-2f52-4619-aed5-70c986d4da51" />






xml file
https://github.com/swiftonsecurity/sysmon-config

https://github.com/olafhartong/sysmon-modular/blob/master/sysmonconfig.xml

# installing sysmon service 

<img width="477" height="66" alt="image" src="https://github.com/user-attachments/assets/3e9c80f0-dc84-4f97-8e8c-de39cbd5b6af" />

<img width="469" height="101" alt="image" src="https://github.com/user-attachments/assets/c469cdcb-e4bf-4d4e-9871-16a670c09202" />


```
.\Sysmon64.exe -accepteula -i sysmonconfig.xml



# Stop the Sysmon driver
Stop-Service -Name Sysmon

# Start the Sysmon driver
Start-Service -Name Sysmon

# Verify status
Get-Service -Name Sysmon

# Alternative using sc.exe
sc.exe stop Sysmon
sc.exe start Sysmon

:: Stop and start Splunk Forwarder service
net stop SplunkForwarder
net start SplunkForwarder

:: Or restart with a single command (not available in CMD)
:: Alternative - restart through SC
sc stop SplunkForwarder
sc start SplunkForwarder

:: Check service status
sc query SplunkForwarder


# Simple restart command
Restart-Service -Name SplunkForwarder

# Alternative with detailed output
Stop-Service -Name SplunkForwarder -Force
Start-Service -Name SplunkForwarder

# Check status
Get-Service -Name SplunkForwarder

# Restart and wait for completion
Restart-Service -Name SplunkForwarder -PassThru | Wait-ForStatus -Timeout 60


```


```
[WinEventLog://Microsoft-Windows-Sysmon/Operational]
disabled = 0
index = main
renderXml = true
sourcetype = XmlWinEventLog:Microsoft-Windows-Sysmon/Operational
```



<img width="897" height="99" alt="image" src="https://github.com/user-attachments/assets/dad6791e-7fff-4122-ba68-0136a7723b3d" />

<img width="1185" height="547" alt="image" src="https://github.com/user-attachments/assets/3520db56-43a4-495b-b02b-418c2c5d788e" />

<img width="1035" height="466" alt="image" src="https://github.com/user-attachments/assets/affa7488-f83f-437c-abc1-9bd2ff474efa" />


<img width="921" height="338" alt="image" src="https://github.com/user-attachments/assets/207b84d2-c4ea-4430-8408-7da9f2333047" />
