<QueryList>
  <Query Id="0">
    <!-- Logon activity -->
    <Select Path="Security">*[System[(EventID=4624 or EventID=4625 or EventID=4634 or EventID=4647 or EventID=4648 or EventID=4672 or EventID=4776 or EventID=4768 or EventID=4769 or EventID=4771)]]</Select>

    <!-- Account and group management -->
    <Select Path="Security">*[System[(EventID=4720 or EventID=4722 or EventID=4723 or EventID=4724 or EventID=4725 or EventID=4726 or EventID=4738 or EventID=4740 or EventID=4767 or EventID=4728 or EventID=4732 or EventID=4756 or EventID=4735)]]</Select>

    <!-- Process creation and privilege use -->
    <Select Path="Security">*[System[(EventID=4688 or EventID=4673 or EventID=4674 or EventID=4697)]]</Select>

    <!-- Policy, audit and log tampering -->
    <Select Path="Security">*[System[(EventID=1102 or EventID=4719 or EventID=4713 or EventID=4906 or EventID=4907)]]</Select>

    <!-- Service installation, log clearing, unexpected shutdown -->
    <Select Path="System">*[System[(EventID=7045 or EventID=7040 or EventID=104 or EventID=6008 or EventID=1074)]]</Select>

    <!-- PowerShell script block and module logging -->
    <Select Path="Microsoft-Windows-PowerShell/Operational">*[System[(EventID=4103 or EventID=4104)]]</Select>
    <Select Path="Windows PowerShell">*[System[(EventID=400 or EventID=403 or EventID=600)]]</Select>

    <!-- Scheduled tasks -->
    <Select Path="Microsoft-Windows-TaskScheduler/Operational">*[System[(EventID=106 or EventID=140 or EventID=141 or EventID=200)]]</Select>

    <!-- WMI persistence -->
    <Select Path="Microsoft-Windows-WMI-Activity/Operational">*[System[(EventID=5857 or EventID=5858 or EventID=5859 or EventID=5860 or EventID=5861)]]</Select>

    <!-- RDP sessions -->
    <Select Path="Microsoft-Windows-TerminalServices-LocalSessionManager/Operational">*[System[(EventID=21 or EventID=23 or EventID=24 or EventID=25)]]</Select>

    <!-- Defender detections -->
    <Select Path="Microsoft-Windows-Windows Defender/Operational">*[System[(EventID=1006 or EventID=1007 or EventID=1008 or EventID=1116 or EventID=1117 or EventID=5001 or EventID=5007 or EventID=5010 or EventID=5012)]]</Select>
  </Query>
</QueryList>
