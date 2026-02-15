

```java
| inputlookup sourcetype.csv
| eval file="sourcetype.csv"
| eval current_sourcetype=sourcetype 
| append [
| inputlookup recomendations.csv
| eval file="recomendations.csv"
| eval recommended_sourcetype=sourcetype
]
| stats  values(recommended_sourcetype) as recommended_sourcetype values(service) as service  values(file) as file values(current_sourcetype) as current_sourcetype by sourcetype
| eval status=if(mvcount(file)>1,"present",if(file IN( "sourcetype.csv"),"out of recommendation","missing"))
| eval recommended_sourcetype=if(status IN ("out of recommendation"),"..... ".current_sourcetype." ......",'recommended_sourcetype') 
| eval sort_position=if(status IN ("missing","present"),1,0)
| sort - recommended_sourcetype sort_position
| table service recommended_sourcetype status



```
