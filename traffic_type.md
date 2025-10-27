To see the different values for the `group` field in `splunkd` logs with `tcpin_connections`, you can use these Splunk searches:

## 1. List All Unique Group Values

```sql
index=_internal source=*metrics.log group=tcpin_connections 
| stats count by group
| sort -count
```

## 2. More Detailed Breakdown

```sql
index=_internal source=*metrics.log group=* 
| search group=*tcpin*
| stats dc(group) as unique_groups, values(group) as all_groups
```

## 3. See Group Values with Connection Counts

```sql
index=_internal source=*metrics.log group=*tcpin*
| stats sum(total_connections) as total_conn, 
        sum(active_connections) as active_conn,
        sum(kb_in) as kb_in,
        sum(kb_out) as kb_out
        by group
| sort -total_conn
```

## 4. Common Group Values You Might See:

```sql
index=_internal source=*metrics.log group=*tcpin*
| chart count over _time by group
```

## 5. Real-time Group Monitoring

```sql
index=_internal source=*metrics.log group=*tcpin*
| timechart span=1h sum(active_connections) by group
```

## 6. Detailed Connection Analysis by Group

```sql
index=_internal source=*metrics.log group=*tcpin*
| eval conn_ratio = (active_connections / total_connections) * 100
| table _time, group, total_connections, active_connections, conn_ratio, kb_in, kb_out
| sort - _time
```

## Expected Group Values:

Common `group` values for `tcpin_connections` typically include:

- **`tcpin_connections`** - General TCP input connections
- **`ssl_tcpin_connections`** - SSL/TLS encrypted connections
- **`http_input_connections`** - HTTP input connections
- **`s2s_tcpin_connections`** - Splunk-to-Splunk connections
- **`indexer_tcpin`** - Indexer-specific connections
- **`forwarder_tcpin`** - Forwarder connections
- **`<specific_port>`** - Connections on specific ports like `8089`, `9997`

## 7. To See All Possible Group Values:

```sql
index=_internal source=*metrics.log 
| dedup group
| table group
| search group=*tcpin*
```

The first search (#1) will give you the clearest view of all different `group` values that exist in your `tcpin_connections` data. Run that search to see exactly what group values are present in your specific Splunk environment.
