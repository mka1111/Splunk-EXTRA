```java

| rest /services/data/props/calcfields
| search eai:acl.app IN ( "Splunk_SA_CIM" )   
| table  title field.name   value eai:acl.app author

```
