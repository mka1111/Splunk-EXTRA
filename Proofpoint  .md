https://splunkbase.splunk.com/app/4327

issue:
https://community.splunk.com/t5/All-Apps-and-Add-ons/Guidance-on-Configuring-Proofpoint-ET-Splunk-TA-in-Splunk-Cloud/m-p/743172

https://splunk.github.io/splunk-connect-for-syslog/1.87.0/sources/CyberArk/





Proofpoint on Demand configuration
Contact Proofpoint support to enable PoD Log API capability. This requires Remote syslog license on your deployment.

Make sure you have the Cluster ID and API Key before you start configuring the Add-on. The cluster ID can be found top right corner of your Proofpoint on Demand admin console and it looks like customername_hosted. The API key is a long series of 200+ alpha numeric characters. Optionally you can check if the API key is valid using a curl command. Here is an example:

curl -i --no-buffer -k -v -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: logstream.proofpoint.com:443" -H "Authorization: Bearer " -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" -H "Sec-WebSocket-Version: 13" "https://logstream.proofpoint.com:443/v1/stream?cid=&type=message"  

##Splunk Configuration

There are two steps to configure the Proofpoint On Demand Email Security Add-on. First, configure an account profile that would be used to connect to Proofpoint Log service. Second, configure mail and message inputs that would use the configured account profile to download logs and tokenize them. Here are the detailed steps:

From the Splunk home page, click on "Proofpoint On Demand Email Security Add On"
Click on the "Configuration" tab
Add button
Give an "Account Profile" name. For example, podlogapi
For "Cluster ID" input your cluster name.
For the "API Key" please past the API as received from Proofpoint. Please make sure to not add space or special character at the end of the API key.
Now that the account profile is created, next let's create input types.

From the "Proofpoint On Demand Email Security Add On" app context, select the "Inputs" tab
Select "Create New Input" on the right side, and select "Proofpoint Mail Log"
On the next screen, for "Name" give a name for this log. For example, pps_mail_log
Retry Interval, use 60 seconds. Please note that this retry setting is only used when the connection is lost. It's not a polling frequency as the logs are pushed using websocket from Proofpoint.
For "Index", select the index you want the logs to be available on.
For "Account Profile" select the account profile from previous step.
Follow steps 2-6 again and create "Proofpoint Message Log" input type. Make sure the use the same index for both input types.
Verification
The Proofpoint On Demand logs are collected by the source type pps_maillog and pps_messagelog. In the search box you can verify the logs by searching for sourcetype="pps_maillog" and sourcetype="pps_messagelog". Note, if the sourcetypes are not created, that means there were no logs downloaded after the inputs were created.
