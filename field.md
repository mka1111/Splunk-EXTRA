``` powershell 
| rest /services/data/props/calcfields
| search eai:acl.app IN ( "Splunk_SA_CIM" )   
| table  type title field.name value eai:acl.app author
| append [
| rest /services/data/props/fieldaliases
| search eai:acl.app IN ( "Splunk_SA_CIM" )   
| rex field=value "\s+as\s+(?<fieldname>.*$)"
| rename fieldname as field.name
| table type  title  field.name  value eai:acl.app author
]

```


```java

| rest /services/data/props/calcfields
| search eai:acl.app IN ( "Splunk_SA_CIM" )   
| table  title field.name   value eai:acl.app author



| rest /services/data/props/fieldaliases
| search eai:acl.app IN ( "Splunk_SA_CIM" )   
| table type   title value eai:acl.app author



```

```
| rest /services/data/props/fieldaliases 
| table title, field_alias, value

| rest /services/data/props/calcfields 
| table title, field_name, eval_expression



```
