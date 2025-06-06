![image](https://github.com/user-attachments/assets/becb9fac-e818-4449-b206-f9070493abb1)![image](https://github.com/user-attachments/assets/db69c567-350c-4d0d-af0f-6ae3020ca8e8)![image](https://github.com/user-attachments/assets/c514c807-f429-43b3-b761-4e7c4dcdeace)

===== Restarting


splunk@tiger:~/var/log/splunk$ cat splunkd_stderr.log 
2025-06-04 21:00:14.812 +0100 splunkd started (build e9664af3d956) pid=621253
2025-06-04 21:13:55.527 +0100 Interrupt signal received sent by PID 628479, command="/opt/splunkforwarder/bin/splunk restart" (UID 997, same as my group)
2025-06-04 21:14:01.364 +0100 splunkd started (build e9664af3d956) pid=628596
2025-06-04 21:26:56.523 +0100 Interrupt signal received sent by PID 635556, command="../../../../bin/splunk restart" (UID 997, same as my group)
2025-06-04 21:27:02.268 +0100 splunkd started (build e9664af3d956) pid=635666
2025-06-04 21:49:08.410 +0100 Interrupt signal received sent by PID 647487, command="/opt/splunkforwarder/bin/splunk stop" (UID 0)
2025-06-06 07:51:20.807 +0100 splunkd started (build e9664af3d956) pid=2219
2025-06-06 18:18:00.638 +0100 Interrupt signal received sent by PID 103681, command="/opt/splunkforwarder/bin/splunk restart" (UID 997, same as my group)
2025-06-06 18:23:23.962 +0100 splunkd started (build e9664af3d956) pid=106905
2025-06-06 18:24:05.342 +0100 Interrupt signal received sent by PID 107297, command="/opt/splunkforwarder/bin/splunk restart" (UID 997, same as my group)
2025-06-06 18:24:48.177 +0100 splunkd started (build e9664af3d956) pid=107746
splunk@tiger:~/var/log/splunk$ id
uid=997(splunk) gid=985(splunk) groups=985(splunk),4(adm)


![image](https://github.com/user-attachments/assets/186e0049-2a55-4634-a440-616f5aca5cbf)



======  INDX Indexer switched off   - checking logs on UF

06-06-2025 18:36:21.558 +0100 INFO  TailReader [107812 tailreader0] - Batch input finished reading file='/opt/splunkforwarder/var/spool/splunk/tracker.log'
06-06-2025 18:36:25.618 +0100 WARN  AutoLoadBalancedConnectionStrategy [107804 TcpOutEloop] - Cooked connection to ip=192.168.1.84:9997 timed out
06-06-2025 18:36:45.543 +0100 WARN  AutoLoadBalancedConnectionStrategy [107804 TcpOutEloop] - Cooked connection to ip=192.168.1.84:9997 timed out
06-06-2025 18:36:51.543 +0100 INFO  TailReader [107812 tailreader0] - Batch input finished reading file='/opt/splunkforwarder/var/spool/splunk/tracker.log'
06-06-2025 18:37:05.467 +0100 WARN  AutoLoadBalancedConnectionStrategy [107804 TcpOutEloop] - Cooked connection to ip=192.168.1.84:9997 timed out
06-06-2025 18:37:21.475 +0100 INFO  TailReader [107812 tailreader0] - Batch input finished reading file='/opt/splunkforwarder/var/spool/splunk/tracker.log'
06-06-2025 18:37:25.391 +0100 WARN  AutoLoadBalancedConnectionStrategy [107804 TcpOutEloop] - Cooked connection to ip=192.168.1.84:9997 timed out



![image](https://github.com/user-attachments/assets/88f4b9fd-0e2b-4165-b47f-a882d1afac2c)


======== make sure that UF is sending data


splunk@tiger:~/var/log/splunk$ cat metrics.log   | tail -5
06-06-2025 19:01:59.956 +0100 INFO  Metrics - group=tailingprocessor, name=tailreader0, current_queue_size=0, max_queue_size=3, files_queued=31, new_files_queued=2, fd_cache_size=2
06-06-2025 19:01:59.956 +0100 INFO  Metrics - group=thruput, name=cooked_output, instantaneous_kbps="0.000", instantaneous_eps="0.000", average_kbps="0.151", total_k_processed="337.000"="0.000", ev=0
06-06-2025 19:01:59.956 +0100 INFO  Metrics - group=thruput, name=thruput, instantaneous_kbps="0.000", instantaneous_eps="0.000", average_kbps="0.000", total_k_processed="0.000", kb="0., ev=0, load_average="0.161"
06-06-2025 19:01:59.956 +0100 INFO  Metrics - group=thruput, name=uncooked_output, instantaneous_kbps="0.000", instantaneous_eps="0.000", average_kbps="0.000", total_k_processed="0.000"="0.000", ev=0
06-06-2025 19:02:19.956 +0100 INFO  Metrics - group=queue, name=tcpout_splunk_indexers, max_size=512000, current_size=507329, largest_size=507329, smallest_size=507329
splunk@tiger:~/var/log/splunk$ ^C




![image](https://github.com/user-attachments/assets/3f0c14f5-a48b-4cab-a7aa-a259541d7f4e)












