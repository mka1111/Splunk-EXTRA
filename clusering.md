Total daily indexing volume, number of peer nodes, replication factor, and search factor



splunkd_access.log – Indexer cluster communication logs
– Example:
index=_internal sourcetype=splunkd_access
(uri="/services/cluster/slave/buckets*" OR uri="/services/cluster/master/buckets*")
| convert ctime(_time) | table _time uri_path | sort _time
<img width="1578" height="869" alt="image" src="https://github.com/user-attachments/assets/b332d378-84fb-4f84-b53c-d7f39a363b76" />
