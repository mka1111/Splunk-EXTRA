1. Important naming decision

Before starting, make sure both machines can resolve the WEC name.

On WEF-Marcin, open an elevated CMD:

notepad C:\Windows\System32\drivers\etc\hosts

Add:

192.168.222.142    WEC-Marcin

On WEC-Marcin:

notepad C:\Windows\System32\drivers\etc\hosts

Add:

192.168.222.144    WEF-Marcin

Then test.

WEF-Marcin
ping WEC-Marcin
WEC-Marcin
ping WEF-Marcin

You should get the correct IP addresses.

The certificate names need to match the names used for the connection. Microsoft specifically requires the collector server certificate subject to match the collector FQDN and the source client certificate subject to match the source FQDN.

For a standalone lab, using the computer names consistently is practical.

2. Create the Root CA

We'll create the CA on:

WEC-Marcin — 192.168.222.142

Log into WEC-Marcin with an Administrator account.

Open PowerShell as Administrator.

Create a directory:

New-Item -Path C:\WEF-CA -ItemType Directory -Force

Create the Root CA:

$RootCA = New-SelfSignedCertificate `
    -Type Custom `
    -KeySpec Signature `
    -Subject "CN=Marcin-WEF-Root-CA" `
    -KeyExportPolicy Exportable `
    -KeyUsage CertSign, CRLSign, DigitalSignature `
    -KeyLength 4096 `
    -HashAlgorithm SHA256 `
    -NotAfter (Get-Date).AddYears(10) `
    -CertStoreLocation "Cert:\LocalMachine\My"

Check it:

$RootCA | Format-List Subject,Thumbprint,NotAfter

You should see something like:

Subject    : CN=Marcin-WEF-Root-CA
Thumbprint : ABC123...
NotAfter   : ...

Save the thumbprint.

3. Export the Root CA certificate

Still on WEC-Marcin:

Export-Certificate `
    -Cert $RootCA `
    -FilePath C:\WEF-CA\Marcin-WEF-Root-CA.cer

Check:

Get-ChildItem C:\WEF-CA

You should have:

C:\WEF-CA\Marcin-WEF-Root-CA.cer

You need to copy this .cer file to WEF-Marcin.

For example, using a shared folder or RDP clipboard.

4. Create the WEC HTTPS server certificate

Still on:

WEC-Marcin

We need a certificate with:

Server Authentication

and the correct computer name.

Run:

$WECServerCert = New-SelfSignedCertificate `
    -Type Custom `
    -Subject "CN=WEC-Marcin" `
    -DnsName "WEC-Marcin" `
    -Signer $RootCA `
    -KeyExportPolicy Exportable `
    -KeySpec Signature `
    -KeyLength 2048 `
    -HashAlgorithm SHA256 `
    -TextExtension @(
        "2.5.29.37={text}1.3.6.1.5.5.7.3.1"
    ) `
    -NotAfter (Get-Date).AddYears(3) `
    -CertStoreLocation "Cert:\LocalMachine\My"

The important EKU here is:

1.3.6.1.5.5.7.3.1

which is Server Authentication.

Verify:

$WECServerCert | Format-List Subject,DnsNameList,Thumbprint,NotAfter

Save the thumbprint:

$WECThumbprint = $WECServerCert.Thumbprint

$WECThumbprint

You will need it later.

Microsoft requires the collector to have a server-authentication certificate in the Local Computer → Personal store, with the subject matching the collector name.

5. Create the WEF client certificate

We need to issue another certificate from the same CA.

Still on:

WEC-Marcin

Run:

$WEFClientCert = New-SelfSignedCertificate `
    -Type Custom `
    -Subject "CN=WEF-Marcin" `
    -DnsName "WEF-Marcin" `
    -Signer $RootCA `
    -KeyExportPolicy Exportable `
    -KeySpec Signature `
    -KeyLength 2048 `
    -HashAlgorithm SHA256 `
    -TextExtension @(
        "2.5.29.37={text}1.3.6.1.5.5.7.3.2"
    ) `
    -NotAfter (Get-Date).AddYears(3) `
    -CertStoreLocation "Cert:\LocalMachine\My"

The important EKU is:

1.3.6.1.5.5.7.3.2

which is Client Authentication.

Check it:

$WEFClientCert | Format-List Subject,DnsNameList,Thumbprint,NotAfter
6. Export the WEF client certificate + private key

This is important.

The WEF computer needs the private key.

Create a password:

$Password = ConvertTo-SecureString `
    "ChangeThisPassword123!" `
    -AsPlainText `
    -Force

