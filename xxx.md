Here's the full setup for forwarding events from WEF-Marcin (192.168.222.144) to WEC-Marcin (192.168.222.142) using a source-initiated subscription over HTTPS (the standard, scalable approach).

1. Hosts file entries (name resolution)

Run as Administrator on each box (skip if you already have DNS resolving these names).

On WEC-Marcin:

powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "192.168.222.144`tWEF-Marcin"

On WEF-Marcin:

powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "192.168.222.142`tWEC-Marcin"

Verify:

powershell
Resolve-DnsName WEC-Marcin
Resolve-DnsName WEF-Marcin
2. Base WinRM/WEC services

On WEC-Marcin (collector):

powershell
winrm quickconfig -q
wecutil qc /q

On WEF-Marcin (forwarder):

powershell
winrm quickconfig -q

This also grants the local NETWORK SERVICE account rights it needs to read most event logs. If you're forwarding a non-standard log (e.g., a custom app log), grant read access explicitly:

powershell
wevtutil gl Security
wevtutil sl <LogName> /ca:"O:BAG:SYD:(A;;0x1;;;NS)"
3. Certificate for the HTTPS listener

HTTPS requires a server certificate on the collector (WEC-Marcin). Use your internal CA if you have one — the cert's Subject/SAN must match WEC-Marcin. For a lab/test cert:

powershell
$cert = New-SelfSignedCertificate -DnsName "WEC-Marcin" `
  -CertStoreLocation "Cert:\LocalMachine\My" `
  -KeyUsage DigitalSignature,KeyEncipherment `
  -Type SSLServerAuthentication
$cert.Thumbprint

Export it and import the public cert into WEF-Marcin's Trusted Root (or intermediate) store so it trusts the listener:

powershell
# On WEC-Marcin: export public cert
Export-Certificate -Cert $cert -FilePath C:\wec-marcin.cer

# Copy wec-marcin.cer to WEF-Marcin, then on WEF-Marcin:
Import-Certificate -FilePath C:\wec-marcin.cer -CertStoreLocation Cert:\LocalMachine\Root
4. Create the HTTPS listener on WEC-Marcin
powershell
winrm create winrm/config/Listener?Address=*+Transport=HTTPS `
  '@{Hostname="WEC-Marcin";CertificateThumbprint="<PASTE_THUMBPRINT>"}'

Verify:

powershell
winrm enumerate winrm/config/Listener
5. Open the firewall

On WEC-Marcin (inbound 5986):

powershell
New-NetFirewallRule -DisplayName "WinRM HTTPS-In" -Direction Inbound -Protocol TCP -LocalPort 5986 -Action Allow

On WEF-Marcin (outbound 5986, usually allowed by default, but to be explicit):

powershell
New-NetFirewallRule -DisplayName "WinRM HTTPS-Out" -Direction Outbound -Protocol TCP -RemotePort 5986 -Action Allow
6. Point WEF-Marcin at the collector (SubscriptionManager)

This tells the forwarder where to push events. If domain-joined, GPO is the normal path (Computer Configuration → Administrative Templates → Windows Components → Event Forwarding → Configure target Subscription Manager), but the direct registry/command equivalent is:

cmd
wecutil qc /q
cmd
reg add "HKLM\Software\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager" /v 1 /t REG_SZ /d "Server=https://WEC-Marcin:5986/wsman/SubscriptionManager/WEC,Refresh=60" /f

Then restart the Windows Event Log/Remote Management services on WEF-Marcin so it picks up the config:

powershell
Restart-Service Winmgmt -Force
Restart-Service WinRM
gpupdate /force   # only if using GPO instead of the reg add above
7. Authentication note (domain vs. workgroup)
Domain-joined: Negotiate/Kerberos auth works over the HTTPS transport as-is — the cert above only provides TLS encryption. No further auth setup needed.
Workgroup/non-domain: Kerberos isn't available, so you need certificate-based mutual auth instead — issue a client cert to WEF-Marcin, import its public cert on WEC-Marcin, and map it to a local account permitted to read/write the subscription (winrm/config/service/certmapping on the collector). Let me know if this is your setup and I'll give the exact mapping commands.
8. Create the subscription on WEC-Marcin

Create subscription.xml:

xml
<Subscription xmlns="http://schemas.microsoft.com/2006/03/windows/events/subscription">
  <SubscriptionId>WEF-Marcin-Subscription</SubscriptionId>
  <SubscriptionType>SourceInitiated</SubscriptionType>
  <Description>Events forwarded from WEF-Marcin</Description>
  <Enabled>true</Enabled>
  <Uri>http://schemas.microsoft.com/wbem/wsman/1/windows/EventLog</Uri>
  <ConfigurationMode>Normal</ConfigurationMode>
  <Delivery Mode="Push">
    <Batching>
      <MaxLatencyTime>60000</MaxLatencyTime>
    </Batching>
    <PushSettings>
      <Heartbeat Interval="60000"/>
    </PushSettings>
  </Delivery>
  <Query>
    <![CDATA[
      <QueryList>
        <Query Id="0" Path="Security">
          <Select Path="Security">*</Select>
        </Query>
      </QueryList>
    ]]>
  </Query>
  <ReadExistingEvents>false</ReadExistingEvents>
  <TransportName>HTTPS</TransportName>
  <ContentFormat>RenderedText</ContentFormat>
  <Locale Language="en-US"/>
  <LogFile>ForwardedEvents</LogFile>
  <AllowedSourceNonDomainComputers></AllowedSourceNonDomainComputers>
  <AllowedSourceDomainComputers>O:NSG:NSD:(A;;GA;;;DC)(A;;GA;;;NS)</AllowedSourceDomainComputers>
</Subscription>

Import it:

powershell
wecutil cs subscription.xml
9. Verify

On WEC-Marcin:

powershell
wecutil es                      # lists subscriptions
wecutil gr WEF-Marcin-Subscription   # shows runtime status/last error per source
Get-WinEvent -LogName ForwardedEvents -MaxEvents 10

On WEF-Marcin, check the forwarding plugin operational log:

powershell
Get-WinEvent -LogName "Microsoft-Windows-Forwarding/Operational" -MaxEvents 20

Let me know whether these machines are domain-joined or a workgroup — that changes step 7 (auth), and I can give the exact certificate-mapping commands if it's a workgroup setup.
