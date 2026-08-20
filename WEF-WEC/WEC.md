how to send evenlogs to different windows machine 
- source initiated withot certificate
To send Windows Event Logs to a different machine without using certificates (source-initiated), you have two main options:

Option 1: WinRM + Wevtutil (HTTP, No Certificates)
This uses WinRM over HTTP (unencrypted) to pull logs from the source machine.

On the Target (Receiving) Machine:
powershell
# Enable WinRM and set up listener on HTTP
Enable-PSRemoting -Force
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'

# Create a firewall rule
New-NetFirewallRule -DisplayName "WinRM HTTP" -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow

# Set the source machine as trusted (for credential delegation)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "SOURCE_IP_OR_HOSTNAME" -Force
On the Source Machine:
powershell
# Configure WinRM client to trust the target
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "TARGET_IP_OR_HOSTNAME" -Force

# Send specific event logs (example: System log, last 100 events)
wevtutil qe System /c:100 /f:text /r:http://TARGET_IP:5985/wsman /u:DOMAIN\username /p:password

# Or send to a file on the target
wevtutil epl System \\TARGET_IP\C$\Logs\System.evtx
Option 2: Raw TCP with Logstash or NXLog (No Encryption)
This is the simplest approach—just send raw log data over TCP port.

Using NXLog (Recommended for event forwarding):
On the Source Machine (nxlog.conf):

apache
<Extension _syslog>
    Module      xm_syslog
</Extension>

<Input in>
    Module      im_msvistalog
    Query       *[System/Level=1 or System/Level=2 or System/Level=3]
    Exec        $EventTime = strftime($EventTime, '%Y-%m-%d %H:%M:%S');
</Input>

<Output out>
    Module      om_tcp
    Host        TARGET_IP
    Port        5140
    OutputType  LineBased
    Exec        $raw_event = $EventTime + " " + $SourceName + " " + $Message;
</Output>

<Route 1>
    Path        in => out
</Route>
On the Target Machine (Simple listener with Netcat or Python):

python
# listener.py
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 5140))
s.listen(5)
while True:
    conn, addr = s.accept()
    data = conn.recv(4096)
    with open('events.log', 'a') as f:
        f.write(data.decode() + '\n')
Option 3: Windows Event Forwarding (WEF) - No Certificate Workaround
Note: WEF normally requires certificates, but you can bypass this by setting the collector to accept anonymous or NTLM authentication:

On the Collector (Target):

powershell
# Set subscription to use NTLM instead of Kerberos
wecutil ss "SubscriptionName" /cm:"NTLM"

# Enable unencrypted HTTP
wecutil cs /http:yes
On the Source:

cmd
# Add the collector to trusted hosts
winrm set winrm/config/client @{TrustedHosts="COLLECTOR_IP"}

# Configure WinRM to allow unencrypted
winrm set winrm/config/service @{AllowUnencrypted="true"}
⚠️ Critical Security Warning
Do NOT use these methods in production without:

Placing both machines on an isolated management VLAN

Using IP whitelisting (firewall restrictions)

Implementing network-level encryption (VPN/IPsec)

Monitoring for unauthorized access

For production, you should:

Use certificates with Event Forwarding

Use HTTPS with WinRM (port 5986)

Use TLS with Syslog (via Logstash/rsyslog)

Quick Comparison Table
Method	Encryption	Ease	Reliability	Firewall Port
WinRM HTTP	None	Medium	Good	5985
NXLog TCP	None	High	Good	5140
WEF HTTP	None	Low	Excellent	5985
Which method would you prefer? If you need help configuring the TCP listener or NXLog properly, let me know and I'll provide the complete configuration.

This response is AI-generated, for reference only.
add to options wecutil subscrption in xml format
Here's how to create a WEC (Windows Event Collector) subscription using XML format with source-initiated mode and no certificates (using NTLM/HTTP):