Export:

Export-PfxCertificate `
    -Cert $WEFClientCert `
    -FilePath C:\WEF-CA\WEF-Marcin-Client.pfx `
    -Password $Password

Check:

Get-ChildItem C:\WEF-CA

You should now have:

Marcin-WEF-Root-CA.cer
WEF-Marcin-Client.pfx

Copy both files to:

WEF-Marcin

7. Install the Root CA on WEF-Marcin

Now move to:

WEF-Marcin — 192.168.222.144

Open PowerShell as Administrator.

Assuming you copied the files to:

C:\WEF-CA\

Run:

Import-Certificate `
    -FilePath C:\WEF-CA\Marcin-WEF-Root-CA.cer `
    -CertStoreLocation Cert:\LocalMachine\Root

Verify:

Get-ChildItem Cert:\LocalMachine\Root |
    Where-Object {$_.Subject -eq "CN=Marcin-WEF-Root-CA"}

You should see the CA.

8. Install the WEF client certificate

Still on:

WEF-Marcin

$Password = ConvertTo-SecureString `
    "ChangeThisPassword123!" `
    -AsPlainText `
    -Force

Then:

Import-PfxCertificate `
    -FilePath C:\WEF-CA\WEF-Marcin-Client.pfx `
    -CertStoreLocation Cert:\LocalMachine\My `
    -Password $Password

Check:

Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.Subject -eq "CN=WEF-Marcin"} |
    Format-List Subject,Thumbprint,EnhancedKeyUsageList,HasPrivateKey

You want:

Subject            : CN=WEF-Marcin
HasPrivateKey      : True

and Client Authentication in the EKU.

9. Give NETWORK SERVICE access to the WEF certificate private key

This is an important step that is easy to miss.

Microsoft specifically requires the NETWORK SERVICE account to have read access to the private key of the client certificate.

Find the certificate:

$cert = Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.Subject -eq "CN=WEF-Marcin"}

Display it:

$cert

Get the certificate key container:

$cert.PrivateKey.CspKeyContainerInfo.UniqueKeyContainerName

Then you can grant access through:

certlm.msc

Go to:

Certificates
  → Personal
    → Certificates

Find:

WEF-Marcin

Right-click:

All Tasks
→ Manage Private Keys

Add:

NETWORK SERVICE

Grant:

Read
10. Configure WinRM on WEF-Marcin

Still on:

WEF-Marcin

Open elevated CMD:

winrm quickconfig -q

Check:

winrm get winrm/config

You should have WinRM running.

Check service:

sc query WinRM

You want:

STATE : 4 RUNNING

Microsoft requires WinRM to be configured on the source computer for this scenario.

11. Configure WEC-Marcin

Move to:

WEC-Marcin — 192.168.222.142

Open elevated CMD:

winrm quickconfig -q

Then:

wecutil qc /q

Check:

sc query Wecsvc

You want:

STATE : 4 RUNNING

wecutil qc configures the Windows Event Collector service, including enabling the ForwardedEvents channel and ensuring the collector service starts appropriately.

12. Enable certificate authentication on WEC

On:

WEC-Marcin

Run:

winrm set winrm/config/service/auth "@{Certificate=\"true\"}"

Verify:

winrm get winrm/config/service/auth

You should see:

Certificate = true

Microsoft explicitly requires certificate authentication to be enabled for this non-domain HTTPS configuration.

13. Create the WinRM HTTPS listener

First find the WEC server certificate:

Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.Subject -eq "CN=WEC-Marcin"} |
    Format-List Subject,Thumbprint,EnhancedKeyUsageList,HasPrivateKey

Copy the thumbprint.

For example:

ABCDEF1234567890...

Remove spaces if necessary.

Then:

winrm delete winrm/config/Listener?Address=*+Transport=HTTPS

If there isn't an existing HTTPS listener, an error here is not necessarily a problem.

Now create it:

winrm create winrm/config/Listener?Address=*+Transport=HTTPS "@{Hostname=\"WEC-Marcin\";CertificateThumbprint=\"YOUR_WEC_CERT_THUMBPRINT\"}"

Replace:

YOUR_WEC_CERT_THUMBPRINT

with the actual thumbprint.

Check:

winrm enumerate winrm/config/listener

You should see:

Transport = HTTPS
Port = 5986
Hostname = WEC-Marcin
CertificateThumbprint = ...

Microsoft documents exactly this HTTPS listener approach using the server certificate thumbprint.

14. Open TCP 5986 firewall

On:

WEC-Marcin

I recommend using the modern Windows Firewall cmdlet:

New-NetFirewallRule `
    -DisplayName "WEF WinRM HTTPS 5986" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 5986 `
    -Action Allow `
    -Profile Any

