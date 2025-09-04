Perfect 👍 If you want to check **connections between Splunk instances using only the internal logs** (`_internal`), the best source is **metrics.log**. That’s where Splunk writes all connection and throughput information.

Here’s how you can approach it:

---

## 🔹 1. Forwarder → Indexer connections

Search in `_internal` for `tcpin_connections`:

```spl
index=_internal source=*metrics.log group=tcpin_connections
| stats latest(_time) as lastSeen values(version) as version values(fwdType) as forwarder_type by hostname sourceIp destIp
| eval lastSeen=strftime(lastSeen,"%Y-%m-%d %H:%M:%S")
```

* **hostname** = forwarder’s host name
* **sourceIp** = forwarder’s IP
* **destIp** = indexer that accepted the connection
* **forwarder\_type** = uf (Universal Forwarder), full (Heavy Forwarder/Enterprise), lwf (deprecated)
* **lastSeen** = when data last arrived

---

## 🔹 2. Data Throughput Between Instances

If you want to see *how much* data flows:

```spl
index=_internal source=*metrics.log group=tcpin_connections
| timechart sum(kb) AS throughput_kb by hostname
```

This shows the **bandwidth usage per forwarder**.

---

## 🔹 3. Search Head ↔ Indexer (Distributed Search)

For distributed setups (SH → Indexer), check **searches.log** and **metrics.log** for `distributed_search` group:

```spl
index=_internal source=*metrics.log group=distributed_search
| stats latest(_time) as lastSeen values(mode) as search_mode by dest
| eval lastSeen=strftime(lastSeen,"%Y-%m-%d %H:%M:%S")
```

* **dest** = the indexer being queried by the Search Head
* **mode** = streaming / results retrieval

---

## 🔹 4. Indexer Cluster Connections

If you use an indexer cluster, you can also see **clustering messages** in `_internal`:

```spl
index=_internal sourcetype=splunkd component=CMReplication
| stats count by host peer_name status
```

This tells you which peer indexers are connected to the cluster master.

---

✅ **Summary**

* Use `group=tcpin_connections` in metrics.log → Forwarders → Indexers
* Use `group=distributed_search` → Search Head → Indexers
* Use `component=CMReplication` → Indexer clustering

---

👉 Do you want me to put together a **ready-made SPL query** that shows *all Splunk-to-Splunk connections (forwarders, SH, indexers, cluster peers)* in one combined table?

Got it 👍 You want to go deeper into **how to map Splunk-to-Splunk connections directly from `_internal` logs**. Let me expand step by step and give you more ready queries.

---

# 🔹 1. Forwarder → Indexer (tcpin\_connections)

Every forwarder (UF/HF/Enterprise acting as forwarder) logs into **metrics.log** with group `tcpin_connections`.

```spl
index=_internal source=*metrics.log group=tcpin_connections
| eval MB=kb/1024
| stats latest(_time) as lastSeen values(version) as version values(fwdType) as forwarder_type sum(MB) as total_MB by hostname sourceIp destIp
| eval lastSeen=strftime(lastSeen,"%Y-%m-%d %H:%M:%S")
| sort - total_MB
```

* ✅ Shows **who is connected to which indexer**
* ✅ Data volume sent
* ✅ Forwarder type (`uf`, `full`, `lwf`)

---

# 🔹 2. Indexer → Indexer (Clustering)

If you have clustering enabled, the **peer connections** are logged:

```spl
index=_internal sourcetype=splunkd component=CMReplication OR component=CMMaster
| stats latest(status) as status by host peer_name
```

* ✅ Shows which indexers (peers) are connected to the **Cluster Master**
* ✅ Status of replication

---

# 🔹 3. Search Head → Indexers (Distributed Search)

When a search head sends queries to indexers, it logs them in metrics.log with group `distributed_search`:

```spl
index=_internal source=*metrics.log group=distributed_search
| stats latest(_time) as lastSeen values(mode) as search_mode values(status) as status by host dest
| eval lastSeen=strftime(lastSeen,"%Y-%m-%d %H:%M:%S")
```

* **host** = the Search Head
* **dest** = the Indexer it’s talking to
* **search\_mode** = streaming, results retrieval
* **status** = ok/failure

---

# 🔹 4. Deployment Server → Clients

If you use a Deployment Server, it logs **phoneHome activity**:

```spl
index=_internal sourcetype=splunkd component=DSClient
| stats latest(_time) as lastSeen values(deploymentServer) as DS by hostname
| eval lastSeen=strftime(lastSeen,"%Y-%m-%d %H:%M:%S")
```

* ✅ Shows which clients (UF/HF) have phoned home to the Deployment Server

---

# 🔹 5. License Master → Slaves

License communication is also visible in `_internal`:

```spl
index=_internal sourcetype=splunkd component=LMTracker
| stats latest(status) as status values(master) as license_master by slave
```

* ✅ Shows connections from license slaves → license master

---

# 🔹 6. Forwarder Status (heartbeat)

Every forwarder also sends heartbeat messages. These can be tracked with:

```spl
index=_internal sourcetype=splunkd component=Metrics group=thruput
| stats latest(_time) as lastSeen avg(kBps) as avg_kBps by host
| eval lastSeen=strftime(lastSeen,"%Y-%m-%d %H:%M:%S")
```

---

# 🔹 7. Unified “Connection Map”

If you want to **see all Splunk-to-Splunk connections in one place**, you can union the above queries. Example skeleton:

```spl
(
  search index=_internal source=*metrics.log group=tcpin_connections
  | eval connection_type="Forwarder→Indexer"
  | table _time host sourceIp destIp connection_type fwdType kb
)
UNION
(
  search index=_internal source=*metrics.log group=distributed_search
  | eval connection_type="SearchHead→Indexer"
  | table _time host dest connection_type status
)
UNION
(
  search index=_internal sourcetype=splunkd component=CMReplication
  | eval connection_type="Indexer→ClusterMaster"
  | table _time host peer_name connection_type status
)
```

👉 This gives you a **connection matrix** across all Splunk roles.

---

✅ **Summary:**

* Use `tcpin_connections` for forwarders → indexers
* Use `distributed_search` for SH → indexers
* Use `CMReplication` for indexer clustering
* Use `DSClient` for Deployment Server connections
* Use `LMTracker` for License Master

---

Do you want me to build this into a **dashboard (XML or Simple XML with panels)** so you can import it and see all these connections visually in Splunk Web?