WEC Subscription XML (Source-Initiated, No Certificates)
Step 1: Create the XML Subscription File
Save this as Subscription.xml:

xml
<Subscription xmlns="http://schemas.microsoft.com/2006/03/windows/eventlog/subscriptions">
    <SubscriptionId>SourceInitiated_NoCert</SubscriptionId>
    <SubscriptionType>SourceInitiated</SubscriptionType>
    <Description>Forwarded events from source machines - no certificate</Description>
    <Enabled>true</Enabled>
    <Uri>http://schemas.microsoft.com/wbem/wsman/1/windows/EventLog</Uri>
    <ConfigurationMode>Normal</ConfigurationMode>
    <Delivery Mode="Push">
        <Batching>
            <MaxLatency>30000</MaxLatency>  <!-- 30 seconds -->
            <MaxItems>5</MaxItems>
            <MaxSize>102400</MaxSize>
        </Batching>
        <Push>
            <HeartbeatInterval>60000</HeartbeatInterval>
        </Push>
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
                    <Select Path="Security">*[System[EventID=4624 or EventID=4625]]</Select>
                </Query>
            </QueryList>
        ]]>
    </Query>
    <ReadExistingEvents>false</ReadExistingEvents>
    <TransportName>HTTP</TransportName>  <!-- No SSL/HTTPS -->
    <TransportPort>5985</TransportPort>
    <ContentFormat>RenderedText</ContentFormat>
    <Locale>en-US</Locale>
    <LogFile>ForwardedEvents</LogFile>
    <PublisherType>NTLM</PublisherType>  <!-- No certificate, use NTLM -->
    <Credentials>
        <User>DOMAIN\WECUser</User>
        <Password>Password123</Password>
    </Credentials>
    <AllowedSourceNonDomainComputers>
        <Computer>SOURCE-PC-01</Computer>
        <Computer>SOURCE-PC-02</Computer>
        <Computer>192.168.1.100</Computer>
    </AllowedSourceNonDomainComputers>
    <AllowedSourceDomainComputers>false</AllowedSourceDomainComputers>
</Subscription>
Step 2: Apply the Subscription on the Collector (Target)
powershell
# On the WEC Collector machine:

# 1. Enable the Windows Event Collector service
wecutil cs

# 2. Import the XML subscription
wecutil sc "SourceInitiated_NoCert" /subscription:Subscription.xml

# 3. Verify the subscription
wecutil gs "SourceInitiated_NoCert"

# 4. Enable unencrypted HTTP on the collector
wecutil cs /http:yes
Step 3: Configure the Source Machines
On each source machine, run this PowerShell:

powershell
# 1. Configure WinRM client to trust the collector
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "COLLECTOR_IP" -Force

# 2. Allow unencrypted traffic
winrm set winrm/config/client @{AllowUnencrypted="true"}

# 3. Set the event forwarding policy
wevtutil set-log ForwardedEvents /enabled:true /retention:false /maxsize:1073741824

# 4. Restart Windows Event Log service
Restart-Service -Name "EventLog"

# 5. Force immediate connection to collector
wevtutil gp "ForwardedEvents" /r:"http://COLLECTOR_IP:5985/wsman" /u:"DOMAIN\WECUser" /p:"Password123"
Alternative: Simplified XML (Minimal Configuration)
If you want a simpler version with just the essentials:

xml
<Subscription xmlns="http://schemas.microsoft.com/2006/03/windows/eventlog/subscriptions">
    <SubscriptionId>Minimal_WEC</SubscriptionId>
    <SubscriptionType>SourceInitiated</SubscriptionType>
    <Enabled>true</Enabled>
    <Uri>http://schemas.microsoft.com/wbem/wsman/1/windows/EventLog</Uri>
    <Delivery Mode="Push">
        <Batching>
            <MaxLatency>60000</MaxLatency>
        </Batching>
    </Delivery>
    <Query>
        <![CDATA[
            <QueryList>
                <Query Id="0" Path="System">
                    <Select Path="System">*[System[(EventID=6005 or EventID=6006)]]</Select>
                </Query>
            </QueryList>
        ]]>
    </Query>
    <TransportName>HTTP</TransportName>
    <TransportPort>5985</TransportPort>
    <ContentFormat>RenderedText</ContentFormat>
    <LogFile>ForwardedEvents</LogFile>
    <PublisherType>NTLM</PublisherType>
    <AllowedSourceNonDomainComputers>
        <Computer>*.local</Computer>
    </AllowedSourceNonDomainComputers>