Verify:

Get-NetFirewallRule -DisplayName "WEF WinRM HTTPS 5986"

Microsoft's WEF documentation specifies TCP 5986 for the HTTPS configuration.

15. Test TCP connectivity from WEF

Move to:

WEF-Marcin

Run:

Test-NetConnection WEC-Marcin -Port 5986

You want:

ComputerName     : WEC-Marcin
RemotePort       : 5986
TcpTestSucceeded : True

If this says:

False

stop here.

Do not continue until TCP 5986 works.

16. Create certificate mapping on WEC

This is the most important certificate-authentication step.

On:

WEC-Marcin

First make sure the Root CA is trusted.

Get-ChildItem Cert:\LocalMachine\Root |
    Where-Object {$_.Subject -eq "CN=Marcin-WEF-Root-CA"} |
    Format-List Subject,Thumbprint

Copy the Root CA thumbprint.

For example:

112233445566...

Now create a local user.

net user WEF-CertAuth "VeryStrongPassword123!" /add

Add it to Administrators:

net localgroup Administrators WEF-CertAuth /add

Important: Microsoft notes that this local account is used for the certificate mapping mechanism; for the Event Forwarding scenario the account isn't used to impersonate the forwarding connection and can be deleted afterward if it isn't needed for another certificate-authentication scenario.

Now create the certificate mapping.

Replace the CA thumbprint:

winrm create winrm/config/service/certmapping?Issuer=YOUR_ROOT_CA_THUMBPRINT+Subject=*+URI=* "@{UserName=\"WEF-CertAuth\";Password=\"VeryStrongPassword123!\"}" -remote:localhost

For example:

winrm create winrm/config/service/certmapping?Issuer=11223344556677889900AABBCCDDEEFF+Subject=*+URI=* "@{UserName=\"WEF-CertAuth\";Password=\"VeryStrongPassword123!\"}" -remote:localhost

Then verify:

winrm enumerate winrm/config/service/certmapping

You should see the mapping.

Microsoft documents this CA-based certificate mapping for standalone/non-domain WEF and specifically uses the issuing CA thumbprint.

17. Test certificate authentication BEFORE configuring WEF

This is extremely important.

Don't create the WEF subscription yet.

First prove:

WEF-Marcin
      |
      | Client certificate
      |
      | HTTPS 5986
      v
WEC-Marcin
      |
      v
WinRM certificate authentication

On:

WEF-Marcin

Find the client certificate:

Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.Subject -eq "CN=WEF-Marcin"} |
    Format-List Subject,Thumbprint

Copy the thumbprint.

Then:

winrm get winrm/config -r:https://WEC-Marcin:5986 -a:certificate -certificate:YOUR_WEF_CLIENT_CERT_THUMBPRINT

Replace the thumbprint.

If successful, you should receive the WEC WinRM configuration.

Microsoft explicitly recommends this test and says not to proceed if the configuration isn't returned.

18. Configure the WEF source to use HTTPS

Now go back to:

WEF-Marcin

