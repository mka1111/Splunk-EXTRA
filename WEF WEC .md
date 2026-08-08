


# Generate logs
## dffsd
### sss




### Start Event logs

```
wevtutil gl security
```



### Hostname

```
C:\Windows\System32\Drivers\etc\
```
- example
- 192.168.1.100   www.mydomain.local


### update xxxxx

```
gpupdate /force 
```

### WINRM

```
 winrm quickconfig
```
```
 winrm qc -q
```
```
Enable-PSRemoting -Force

```


Delete winrm https
```
netsh http delete urlacl url=http://+:5985/wsman/
```
Test 
Test-WSMan -ComputerName 172.31.24.110 -Port 5985

Enable-PSRemoting -Force



REM Create the registry key
REG ADD "HKLM\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager" /f

REM Add the subscription as a multi-string value
REG ADD "HKLM\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager" /v "1" /t REG_MULTI_SZ /d "Server=http://172.31.24.110:5985/wsman/SubscriptionManager/WEC,Refresh=60" /f





Tet-Item WSMan:\localhost\Client\TrustedHosts -Value "172.31.24.110" -Force

netsh http add urlacl url=http://+:5985/wsman/ sddl=D:(A;;GX;;;S-1-5-80-569256582-2953403351-2909559716-1301513147-412116970)(A;;GX;;;S-1-5-80-4059739203-877974739-1245631912-527174227-2996563517)




### Create EventLogs


eventcreate /id 999 /t error /l application /d "This is a test event for WEF."


Write-EventLog -LogName Security -Source "Microsoft-Windows-Security-Auditing" -EventId 4740 -EntryType Failure -Message @'









Certificate Architecture Overview
WEC Server: Needs SSL/Server Authentication certificate for HTTPS listener

WEF Server: Needs Client Authentication certificate for identity

Both must trust each other's certificates

COMPLETE SETUP - EXECUTE IN THIS ORDER
PHASE 1: On WEC Server (Collector)
Step 1.1 - Create Server Authentication Certificate
powershell
# Create certificate for HTTPS listener (Server Authentication)
$wecCert = New-SelfSignedCertificate `
    -DnsName "WEC-Server", "WEC-Server.domain.com", "192.168.1.100" `
    -CertStoreLocation "Cert:\LocalMachine\My" `
    -KeyUsage KeyEncipherment, DigitalSignature `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1") `
    -NotAfter (Get-Date).AddYears(10)

# Note the thumbprint for later
$wecCert.Thumbprint | Out-File "C:\Certs\WEC-Thumbprint.txt"
Write-Host "WEC Certificate Thumbprint: $($wecCert.Thumbprint)"
Step 1.2 - Export WEC Certificate for WEF Server
powershell
# Create directory for certificates
New-Item -Path "C:\Certs" -ItemType Directory -Force

# Export public certificate (for WEF to trust)
Export-Certificate `
    -Cert $wecCert `
    -FilePath "C:\Certs\WEC-Server-Public.cer" `
    -Type CERT

# Export full certificate with private key (BACKUP ONLY - keep secure)
$password = ConvertTo-SecureString -String "StrongP@ssw0rd123" -Force -AsPlainText
Export-PfxCertificate `
    -Cert $wecCert `
    -FilePath "C:\Certs\WEC-Server-Backup.pfx" `
    -Password $password
Step 1.3 - Configure WinRM HTTPS Listener
powershell
# Enable PSRemoting if not already done
Enable-PSRemoting -Force

# Delete any existing HTTPS listeners
Get-ChildItem -Path WSMan:\localhost\Listener\*\* | Where-Object {$_.Keys -contains "Transport=HTTPS"} | Remove-Item -Recurse

# Create HTTPS listener with certificate
New-WSManInstance `
    -ResourceURI winrm/config/Listener `
    -SelectorSet @{Address="*";Transport="HTTPS"} `
    -ValueSet @{Hostname="WEC-Server";CertificateThumbprint=$wecCert.Thumbprint}
Step 1.4 - Configure WinRM Service Authentication
powershell
# Enable certificate authentication on WinRM service
Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $true

# Enable client certificate mapping
Set-Item -Path WSMan:\localhost\Service\EnableCompatibilityHttpsListener -Value $true
Step 1.5 - Configure Firewall Rules
powershell
# Allow WinRM HTTPS (port 5986)
New-NetFirewallRule `
    -DisplayName "WinRM HTTPS" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 5986 `
    -Action Allow `
    -Profile Domain,Private,Public
