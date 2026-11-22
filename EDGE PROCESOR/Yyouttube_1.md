
https://www.youtube.com/watch?v=CvTRT7HOJvw

https://www.youtube.com/watch?v=oyofqBBUxn0

create correct user firewall 

<img width="753" height="209" alt="image" src="https://github.com/user-attachments/assets/b71870af-cca6-43c1-b3fd-1d4a1d9ae06a" />

https://www.youtube.com/watch?v=ZbSzKN__-sw

<img width="919" height="188" alt="image" src="https://github.com/user-attachments/assets/1e06839a-bbfc-437f-98b9-4c1b974f0ef1" />



# Extraction

<img width="1001" height="197" alt="image" src="https://github.com/user-attachments/assets/e0ea7b51-fb52-4c26-b7b9-b66d994e76e6" />



# Destination to ES cloud??
<img width="1286" height="251" alt="image" src="https://github.com/user-attachments/assets/fcc712de-0336-461e-9b19-aabe61f635b6" />


# Check if you have certs for destinamtion

<img width="1016" height="263" alt="image" src="https://github.com/user-attachments/assets/e10b2888-b914-4f00-9e31-e8ecdf2c89e2" />


# SPL2 requries regex with beginning and end  ^ and $


```
$pipeline = | from $source
| rex field=$raw /^.+\\s(?P<accountname>[a-z]+-[a-z]+-\\d) (?P<servicename>\\w+)\\[(?<actionid>\\d+)\\]: (?P<message>.+)$/

| into $destination;
```

<img width="817" height="84" alt="image" src="https://github.com/user-attachments/assets/a5f035e3-94c1-4934-923a-f21644d215f3" />


# jak robiny rerouting bedziemy mieli 2 destimation

<img width="1116" height="496" alt="image" src="https://github.com/user-attachments/assets/7351e0a1-e140-4f67-9ef5-1311c2a03f01" />