Run:

gpedit.msc

Go to:

Computer Configuration
  → Administrative Templates
    → Windows Components
      → Event Forwarding

Find:

Configure the server address, refresh interval,
and issuer certificate authority of a target Subscription Manager

Set:

Enabled

Click:

Show...

Add:

Server=HTTPS://WEC-Marcin:5986/wsman/SubscriptionManager/WEC,Refresh=10,IssuerCA=YOUR_ROOT_CA_THUMBPRINT

For example:

Server=HTTPS://WEC-Marcin:5986/wsman/SubscriptionManager/WEC,Refresh=10,IssuerCA=11223344556677889900AABBCCDDEEFF

Microsoft documents this exact Server=HTTPS://...:5986/wsman/SubscriptionManager/WEC,Refresh=...,IssuerCA=... format.

Then:

gpupdate /force
19. Configure the WEC subscription

Go to:

WEC-Marcin

Run:

eventvwr.msc

Go to:

Applications and Services Logs

Actually, for subscriptions, open:

Event Viewer
   → Subscriptions

Click:

Create Subscription...

Choose:

Destination Log:
ForwardedEvents

Give it a name:

WEF-Marcin-Security

Select:

Source computer initiated

Then:

Select Computer Groups...

Select:

Add Non-Domain Computers...

Enter:

WEF-Marcin

Then click:

Add Certificates...

Add:

Marcin-WEF-Root-CA

This is important: you're telling WEC to trust client certificates issued by your CA.

Microsoft's standalone configuration specifically requires adding the non-domain source and the CA that issued the source's client certificate.

20. Configure the events

For the first test, don't start with everything.

Select:

Select Events...

Start with:

Windows Logs
→ System

For example:

Event level:
Information
Warning
Error
Critical

Or use a small test filter.

Once it works, create a separate subscription for:

Security
System
Application
Microsoft-Windows-PowerShell/Operational
Microsoft-Windows-Sysmon/Operational

etc.

21. Select HTTPS

In the subscription:

Advanced...

Select:

Protocol:
HTTPS

Choose:

Normal

for your initial test.

Click:

OK

Microsoft explicitly instructs selecting HTTPS under the subscription's Advanced settings for this configuration.

22. Check WEF-Marcin

On:

WEF-Marcin

Open:

eventvwr.msc

Go to:

Applications and Services Logs
    Microsoft
       Windows
          Eventlog-ForwardingPlugin
             Operational

Look for:

Event ID 104

Microsoft identifies Event ID 104 as the successful connection to the Subscription Manager.

Also look for:

Event ID 100

indicating the subscription was created successfully.

23. Check WEC-Marcin

On:

WEC-Marcin

Open:

eventvwr.msc

Check:

Forwarded Events

You should eventually see events coming from:

WEF-Marcin

You can also check the subscription from CMD:

wecutil gr WEF-Marcin-Security

And:

wecutil gs WEF-Marcin-Security

Microsoft specifically recommends wecutil gr for runtime status and wecutil gs for subscription configuration.

24. Generate a test event

On:

WEF-Marcin

Run PowerShell:

Write-EventLog `
    -LogName Application `
    -Source "Windows PowerShell" `
    -EventId 1000 `
    -EntryType Information `
    -Message "WEF HTTPS TEST - WEF-Marcin"

If the source doesn't have that event source registered, use:

New-EventLog -LogName Application -Source "WEF-Test"

Then:

Write-EventLog `
    -LogName Application `
    -Source "WEF-Test" `
    -EventId 1000 `
    -EntryType Information `
    -Message "WEF HTTPS TEST - WEF-Marcin"

Then check on:

WEC-Marcin

Event Viewer
→ Forwarded Events

You should see:

WEF HTTPS TEST - WEF-Marcin
25. Useful troubleshooting commands
WEF-Marcin

Check WinRM:

winrm get winrm/config

Check WEF subscription manager:

reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\EventLog\EventForwarding" /s

Check client certificate:

Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.Subject -eq "CN=WEF-Marcin"} |
    Format-List Subject,Issuer,Thumbprint,HasPrivateKey,EnhancedKeyUsageList