Step 1.6 - Enable Event Collector Service
powershell
# Configure Event Collector
wecutil qc
PHASE 2: On WEF Server (Forwarder)
Step 2.1 - Create Client Authentication Certificate
powershell
# Create directory for certificates
New-Item -Path "C:\Certs" -ItemType Directory -Force

# Create certificate for client authentication
$wefCert = New-SelfSignedCertificate `
    -DnsName "WEF-Server", "WEF-Server.domain.com" `
    -CertStoreLocation "Cert:\LocalMachine\My" `
    -KeyUsage DigitalSignature, KeyEncipherment `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2") `
    -NotAfter (Get-Date).AddYears(10)

# Note the thumbprint
$wefCert.Thumbprint | Out-File "C:\Certs\WEF-Thumbprint.txt"
Write-Host "WEF Certificate Thumbprint: $($wefCert.Thumbprint)"
Step 2.2 - Export WEF Certificate for WEC Server
powershell
# Export public certificate (to be trusted by WEC)
Export-Certificate `
    -Cert $wefCert `
    -FilePath "C:\Certs\WEF-Client-Public.cer" `
    -Type CERT

# Export full certificate with private key (BACKUP ONLY)
$password = ConvertTo-SecureString -String "StrongP@ssw0rd456" -Force -AsPlainText
Export-PfxCertificate `
    -Cert $wefCert `
    -FilePath "C:\Certs\WEF-Client-Backup.pfx" `
    -Password $password
Step 2.3 - Copy Certificates from WEC to WEF
powershell
# Copy WEC public cert from WEC server to WEF server first
# Then import it to Trusted Root Certification Authorities
Import-Certificate `
    -FilePath "C:\Certs\WEC-Server-Public.cer" `
    -CertStoreLocation "Cert:\LocalMachine\Root"
PHASE 3: Back to WEC Server
Step 3.1 - Copy WEF Certificate from WEF to WEC
powershell
# Copy WEF public cert from WEF server to WEC server first
# Then import it to Trusted People store
Import-Certificate `
    -FilePath "C:\Certs\WEF-Client-Public.cer" `
    -CertStoreLocation "Cert:\LocalMachine\TrustedPeople"
Step 3.2 - Create Local User for Certificate Mapping
powershell
# Create a local user that WEF will map to
$username = "WEF-Server$"
$password = ConvertTo-SecureString "ComplexP@ssw0rd789!" -AsPlainText -Force

New-LocalUser `
    -Name $username `
    -Password $password `
    -PasswordNeverExpires `
    -AccountNeverExpires

