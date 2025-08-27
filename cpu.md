index=_introspection sourcetype=splunk_resource_usage component=Hostwide earliest=-5m | timechart avg(data.cpu_user_pct) by host
