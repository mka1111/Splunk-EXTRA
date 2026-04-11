
Max Partition 32

Retention znaczy ze jak nie ma polaczenia to w tym czasie dane bede trzymane w event hub. 


# Apps
## Splunk Add on for Microsoft Azure
<img width="792" height="738" alt="image" src="https://github.com/user-attachments/assets/b0380ce1-f81a-40cc-8a2a-fe75f6bea045" />


## Splunk Add-on for Microsoft Cloud Services
<img width="917" height="669" alt="image" src="https://github.com/user-attachments/assets/a3538a39-9394-4b16-8c1a-30a546875d0c" />



<img width="1247" height="677" alt="image" src="https://github.com/user-attachments/assets/1c424a92-12a8-41fb-ad72-339e186889a4" />


<img width="1384" height="791" alt="image" src="https://github.com/user-attachments/assets/c67fa635-b86f-49f8-b1fd-3b9a3439d30d" />


<img width="1420" height="794" alt="image" src="https://github.com/user-attachments/assets/3afad4b0-f7c8-4c0c-a51f-84e7ffb1b674" />


<img width="1338" height="754" alt="image" src="https://github.com/user-attachments/assets/016ab770-8b74-496c-84fc-14507537232d" />


<img width="601" height="305" alt="image" src="https://github.com/user-attachments/assets/cab5ddf2-c907-4880-b0ea-d785ffc7fde5" />




# 1 Crate EventHub namespace
<img width="998" height="671" alt="image" src="https://github.com/user-attachments/assets/82dcefc1-4b2f-4f1f-8b4b-68b5318e8833" />

# 2 Create Event Hub
<img width="850" height="442" alt="image" src="https://github.com/user-attachments/assets/d59c352a-cc1c-4d60-ae56-b86604c8a67b" />
# 3 You cann create Consumer Group

<img width="1170" height="434" alt="image" src="https://github.com/user-attachments/assets/ab5ecea7-3790-477a-841d-c23d946a8d45" />

# 4 Add Shared Access Policy
<img width="1444" height="440" alt="image" src="https://github.com/user-attachments/assets/f151e812-5911-4656-9820-307e721c8d1f" />

# 5 Create App with API permission

<img width="1177" height="306" alt="image" src="https://github.com/user-attachments/assets/c4875405-ea53-44e8-80a9-b1f528bd0f7d" />

<img width="1423" height="574" alt="image" src="https://github.com/user-attachments/assets/30e220e8-d404-4e93-8219-54680cad5752" />




<img width="1417" height="566" alt="image" src="https://github.com/user-attachments/assets/d387eb10-5b4e-400f-9d6f-d3777d00d308" />













Logs can be taken from 
Subscription

<img width="1132" height="668" alt="image" src="https://github.com/user-attachments/assets/52fb235a-51ed-4afb-8de8-dd39bfca3500" />

Entra ID


Monitor 





Notes from GTP

<img width="527" height="126" alt="image" src="https://github.com/user-attachments/assets/5f872953-06b6-4610-bbd6-8b6f589b5e30" />

<img width="566" height="274" alt="image" src="https://github.com/user-attachments/assets/4f0c75e7-34ad-45bc-88b4-400d5aee835f" />

<img width="511" height="291" alt="image" src="https://github.com/user-attachments/assets/464a5bdb-ac96-47b6-b301-edcebbcbd28f" />

<img width="888" height="377" alt="image" src="https://github.com/user-attachments/assets/9b17756f-161c-48ab-8ab5-495fc6477daf" />

<img width="939" height="415" alt="image" src="https://github.com/user-attachments/assets/d9ddc0b9-08ab-4b74-b923-69cf5f5b7065" />

<img width="961" height="433" alt="image" src="https://github.com/user-attachments/assets/a31229cc-1724-409e-ae69-7e92747c0740" />

<img width="796" height="235" alt="image" src="https://github.com/user-attachments/assets/56f8cb92-65f4-41b1-bf63-8f5da70ff25e" />

<img width="847" height="271" alt="image" src="https://github.com/user-attachments/assets/265a2b92-d92f-4567-abef-648dd431a74b" />

<img width="918" height="345" alt="image" src="https://github.com/user-attachments/assets/0738337d-a411-41d3-992d-de74b4d6aad6" />

<img width="932" height="297" alt="image" src="https://github.com/user-attachments/assets/24dcaf02-a153-4a0b-b5ee-fc199e617a01" />


<img width="888" height="354" alt="image" src="https://github.com/user-attachments/assets/6043bdfc-667d-40e7-8576-615ba73b17f7" />

<img width="843" height="256" alt="image" src="https://github.com/user-attachments/assets/429fa760-d136-4c01-8f88-8d4b1583dc58" />


Recommended (real-world SOC) Enable: 

SignInLogs 
AuditLogs 
NonInteractiveUserSignInLogs 
ServicePrincipalSignInLogs



<img width="832" height="414" alt="image" src="https://github.com/user-attachments/assets/b4a39582-f638-47db-bf60-403de69585e8" />