# Add to Event Log Readers group
Add-LocalGroupMember -Group "Event Log Readers" -Member $username
Step 3.3 - Configure Certificate to User Mapping
powershell
# Get the WEF client certificate details
$wefClientCert = Get-ChildItem -Path Cert:\LocalMachine\TrustedPeople | `
    Where-Object {$_.Subject -like "*WEF-Server*"}

# Create credential object for the local user
$cred = New-Object System.Management.Automation.PSCredential(
    "WEC-Server\$username", 
    $password
)

# Create the certificate mapping in WinRM
New-Item -Path WSMan:\localhost\ClientCertificate `
    -Subject "$($wefClientCert.Subject)" `
    -Issuer "$($wefClientCert.Issuer)" `
    -Credential $cred `
    -Force
Step 3.4 - Create Event Subscription
powershell
# Create subscription XML
$subscriptionXML = @"
<?xml version="1.0" encoding="UTF-8"?>
<Subscription xmlns="http://schemas.microsoft.com/2006/03/windows/events/subscription">
    <SubscriptionId>WEF-Server-System-Logs</SubscriptionId>
    <SubscriptionType>SourceInitiated</SubscriptionType>
    <Description>Collect System logs from WEF Server</Description>
    <Enabled>true</Enabled>
    <Uri>https://WEC-Server:5986/wsman/SubscriptionManager/WEC</Uri>
    <ConfigurationMode>Custom</ConfigurationMode>
    <Delivery Mode="Push">
        <Batching>
            <MaxLatencyTime>900000</MaxLatencyTime>
            <MaxItems>100</MaxItems>
        </Batching>
        <PushSettings>
            <Heartbeat Interval="900000"/>
        </PushSettings>
    </Delivery>
    <Query>
        <![CDATA[
            <QueryList>
                <Query Id="0" Path="System">
                    <Select Path="System">*[System[(Level=1 or Level=2 or Level=3)]]</Select>
                </Query>
                <Query Id="1" Path="Application">
                    <Select Path="Application">*[System[(Level=1 or Level=2 or Level=3)]]</Select>
                </Query>
                <Query Id="2" Path="Security">
                    <Select Path="Security">*</Select>
                </Query>
            </QueryList>
        ]]>
    </Query>
</Subscription>
"@

# Save subscription XML
$subscriptionXML | Out-File -FilePath "C:\Certs\Subscription.xml" -Encoding UTF8

# Create the subscription
wecutil cs "C:\Certs\Subscription.xml"
PHASE 4: Back to WEF Server
Step 4.1 - Configure WinRM Client
powershell
# Enable certificate authentication on WinRM client
Set-Item -Path WSMan:\localhost\Client\Auth\Certificate -Value $true

# Add WEC server to trusted hosts
Set-Item -Path WSMan:\localhost\Client\TrustedHosts -Value "WEC-Server" -Force

# Configure client certificate for WEC server
Set-Item -Path WSMan:\localhost\ClientCertificate\TrustedHosts `
    -Value "WEC-Server" `
    -Force
Step 4.2 - Configure Event Forwarding
powershell
# Enable event forwarding
wecutil qc

# Create source-initiated subscription to WEC
$subscriptionXML = @"
<?xml version="1.0" encoding="UTF-8"?>
<Subscription xmlns="http://schemas.microsoft.com/2006/03/windows/events/subscription">
    <SubscriptionId>Forward-to-WEC</SubscriptionId>
    <SubscriptionType>SourceInitiated</SubscriptionType>
    <Description>Forward events to WEC Server</Description>
    <Enabled>true</Enabled>
    <Uri>https://WEC-Server:5986/wsman/SubscriptionManager/WEC</Uri>
    <ConfigurationMode>Custom</ConfigurationMode>
    <Delivery Mode="Push">
        <Batching>
            <MaxLatencyTime>900000</MaxLatencyTime>
            <MaxItems>100</MaxItems>
        </Batching>
        <PushSettings>
            <Heartbeat Interval="900000"/>
        </PushSettings>
    </Delivery>
    <Query>
        <![CDATA[
            <QueryList>
                <Query Id="0" Path="System">
                    <Select Path="System">*[System[(Level=1 or Level=2 or Level=3)]]</Select>
                </Query>
                <Query Id="1" Path="Application">
                    <Select Path="Application">*[System[(Level=1 or Level=2 or Level=3)]]</Select>
                </Query>
                <Query Id="2" Path="Security">
                    <Select Path="Security">*</Select>
                </Query>
            </QueryList>
        ]]>
    </Query>
</Subscription>
"@

$subscriptionXML | Out-File -FilePath "C:\Certs\WEF-Subscription.xml" -Encoding UTF8
wecutil cs "C:\Certs\WEF-Subscription.xml"
Step 4.3 - Restart WinRM Service
powershell
Restart-Service WinRM -Force
VERIFICATION COMMANDS
On WEC Server:
powershell
# Check HTTPS listener
winrm enumerate winrm/config/listener

# Verify certificate mapping
Get-ChildItem -Path WSMan:\localhost\ClientCertificate

# Check subscription status
wecutil gr "WEF-Server-System-Logs"

# View forwarded events
Get-WinEvent -LogName "ForwardedEvents" -MaxEvents 10

# Check event forwarding log
Get-WinEvent -LogName "Microsoft-Windows-Eventlog-ForwardingPlugin/Operational" -MaxEvents 20
On WEF Server:
powershell
# Test connection to WEC
Test-WSMan -ComputerName WEC-Server -UseSSL -Authentication Certificate

# Check subscription runtime status
wecutil gr "Forward-to-WEC"

# Check WinRM configuration
winrm get winrm/config/client

# Verify certificates
Get-ChildItem -Path Cert:\LocalMachine\My | Format-List Subject, Thumbprint, EnhancedKeyUsageList

# Check event forwarding operational log
Get-WinEvent -LogName "Microsoft-Windows-Eventlog-ForwardingPlugin/Operational" -MaxEvents 20 | Format-List
