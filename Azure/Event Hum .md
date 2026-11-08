


Throughput Units (Ingress Speed)

• Per Throughput Unit (TU): In the Basic and Standard tiers, 1 TU provides up to 1 MB/sec or 1,000 events per second for ingress, and 2 MB/sec for
- You should provision at least 2 TUs to give yourself a safety buffer,
- Partitions are about parallelism, consumer scaling, and physical limitations, not just your total average throughput.
- Ingress Ceiling
-  ch partition caps at roughly 1 MB/s ingress regardless of how many TUs you’ve bought.
-  



- If your data has any micro-bursts, peak hours, or minor spikes (e.g., hitting 1.2 MB/sec for just a few seconds), Azure will immediately throw a ServerBusyException and reject your data.

Each partition caps at roughly 1 MB/s ingress regardless of how many TUs the namespace holds. The Defender hub is averaging 0.95 MB/s per partition — 95% of the ceiling, sustained. Every burst above average throttles instantly. That’s the entire explanation for why Defender throttles ~100× more than aad-diag while carrying fewer messages.

aad-diag at 0.22 MB/s per partition has ample room, and its 30 throttles over 12 hours are incidental — ignore them.

<img width="896" height="314" alt="image" src="https://github.com/user-attachments/assets/47f10e3c-073a-4b54-8e92-40ff3914d498" />

<img width="985" height="661" alt="image" src="https://github.com/user-attachments/assets/c099a275-b8b7-40ee-84bd-59e133d99b63" />



```
az monitor metrics list --resource <namespace-id> \
  --metric IncomingBytes --aggregation Total --interval PT1M \
  --start-time 2026-11-01T00:00:00Z \
  --query "value[0].timeseries[0].data[].total" -o tsv \
  | sort -n > /tmp/bytes.txt

N=$(wc -l < /tmp/bytes.txt)
for p in 50 95 99 100; do
  LINE=$(( N * p / 100 )); [ "$LINE" -lt 1 ] && LINE=1
  V=$(sed -n "${LINE}p" /tmp/bytes.txt)
  echo "P$p: $(echo "scale=2; $V / 60 / 1048576" | bc) MB/s"
done

```

## In the Standard tier, the maximum number of partitions is 32.   if you have more than 32 **consumer** threads, they cannot process in parallel



## Actions
Cutover: add a second Streaming API export in the Defender portal pointing at defender-v2, create a new Splunk input against it (you need a new input anyway — the hub name and consumer group fields aren’t editable after creation), confirm events are arriving on both, then delete the old export and input. Keeping both running briefly duplicates events for that window, which is cheaper than a gap.

Migration sequence
Build both new namespaces and hubs
Add second Streaming API export in the Defender portal → new hub, and a second diagnostic setting for AAD → new hub
Create new Splunk inputs against the new hubs (new inputs are required anyway — hub name and consumer group aren’t editable)
Confirm events arriving on both old and new paths
Remove the old exports, then the old Splunk inputs, then the old namespace



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
