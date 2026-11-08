


Throughput Units (Ingress Speed)

• Per Throughput Unit (TU): In the Basic and Standard tiers, 1 TU provides up to 1 MB/sec or 1,000 events per second for ingress, and 2 MB/sec for
- You should provision at least 2 TUs to give yourself a safety buffer,
- Partitions are about parallelism, consumer scaling, and physical limitations, not just your total average throughput.
- Ingress Ceiling
-  



- If your data has any micro-bursts, peak hours, or minor spikes (e.g., hitting 1.2 MB/sec for just a few seconds), Azure will immediately throw a ServerBusyException and reject your data.





## In the Standard tier, the maximum number of partitions is 32.   if you have more than 32 **consumer** threads, they cannot process in parallel





<img width="1031" height="834" alt="image" src="https://github.com/user-attachments/assets/3dfae533-7446-451d-bf9e-f0624354b094" />



```
// Replace 'AzureDiagnostics' with your specific Event Hub log table if customized
AzureDiagnostics
| where TimeGenerated > ago(12h)
| where OperationName == "OperationalLogs" // Filters for traffic logs
| summarize IngressBytes = sum(ExpressMessageByteSize_d) by bin(TimeGenerated, 1m)
| extend IngressMBperSec = (IngressBytes / 1024 / 1024) / 60
| summarize MaxPeakSpeed = max(IngressMBperSec), AverageSpeed = avg(IngressMBperSec)

```