https://docs.fortinet.com/document/forticnapp/latest/lacework-forticnapp-policies/948338/lacework-global-1018?utm_source=chatgpt.com
Remediation
Using the Azure console:

Go to Microsoft Entra ID.

Under Monitoring, click Diagnostic settings.

Click + Add diagnostic setting.

Provide a Diagnostic setting name.

Under Logs > Categories, select the following categories:

AuditLogs

SignInLogs

NonInteractiveUserSignInLogs

ServicePrincipalSignInLogs

ManagedIdentitySignInLogs

ProvisioningLogs

ADFSSignInLogs

RiskyUsers

UserRiskEvents

NetworkAccessTrafficLogs

RiskyServicePrincipals

ServicePrincipalRiskEvents

EnrichedOffice365AuditLogs

MicrosoftGraphActivityLogs

RemoteNetworkHealthLogs

NetworkAccessAlerts



<img width="797" height="353" alt="image" src="https://github.com/user-attachments/assets/96cd3422-c243-4e17-a50e-c7aece8479e2" />









Notes from Splunk
ref : https://github.com/mka1111/Splunk-EXTRA/edit/main/AzureEventHubSplunk.md

Add-on prerequisites¶
Configure an application in Microsoft Entra ID for the Splunk Add-on for Microsoft Cloud Services
Connect to your Azure App Account with Splunk Add-on for Microsoft Cloud Services

- Configure an **Azure Event Hub for each log category in Azure**, such as Microsoft Entra ID, Resource, and Activit
- Authorize access to Azure Event Hubs by giving **Azure Event Hubs Data Receiver **permissions to each applicable Azure applicatio
- must use the Admin Configuration Service (ACS) to configure outbound **ports 5671/tcp and 5672/tcp **(Advanced Message Queuing Protocol (AMQP
- On your Azure deployment, you should configure a ratio of at least one Event Hub throughput unit for each partition  - example, if you have 20 throughput units, configure 20 partitions
- On the Splunk software side, the number of Event Hub inputs that you create as consumers on an Event Hub must be less than or equal to the number of partitions that you have on the Event Hub.
- The Azure EventHubs input for the Splunk Add-on for Microsoft Cloud Services is not compatible with the Event Hubs input in the Splunk Add-on for Microsoft Azure, when listening to the same Event Hub namespace. The Event Hubs input in the Splunk Add-on for Microsoft Azure needs to be disabled for this input to run.
- Interval	The number of seconds to wait before the Splunk platform runs the command again. The default is 3600 seconds.
- Select the source type based on the configured Event Hub. Supported source types are mscs:azure:eventhub, azure:monitor:aad, azure:monitor:resource and azure:monitor:activity.


Throughput units
Throughput units control the throughput capacity of event hubs. Throughput units are prepurchased units of capacity. A single throughput unit provides the following capabilities:

Ingress: Up to 1 MB per second or 1,000 events per second (whichever comes first).
Egress: Up to 2 MB per second or 4,096 events per second.
If you exceed the capacity of the throughput units you purchased, ingress is throttled and Event Hubs throws a EventHubsException with a Reason value of ServiceBusy.

Once you purchase throughput units, you pay for a minimum of one hour. 

Data ingress rates exceed set throughput units.
Data egress request rates exceed set throughput units.

It doesn't matter how many partitions are in an event hub when it comes to pricing. It depends on the number of pricing units (throughput units (TUs) for the standard tier

Standard tier: ~1 MB/s ingress and ~2 MB/s egress per partition.
Premium and Dedicated tiers: ~1-2 MB/s ingress and ~2-5 MB/s egress per partition.




Processing units
Event Hubs Premium provides superior performance and better isolation within a managed multitenant PaaS environment. The resources in a Premium tier are isolated at the CPU and memory level so that each tenant workload runs in isolation. This resource container is called a Processing Unit (PU). You can purchase 1, 2, 4, 6, 8, 10, 12, or 16 processing Units for each Event Hubs Premium namespace.

How much you can ingest and stream with a processing unit depends on various factors such as your producers, consumers, the rate at which you're ingesting and processing, and much more.

For example, Event Hubs Premium namespace with one PU and one event hub (100 partitions) can approximately offer core capacity of ~5-10 MB/s ingress and 10-20 MB/s egress for both AMQP or Kafka workloads.

For more information about configuring PUs for a premium tier namespace, see Configure processing units.




App
- Select Access Azure Service Management as organization under Delegated Permissions.

- Navigate to Home > Subscriptions.
Select the active subscription that you want to use from the Subscription Name column.
Select Access control (IAM)
Select Role assignments
Select Add role assignment.
In the Add role assignment drop-down list, perform the following steps:

a. Select Reader from the Role dropdown list.

b. Select User, group, or service principal from the Assign access to dropdown list, if it has not already been selected.

c. Select your application by searching for it by name in the dropdown.

Save your changes.
- 


<img width="888" height="484" alt="image" src="https://github.com/user-attachments/assets/0e540333-a863-40e9-b5d1-f59a078ba016" />











ref:
https://www.youtube.com/watch?v=GfVp2cx-w_E