</Subscription>
Step 4: Check Subscription Status
powershell
# On collector - list all subscriptions
wecutil es

# Get detailed subscription status
wecutil gs "SourceInitiated_NoCert"

# Check if events are arriving
wevtutil qe ForwardedEvents /c:10 /f:text
Quick Command Reference
Action	Command
Create subscription	wecutil sc "Name" /subscription:file.xml
List subscriptions	wecutil es
Delete subscription	wecutil dc "Name"
Get subscription details	wecutil gs "Name"
Set collector config	wecutil cs /http:yes
Set retry interval	wecutil cs /r:60
⚠️ Security Implications
This configuration:

Transmits unencrypted event data (plain HTTP)

Sends credentials in clear text (NTLM over HTTP)

No certificate validation (HTTP, not HTTPS)

Recommendations for security:

Place both machines on an isolated VLAN

Use IPsec between the machines

Use a dedicated low-privilege service account

Monitor the ForwardedEvents log for anomalies

Consider using HTTPS with certificates for production

Do you want me to:

Add more event types to the XML query?

Show how to set up the NTLM credential configuration?

Provide the PowerShell script to deploy this to multiple source machines?

Show how to set up the NTLM credential configuration?
Here's how to properly set up NTLM credential configuration for source-initiated WEC subscriptions without certificates:

Complete NTLM Credential Setup for WEC
Step 1: Create a Dedicated Service Account
First, create a dedicated low-privilege account for event forwarding:

powershell
# On Domain Controller (if domain) or locally on collector:
New-ADUser -Name "WECService" -SamAccountName "WECService" -AccountPassword (ConvertTo-SecureString "YourSecurePassword123!" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true -Description "WEC Event Forwarding Service Account"

# Add to local "Event Log Readers" group on collector
Add-LocalGroupMember -Group "Event Log Readers" -Member "DOMAIN\WECService"

# OR on non-domain:
net user WECService "YourSecurePassword123!" /add /passwordchg:no /expires:never
net localgroup "Event Log Readers" WECService /add
Step 2: Configure Collector (Target) for NTLM Authentication
powershell
# On the WEC Collector machine:

# 1. Enable NTLM authentication for WinRM
winrm set winrm/config/service/auth '@{NTLM="true"}'

# 2. Set authentication level (optional - can be left default)
winrm set winrm/config/service '@{Negotiate="true"}'

# 3. Enable unencrypted HTTP (since we're not using certificates)
winrm set winrm/config/service '@{AllowUnencrypted="true"}'

# 4. Allow Basic authentication (fallback if NTLM fails)
winrm set winrm/config/service/auth '@{Basic="true"}'

# 5. Verify settings
winrm get winrm/config/service/auth
Step 3: Create XML Subscription with Explicit NTLM Credentials
Save this as WEC_NTLM_Subscription.xml:

xml
<?xml version="1.0" encoding="UTF-8"?>
<Subscription xmlns="http://schemas.microsoft.com/2006/03/windows/eventlog/subscriptions">
    <SubscriptionId>NTLM_Event_Forwarding</SubscriptionId>
    <SubscriptionType>SourceInitiated</SubscriptionType>
    <Description>Forwarded events using NTLM authentication (no certificates)</Description>
    <Enabled>true</Enabled>
    <Uri>http://schemas.microsoft.com/wbem/wsman/1/windows/EventLog</Uri>
    <ConfigurationMode>Normal</ConfigurationMode>
    <Delivery Mode="Push">
        <Batching>
            <MaxLatency>30000</MaxLatency>
            <MaxItems>10</MaxItems>
            <MaxSize>102400</MaxSize>
        </Batching>
        <Push>
            <HeartbeatInterval>60000</HeartbeatInterval>
        </Push>
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
            </QueryList>
        ]]>
    </Query>
    <ReadExistingEvents>false</ReadExistingEvents>
    <TransportName>HTTP</TransportName>
    <TransportPort>5985</TransportPort>
    <ContentFormat>RenderedText</ContentFormat>
    <Locale>en-US</Locale>
    <LogFile>ForwardedEvents</LogFile>
    
    <!-- CRITICAL: NTLM Authentication Configuration -->
    <PublisherType>NTLM</PublisherType>
    <Credentials>
        <User>DOMAIN\WECService</User>
        <Password>YourSecurePassword123!</Password>
    </Credentials>
    
    <!-- Allow specific source computers (can use wildcards) -->
    <AllowedSourceNonDomainComputers>
        <Computer>SOURCE-PC-01</Computer>
        <Computer>SOURCE-PC-02</Computer>
        <Computer>192.168.1.*</Computer>
        <Computer>*.corp.local</Computer>
    </AllowedSourceNonDomainComputers>
    <AllowedSourceDomainComputers>false</AllowedSourceDomainComputers>
