



# Version

splunk version
# On Linux/Unix
rpm -qa | grep splunk
# or
dpkg -l | grep splunk

## Connectivity 



## How to check if conectivity to the port 8089 
curl -k -u admin:password https://localhost:8089/services/server/info



