======   DIVIDE INDEX ==========
┌─[splunk@parrot]─[/opt/splunk/etc/apps/mka/local]
└──╼ $cat props.conf transforms.conf 
[mka_sourcetype]
DATETIME_CONFIG = CURRENT
LINE_BREAKER = ([\r\n]+)
NO_BINARY_CHECK = true
category = Custom
description = mka_sourcetype
pulldown_type = true
SHOULD_LINEMERGE = false


[source::/opt/splunk/etc/apps/mka/logs/system.logs]
TRANSFORMS-split = authentication, mail, change
[authentication]
REGEX = authentication
FORMAT = s_authentication
DEST_KEY = _MetaData:Index

[mail] 
REGEX = mail
FORMAT = s_mail
DEST_KEY = _MetaData:Index

[change]
REGEX = change
FORMAT = s_change
DEST_KEY = _MetaData:Index
┌─[splunk@parrot]─[/opt/splunk/etc/apps/mka/local]
└──╼ $

======   DIVIDE SOURCETYPE  ==========


props.conf
```json
splunk@parrot]─[/opt/splunk/etc/apps/mka/local]
└──╼ $cat props.conf 




[source::/opt/splunk/etc/apps/mka/logs/system.logs]
TRANSFORMS-split = authentication, mail, change
[mka_sourcetype]
DATETIME_CONFIG = CURRENT
LINE_BREAKER = ([\r\n]+)
NO_BINARY_CHECK = true
category = Custom
description = mka_sourcetype
pulldown_type = true
SHOULD_LINEMERGE = false


```

transforms.conf
```json
┌─[splunk@parrot]─[/opt/splunk/etc/apps/mka/local]
└──╼ $cat transforms.conf 



[authentication]
REGEX = authentication
FORMAT = sourcetype::s:authentication
DEST_KEY = MetaData:Sourcetype
WRITE_META = true

[mail] 
REGEX = mail
FORMAT = sourcetype::s:mail
DEST_KEY = MetaData:Sourcetype
WRITE_META = true

[change]
REGEX = change
FORMAT = sourcetype::s:change
DEST_KEY = MetaData:Sourcetype
WRITE_META = true
 

```



```
[firewall_logs]
INGEST_EVAL = sourcetype=if(match(_raw,"DROPPED"),"firewall_deny","firewall_allow")