</Subscription>
Step 4: Apply Subscription with NTLM Credentials
powershell
# On collector machine:

# 1. Import the XML subscription
wecutil sc "NTLM_Event_Forwarding" /subscription:WEC_NTLM_Subscription.xml

# 2. Force the subscription to use NTLM explicitly (in case XML wasn't enough)
wecutil ss "NTLM_Event_Forwarding" /cm:"NTLM"

# 3. Enable HTTP on the collector
wecutil cs /http:yes

# 4. Set collector to accept NTLM credentials
wecutil cs /n:1  # 1 = NTLM enabled

# 5. Verify subscription settings
wecutil gs "NTLM_Event_Forwarding"
Step 5: Configure Source Machines for NTLM Authentication
On each source machine, run this PowerShell script:

powershell
# SOURCE MACHINE CONFIGURATION

# Variables
$CollectorIP = "COLLECTOR_IP_ADDRESS"
$CollectorUser = "DOMAIN\WECService"
$CollectorPass = "YourSecurePassword123!"

# 1. Add collector to trusted hosts
Set-Item WSMan:\localhost\Client\TrustedHosts -Value $CollectorIP -Force

# 2. Enable NTLM and unencrypted traffic on client
winrm set winrm/config/client/auth '@{NTLM="true"}'
winrm set winrm/config/client '@{AllowUnencrypted="true"}'

# 3. Configure WinRM to use NTLM as preferred auth
winrm set winrm/config/client '@{Negotiate="true"}'

# 4. Create a credential object for testing
$cred = New-Object System.Management.Automation.PSCredential($CollectorUser, (ConvertTo-SecureString $CollectorPass -AsPlainText -Force))

# 5. Test connection to collector using NTLM
try {
    Test-WSMan -ComputerName $CollectorIP -Credential $cred -Authentication Negotiate
    Write-Host "NTLM connection successful!" -ForegroundColor Green
} catch {
    Write-Host "Connection failed: $_" -ForegroundColor Red
}

# 6. Force immediate event forwarding with NTLM
wevtutil gp "ForwardedEvents" /r:"http://$CollectorIP:5985/wsman" /u:"$CollectorUser" /p:"$CollectorPass"

# 7. Restart Event Log service
Restart-Service -Name "EventLog" -Force
Step 6: Automated NTLM Credential Deployment (Group Policy)
For domain environments, deploy via GPO:

Create a PowerShell script: Configure-WEC-NTLM.ps1

powershell
# Configure-WEC-NTLM.ps1

