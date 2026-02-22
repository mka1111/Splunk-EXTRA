
LOGS

<img width="1048" height="284" alt="image" src="https://github.com/user-attachments/assets/c9ad662b-aec9-4634-be26-96ddea43dc60" />


# PUSH

<img width="1250" height="914" alt="image" src="https://github.com/user-attachments/assets/9653915d-9f0b-40b8-ab4d-7971d0b6f833" />
<img width="1069" height="716" alt="image" src="https://github.com/user-attachments/assets/2b759b94-c37b-46e6-af90-776875ccd33c" />


The push approach typically uses Amazon Data Firehose to stream data to a Splunk HTTP Event Collector (HEC) endpoint
where Data Firehose integration is not possible, an alternative approach is to deploy a script, typically as a Lambda function, to pull the required data via the AWS API and then push the data to a Splunk HEC endpoint

Benefits
  Highly Scalable
  Tight integration between AWS services
  Lower latency data ingest than the pull approach
  Supports HEC ACK (SCP)


Considerations/Limitations
  Requires a publicly accessible HEC endpoint
  Customer managed HEC endpoints must use a Public Certificate Authority issued SSL Certificate
  Not all data sources support push based ingestion


# PULL
<img width="1174" height="864" alt="image" src="https://github.com/user-attachments/assets/c2ae88a9-ddc2-46d3-927c-cb3c5ee2f57c" />
<img width="1135" height="624" alt="image" src="https://github.com/user-attachments/assets/40adc764-f773-4425-a601-3d3b39cea43c" />


Benefits
  Capable of utilizing private networks or VPC endpoints to retrieve data
  Supports bulk/replay scenarios in addition to incremental pulls
Considerations/Limitations
  Pull approach uses scheduled data retrievals which introduces ingestion latency
  Can generate an uncontrolled influx of events, which may overwhelm Splunk hosts and negatively impact data ingestion and indexing performance causing indexing pipelines and queues to block





  ================

Send VPC Flow Log Data to Splunk Using Amazon Kinesis Data Firehose | Amazon Web Services

  https://www.youtube.com/watch?v=idizFTiOqUE

<img width="1253" height="341" alt="image" src="https://github.com/user-attachments/assets/ff8993ad-69b6-4ba5-8b24-a67ce03b3758" />


<img width="1121" height="547" alt="image" src="https://github.com/user-attachments/assets/97d33783-f3b3-4336-8294-c3f997fbe0fb" />

<img width="1343" height="512" alt="image" src="https://github.com/user-attachments/assets/bf012600-5af8-4075-b5ca-052667a9f555" />



1 Create HTTP Collector 
<img width="1380" height="615" alt="image" src="https://github.com/user-attachments/assets/b108e9e0-02e0-44ff-a2c9-8c0e56151027" />
<img width="1104" height="529" alt="image" src="https://github.com/user-attachments/assets/b08cd854-2e62-4c75-a683-1bdfc5a923d1" />


2 Go to Lambda

<img width="1022" height="369" alt="image" src="https://github.com/user-attachments/assets/28983d99-a2cd-481c-9734-39b3a43da19f" />


3 Create New Function
<img width="559" height="266" alt="image" src="https://github.com/user-attachments/assets/bbf7ee48-3452-4540-8658-7350ce0601e6" />
<img width="792" height="294" alt="image" src="https://github.com/user-attachments/assets/3f01821c-6473-4fab-ba36-e7873bc98452" />
<img width="905" height="499" alt="image" src="https://github.com/user-attachments/assets/e9e95155-718f-45a9-b30d-656af4883a68" />

and Deploy
<img width="539" height="299" alt="image" src="https://github.com/user-attachments/assets/b7bddc0b-c6ed-4e63-a293-40833575b9b9" />


we will be needning id
<img width="1402" height="330" alt="image" src="https://github.com/user-attachments/assets/dc030a74-e7bc-4d53-9379-ff1a0b8d4ebf" />


4 Go to Kinesiss
<img width="1459" height="723" alt="image" src="https://github.com/user-attachments/assets/ecfeff78-06d0-4d77-8c7b-128626c8db50" />

<img width="1146" height="658" alt="image" src="https://github.com/user-attachments/assets/6f2c2300-cc78-48fa-808f-4060ae6da2d6" />

<img width="800" height="297" alt="image" src="https://github.com/user-attachments/assets/99498a5c-f57c-4036-aaae-d5fad46a8b27" />

<img width="972" height="636" alt="image" src="https://github.com/user-attachments/assets/86375faa-55f1-4ccd-a858-af1f1e2b2b00" />


1meg
<img width="517" height="194" alt="image" src="https://github.com/user-attachments/assets/580fd87f-2e19-4dd9-a743-5aa255bfdefd" />


<img width="809" height="272" alt="image" src="https://github.com/user-attachments/assets/0e643042-092f-462d-8474-90c01fcf018f" />

<img width="727" height="177" alt="image" src="https://github.com/user-attachments/assets/d38a1b7c-b95a-4fbc-982b-b907ef12ea32" />


For the backup selet one of the buckets
<img width="1514" height="690" alt="image" src="https://github.com/user-attachments/assets/280be0a5-b769-41b2-9790-165445282bac" />

And create Delivery stream 
<img width="992" height="357" alt="image" src="https://github.com/user-attachments/assets/7c96c057-a717-4409-acd7-f994f8d9ec80" />


5 Go to VPC to create VPV Flow Logs




<img width="1426" height="760" alt="image" src="https://github.com/user-attachments/assets/4eb1e11a-2420-4af0-acfd-e637e85380da" />

<img width="241" height="172" alt="image" src="https://github.com/user-attachments/assets/979a0c84-9ba1-4afd-9e80-4eb4e9608766" />


<img width="596" height="167" alt="image" src="https://github.com/user-attachments/assets/3028c1d4-9e9e-4221-8ad1-b1592088c6b0" />

<img width="730" height="186" alt="image" src="https://github.com/user-attachments/assets/80d860ed-aa2f-49fe-b983-8701b147c598" />


<img width="1032" height="519" alt="image" src="https://github.com/user-attachments/assets/9b5718a5-ce6d-4c5c-86fc-b1fd933869df" />

<img width="307" height="76" alt="image" src="https://github.com/user-attachments/assets/18d75ee0-fd1c-4aa5-867a-88f5966b5379" />


















































  
