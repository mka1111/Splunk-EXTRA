Good question 👍 You want to use **splunkd logs** to detect when an **IP or network is removed from an access control list (ACL)**, and store/detect it via the `access` index.

Let’s break it down:

---

### 🔹 1. Where it shows up

* In **Splunk**, `splunkd.log` records system and configuration changes.
* ACL or firewall changes may also appear in the **data source logs** (e.g., Cisco ASA, Palo Alto, Linux iptables).
* If you’ve got those ingested into the `access` index, that’s the best place to detect “removal.”

---

### 🔹 2. Searching `splunkd.log`

To look for changes in ACLs (example: “removed,” “deleted,” “revoked” keywords):

```spl
index=_internal sourcetype=splunkd
("remove" OR "removed" OR "delete" OR "deleted" OR "revoked") AND ("ACL" OR "Access List" OR "network" OR "ip")
| table _time host log_level component message
```

This shows you when Splunk recorded messages about ACL/IP/network removal.

---

### 🔹 3. Searching your **`access` index** (firewall or access logs)

If ACL modifications are logged there:

```spl
index=access ("remove" OR "deleted" OR "revoked") ("ACL" OR "Access List" OR "network" OR "ip")
| rex "(?<ip_removed>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
| stats count by _time user host ip_removed
```

* `rex` extracts the IP removed
* `user` field (if available) shows who made the change

---

### 🔹 4. Example for Cisco ASA logs in `access` index

```spl
index=access sourcetype=cisco:asa ("access-list" AND "removed")
| rex "access-list \S+ denied (?<ip_removed>\d+\.\d+\.\d+\.\d+)"
| table _time src_user src host ip_removed
```

---

✅ This way, you can:

* Detect removals in Splunk’s own logs (`splunkd`)
* Or in your security device logs stored in `access`

---

Do you want me to build this into a **correlation search** that will generate a **notable event** whenever an IP/network is removed from an ACL?