# Get collector from registry or parameter
$CollectorIP = "COLLECTOR_IP"
$CollectorUser = "DOMAIN\WECService"
$CollectorPass = "YourSecurePassword123!"

# Configure WinRM
Set-Item WSMan:\localhost\Client\TrustedHosts -Value $CollectorIP -Force
winrm set winrm/config/client/auth '@{NTLM="true"}'
winrm set winrm/config/client '@{AllowUnencrypted="true"}'

# Configure Event Forwarding
wevtutil set-log ForwardedEvents /enabled:true /retention:false /maxsize:1073741824

# Add subscription manually (if needed)
wevtutil gp "ForwardedEvents" /r:"http://$CollectorIP:5985/wsman" /u:"$CollectorUser" /p:"$CollectorPass"

# Restart services
Restart-Service -Name "EventLog" -Force
Deploy via GPO:

Create GPO → Computer Configuration → Windows Settings → Scripts → Startup

Add the PowerShell script

Link to OUs containing source machines

Step 7: Verify NTLM Authentication is Working
powershell
# On collector - check if events are arriving with proper credentials
wecutil gs "NTLM_Event_Forwarding" | findstr "Status"

# Check subscription health
wecutil gs "NTLM_Event_Forwarding" | findstr "Healthy"

# View events received
wevtutil qe ForwardedEvents /c:5 /f:text

# Check WinRM authentication logs
Get-WinEvent -LogName "Microsoft-Windows-WinRM/Operational" | Where-Object {$_.Message -match "NTLM"} | Select-Object -First 5
Step 8: Troubleshooting NTLM Credential Issues
If authentication fails, check these common issues:

powershell
# 1. Check if NTLM is blocked by security policy
Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System

# 2. Enable NTLM auditing
reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Audit /v NTLMAudit /t REG_DWORD /d 2 /f

# 3. Check event logs for auth failures
Get-WinEvent -LogName Security -MaxEvents 10 | Where-Object {$_.Id -in 4625,4776,4771}

# 4. Test NTLM connectivity directly
Test-NetConnection -ComputerName $CollectorIP -Port 5985

# 5. Reset WinRM if corrupted
winrm quickconfig -force
Security Best Practices for NTLM Credentials
powershell
# 1. Store password securely (using Windows Credential Manager)
cmdkey /add:"WECCollector" /user:"DOMAIN\WECService" /pass:"YourSecurePassword123!"

# Then use in scripts without hardcoding:
$cred = Get-Credential "DOMAIN\WECService"
# or
$cred = (Get-Credential "DOMAIN\WECService" -Message "Enter WEC credentials")

# 2. Use managed service accounts (gMSA) if possible
New-ADServiceAccount -Name "WECgMSA" -DNSHostName "wec.collector.local" -ServicePrincipalNames "HTTP/wec.collector.local"

# 3. Set password expiration (if not using gMSA)
Set-ADUser -Identity "WECService" -PasswordNeverExpires $false -AccountExpiration (Get-Date).AddYears(1)

# 4. Audit credential usage
Get-WinEvent -LogName Security -FilterXPath "*[System[EventID=4624 and EventData/Data[@Name='LogonType']='3']]" | Where-Object {$_.Properties[5].Value -eq "DOMAIN\WECService"}
Quick Reference: NTLM Configuration Parameters
Parameter	Value	Purpose
<PublisherType>	NTLM	Specifies NTLM authentication
<TransportName>	HTTP	Unencrypted transport (no cert)
<TransportPort>	5985	Default WinRM HTTP port
<Credentials>	User/Password	Service account credentials
winrm set /auth:NTLM	true	Enables NTLM on client/server
wecutil cs /n:1	1	Enables NTLM on collector
Do you need help with:

Setting up a gMSA instead of regular service account?

Encrypting the NTLM traffic using IPsec?

Deploying this to multiple source machines via Group Policy?

Monitoring the NTLM authentication logs?

