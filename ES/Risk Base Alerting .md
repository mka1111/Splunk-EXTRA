

https://splunk.github.io/rba/
https://www.youtube.com/watch?v=94oalGr8RXc




<img width="1249" height="653" alt="image" src="https://github.com/user-attachments/assets/8d7155aa-14c8-4c32-bc33-9a0701f196a8" />


<img width="1255" height="574" alt="image" src="https://github.com/user-attachments/assets/06ab83e8-958c-45ef-bf35-f917398a41bd" />

<img width="1110" height="677" alt="image" src="https://github.com/user-attachments/assets/a4da68c9-4b7f-4310-b41d-fb887c7d0bcb" />

<img width="1264" height="595" alt="image" src="https://github.com/user-attachments/assets/a612b8ee-6821-4954-9d9d-af8ef19f2ddc" />

<img width="1182" height="670" alt="image" src="https://github.com/user-attachments/assets/d36571ea-bb70-4933-8d26-eca9deeb71a3" />



<img width="1900" height="789" alt="image" src="https://github.com/user-attachments/assets/6da32d04-cc6a-4d28-9d58-1500f5cbd007" />

<img width="1191" height="486" alt="image" src="https://github.com/user-attachments/assets/4432c9c5-6e84-45ae-aef6-6d53d4674eae" />


Risk Events are those individual suspicious things. Each one is a small observation like “this user logged in from a new country”, “this host ran PowerShell with an encoded command”, or “this account failed MFA five times”. On its own, each would be too noisy to alert on, so instead of becoming an alert it’s written down as a risk event against a specific entity (the risk object), with a score attached.

Risk Score is the running total of those scores for that entity over a time window. A new-country login might add 20, encoded PowerShell 40, a disabled security tool 80, and so on. When the total crosses a threshold, a Risk Notable is created for an analyst to investigate.

<img width="3873" height="1557" alt="image" src="https://github.com/user-attachments/assets/a74d3c1a-59fd-408f-be05-095ac9a12767" />


https://youtu.be/94oalGr8RXc?t=1485




# Risk Factor



<img width="1182" height="531" alt="image" src="https://github.com/user-attachments/assets/6bfc03dd-4912-4430-8639-3236330613b4" />


## For example increasing Score  if admin 

<img width="911" height="508" alt="image" src="https://github.com/user-attachments/assets/7ea89155-a3e3-42d3-9747-f540f32202a1" />

https://youtu.be/94oalGr8RXc?t=1870


https://research.splunk.com/

<img width="1243" height="646" alt="image" src="https://github.com/user-attachments/assets/a0ba5a75-a9d2-4a99-98ea-25bf328229df" />

## How to calculate SCORE

<img width="1822" height="950" alt="image" src="https://github.com/user-attachments/assets/ebce96c2-8815-4b61-b63e-c180daa31d9d" />



## Machine learning has to use mltk toolkit to create its own model
## we can configure the model to look into the Risk Index to learn patterns and behaviors and anomaly detections -> vonvert into notable events. 
## 


## 




==========================

https://www.youtube.com/watch?v=hvRxNZOZ5po

<img width="984" height="551" alt="image" src="https://github.com/user-attachments/assets/8f925368-eba9-4d03-baa4-50dc4ab8deb5" />




