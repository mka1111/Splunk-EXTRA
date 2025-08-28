Total daily indexing volume, number of peer nodes, replication factor, and search factor



splunkd_access.log – Indexer cluster communication logs
– Example:
index=_internal sourcetype=splunkd_access
(uri="/services/cluster/slave/buckets*" OR uri="/services/cluster/master/buckets*")
| convert ctime(_time) | table _time uri_path | sort _time


