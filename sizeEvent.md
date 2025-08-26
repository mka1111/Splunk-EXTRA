Got it 👍 You want a **Splunk search** that calculates the **size of the incoming data** (how much data is being indexed or coming into Splunk).

There are a few ways, depending on whether you want:

---

### 1. **Size of Events (Raw Data Size)**

If you want to see how much data (bytes/MB/GB) is being ingested from events:

```spl
index=* 
| eval bytes=len(_raw) 
| stats sum(bytes) as total_bytes 
| eval total_MB=round(total_bytes/1024/1024,2), total_GB=round(total_bytes/1024/1024/1024,2)
```

🔹 Explanation:

* `len(_raw)` → calculates event size in bytes.
* `stats sum(bytes)` → sums up all events in the search window.
* Converts to **MB** and **GB**.

---

### 2. **Daily Ingest by Index**

If you want to see how much data is coming per index per day:

```spl
| tstats sum(_raw) as bytes where index=* by _time span=1d index
| eval MB=round(bytes/1024/1024,2), GB=round(bytes/1024/1024/1024,2)
```

This uses `tstats` (much faster than `stats`).

---

### 3. **License Usage (Official Data Volume)**

Splunk tracks license usage (which is data indexed per day). You can query it with:

```spl
index=_internal source=*license_usage.log type="Usage" 
| stats sum(b) as bytes by idx 
| eval MB=round(bytes/1024/1024,2), GB=round(bytes/1024/1024/1024,2)
| sort -GB
```

🔹 This is the **most accurate** way, because Splunk billing/licensing is based on this.

---

👉 Question for you:
Do you want the **real license usage (official ingestion size)** or just an **approximate size of events in searches**?
