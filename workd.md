Skip to content
Chat history
Skip to content
Chat history

You said:
splunk workday:user_activity 

example leaver logs or terminate
ChatGPT said:
I’ll walk you through this step by step.

When you want to look for Workday leaver/termination events in Splunk, you’ll typically search against the Workday user_activity sourcetype (or whichever sourcetype your environment uses). Workday logs usually include events like Terminate Employee, End Contingent Worker, or Rescind Termination.

Here’s a simple example Splunk search you can start with:

index=workday sourcetype="workday:user_activity"
("Terminate Employee" OR "End Contingent Worker" OR "Termination" OR "Rescind Termination")
| table _time user_id user_name action performed_by worker_id worker_name details
Example of a termination log entry you might see:
{
  "_time": "2025-09-16T08:14:23Z",
  "sourcetype": "workday:user_activity",
  "user_id": "john.doe@example.com",
  "user_name": "John Doe",
  "worker_id": "12345",
  "worker_name": "John Doe",
  "action": "Terminate Employee",
  "performed_by": "hr.manager@example.com",
  "details": {
    "termination_date": "2025-09-30",
    "reason": "Voluntary Resignation"
  }
}
Tips:
Common termination-related actions in Workday logs:

Terminate Employee

End Contingent Worker

Request Rescind Termination

Complete Termination

If you want only leaver events in the last 30 days:

index=workday sourcetype="workday:user_activity"
("Terminate Employee" OR "End Contingent Worker")
earliest=-30d@d latest=now
| table _time user_id user_name worker_id worker_name action performed_by
👉 Do you want me to build you a Splunk query that detects all terminated users who still have active accounts in AD/Okta (a common offboarding use case), or just the raw Workday leaver events?




No file chosenNo file chosen
ChatGPT can make mistakes. Check important info. See Cookie Preferences.

You said:
splunk workday:user_activity 

example leaver logs or terminate
ChatGPT said:
I’ll walk you through this step by step.

When you want to look for Workday leaver/termination events in Splunk, you’ll typically search against the Workday user_activity sourcetype (or whichever sourcetype your environment uses). Workday logs usually include events like Terminate Employee, End Contingent Worker, or Rescind Termination.

Here’s a simple example Splunk search you can start with:

index=workday sourcetype="workday:user_activity"
("Terminate Employee" OR "End Contingent Worker" OR "Termination" OR "Rescind Termination")
| table _time user_id user_name action performed_by worker_id worker_name details
Example of a termination log entry you might see:
{
  "_time": "2025-09-16T08:14:23Z",
  "sourcetype": "workday:user_activity",
  "user_id": "john.doe@example.com",
  "user_name": "John Doe",
  "worker_id": "12345",
  "worker_name": "John Doe",
  "action": "Terminate Employee",
  "performed_by": "hr.manager@example.com",
  "details": {
    "termination_date": "2025-09-30",
    "reason": "Voluntary Resignation"
  }
}
Tips:
Common termination-related actions in Workday logs:

Terminate Employee

End Contingent Worker

Request Rescind Termination

Complete Termination

If you want only leaver events in the last 30 days:

index=workday sourcetype="workday:user_activity"
("Terminate Employee" OR "End Contingent Worker")
earliest=-30d@d latest=now
| table _time user_id user_name worker_id worker_name action performed_by
👉 Do you want me to build you a Splunk query that detects all terminated users who still have active accounts in AD/Okta (a common offboarding use case), or just the raw Workday leaver events?




No file chosenNo file chosen
ChatGPT can make mistakes. Check important info. See Cookie Preferences.