Test port:

Test-NetConnection WEC-Marcin -Port 5986

Test HTTPS WinRM:

winrm get winrm/config -r:https://WEC-Marcin:5986 -a:certificate -certificate:CLIENT_CERT_THUMBPRINT

Check WEF events:

Applications and Services Logs
→ Microsoft
→ Windows
→ Eventlog-ForwardingPlugin
→ Operational
WEC-Marcin

Check listener:

winrm enumerate winrm/config/listener

Check certificate authentication:

winrm get winrm/config/service/auth

Check certificate mappings:

winrm enumerate winrm/config/service/certmapping

Check WEC:

wecutil qc /q

Check subscription:

wecutil gs WEF-Marcin-Security

Check runtime:

wecutil gr WEF-Marcin-Security

Check HTTPS port:

Get-NetTCPConnection -LocalPort 5986 -State Listen

Check firewall:

Get-NetFirewallRule -DisplayName "WEF WinRM HTTPS 5986"
The final architecture

When everything is configured correctly, you should have:

                  192.168.222.144
                    WEF-Marcin
                 Standalone/Workgroup
                       |
                       |
             Client Authentication
             WEF-Marcin certificate
                       |
                       |
                  HTTPS / 5986
                       |
                       v
                  192.168.222.142
                    WEC-Marcin
                 Standalone/Workgroup
                       |
             Server Authentication
             WEC-Marcin certificate
                       |
                       v
                ForwardedEvents

The critical certificates are:

Machine	Certificate	EKU	Store
WEC-Marcin	WEC-Marcin	Server Authentication	LocalMachine\My
WEF-Marcin	WEF-Marcin	Client Authentication	LocalMachine\My
Both	Marcin-WEF-Root-CA	CA	LocalMachine\Root

And the critical network connection is:

WEF-Marcin  →  WEC-Marcin:5986/TCP
One correction to be aware of

Don't use a certificate that is merely a generic self-signed certificate. WinRM HTTPS requires an appropriate server-authentication certificate whose name matches the collector, and WEF's standalone certificate-authentication configuration requires the source to have a client-authentication certificate.

If you follow the sequence above, test each layer before moving to the next:

1. Name resolution
       ↓
2. Certificates
       ↓
3. WinRM
       ↓
4. HTTPS listener
       ↓
5. TCP 5986
       ↓
6. Certificate mapping
       ↓
7. winrm -a:certificate test
       ↓
8. Subscription Manager
       ↓
9. WEC subscription
       ↓
10. Test event

That approach makes it much easier to identify exactly where the configuration fails.





-----------------------------
---------------------------


Run this on whichever machine you're on now (looks like the one that generated the certs — confirm which one this is):

powershell
Write-Host "--- WEF-Marcin cert issuer ---" -ForegroundColor Cyan
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEF-Marcin"} | Format-List Subject, Thumbprint, Issuer

Write-Host "--- WEC-Marcin cert issuer ---" -ForegroundColor Cyan
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=WEC-Marcin"} | Format-List Subject, Thumbprint, Issuer

Issuer won't show the thumbprint directly (just the CN), so also run this to map subject → thumbprint for both CA copies, so we can match them up:

powershell
Get-ChildItem Cert:\LocalMachine\My | Where-Object {$_.Subject -eq "CN=Marcin-WEF-Root-CA"} | Format-List Subject, Thumbprint, NotBefore, HasPrivateKey

The NotBefore timestamps will tell us which one is older/newer, and HasPrivateKey will tell us which one can still sign anything if we need to reissue.

My strong recommendation given the confusion: rather than untangle which duplicate signed what, it's cleaner to delete both root CA copies and every leaf cert, and regenerate everything from scratch in one clean pass on a single machine, since we know that process works — we've just had thumbprint bookkeeping errors, not a fundamental design problem. That avoids any chance of the two servers ending up trusting different CAs.

Do you want to go that route (full clean regeneration), or would you prefer to first identify which CA copy is the "real" one and just clean up the stray duplicate? Either works, but a clean regeneration removes all ambiguity going forward.
