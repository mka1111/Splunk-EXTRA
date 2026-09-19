https://www.youtube.com/watch?v=QHEtAHGiCpc&t=1989s

https://www.youtube.com/watch?v=Jqucy138ets&t=2417s


<img width="1451" height="838" alt="image" src="https://github.com/user-attachments/assets/e68f0069-094d-4990-b0df-2a7bbde8b9f5" />





<img width="1057" height="541" alt="image" src="https://github.com/user-attachments/assets/bd0f2639-46b8-4bff-bd8c-667fc7eeacfe" />




- detection
- hunting
- investigate 

SIEM 'sim'
Analytics  Tier 'tir' 
Data is being ingested directly into Analytics Tier and mirrored down or directly into the data lake. 

Microsoft entra ID tenant


Daily  Cap   



<img width="1589" height="932" alt="image" src="https://github.com/user-attachments/assets/c8d56aed-c833-48a3-8fb9-41c50742aa00" />




<img width="1675" height="858" alt="image" src="https://github.com/user-attachments/assets/8045e354-b048-4826-838d-655b95f5bcc5" />


if we look  at the linux logs logs like syslog custom logs apps logs CEF logs we have many alternatives Azure Monitoring Agent. 
if you use things like log stash / cributl you can also send those logs 

iw we take a look at  windows side 
We also have Azure  monitoring agent  
Also we could centralzise ingestion if you have number of windows server  to be able to centralize the collection of those logs. 
Czesto movi though subscription 
if those servers ccannot connect to th the public interne you could se up a log analytics gateway in order to send  that data into the Sentinel workspace.

- we can take advantage of the REST API , that log ingestion API to be able to send logs using a number of the diferent SDKs like Python, Java C# 



<img width="1855" height="1016" alt="image" src="https://github.com/user-attachments/assets/9661b590-de7c-4c1e-9d8c-6d670b91598d" />




<img width="1849" height="1018" alt="image" src="https://github.com/user-attachments/assets/4253b70f-e236-40f1-b300-18494782ff50" />



Data Collection Pipeline 
Clients
- Direct ingest
-   Agents

Data Collection Rule
- Data to collect
- Schema of incoming Stream
- Transformation to filter and manipulate data
- Destination to send data

  Incoming DAta -> Transformation -> Transformed Data -> Microsoft Sentinel Analitics / Data Lake.


  Transformation
  - Filter records and columns
  - Add calculated columns
  - Parse data for destination
  - Hide Sensitive Data


<img width="1880" height="1015" alt="image" src="https://github.com/user-attachments/assets/62b7f8b4-2c77-461d-97be-f131df44d8c0" />


<img width="1841" height="919" alt="image" src="https://github.com/user-attachments/assets/2d88ef28-e773-4d84-9b93-051900b2a04f" />

<img width="1835" height="1014" alt="image" src="https://github.com/user-attachments/assets/1a6d735c-6492-4206-aed4-5d285bc7562f" />


<img width="751" height="440" alt="image" src="https://github.com/user-attachments/assets/0d3d4a27-8e27-47b7-8770-419eca26f7ce" />


<img width="801" height="781" alt="image" src="https://github.com/user-attachments/assets/af893083-1e96-4821-8af5-e2608515f82e" />


<img width="741" height="291" alt="image" src="https://github.com/user-attachments/assets/0cc63dfc-1571-438e-b842-50b46323ea4d" />


<img width="1575" height="722" alt="image" src="https://github.com/user-attachments/assets/3067178e-856b-49bb-8ac1-1b0c2100bd79" />



 <img width="797" height="357" alt="image" src="https://github.com/user-attachments/assets/7dcb7b66-1f64-43f3-af2f-590b669ebe88" />

 <img width="778" height="555" alt="image" src="https://github.com/user-attachments/assets/1d64906b-8370-4499-844b-9a659f964855" />

<img width="821" height="418" alt="image" src="https://github.com/user-attachments/assets/fcb764df-c73e-44a1-aa00-00aee7cff01e" />



