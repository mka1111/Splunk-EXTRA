
https://chat.deepseek.com/share/ifghdevcnkcsep3jxi





Step 1: Configure the Repository Channel
Choose the appropriate update channel for Defender packages:

Insider Fast – Bleeding-edge builds (for testing)

Insider Slow – More stable preview builds

Prod – Recommended for production environments

Action: Set the channel by configuring the repository URL accordingly.
Example for Prod

```
echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/20.04/prod focal main" | sudo tee /etc/apt/sources.list.d/microsoft-prod.list
```


Step 2: Install Microsoft GPG Key & HTTPS Driver
Before installing the Defender package, you need to add Microsoft’s GPG key and ensure apt can use HTTPS:

```
# Install HTTPS transport for apt
sudo apt-get update
sudo apt-get install apt-transport-https

# Download and install Microsoft GPG key
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
```


Step 3: Install MDATP (Defender for Endpoint)
Now install the mdatp package:


```
sudo apt-get update
sudo apt-get install mdatp

```




Step 4: Run the Onboarding Script
The onboarding script is a Python script provided by Microsoft.

It registers the device with your Defender tenant.

Typical steps:

Download the onboarding script from the Microsoft Defender portal (under Settings > Device Management > Onboarding).

Make it executable and run:




```

sudo python3 onboarding_script.py
```



your OS. For example:

For Ubuntu 22.04: https://packages.microsoft.com/ubuntu/22.04/prod

For Debian 11: https://packages.microsoft.com/debian/11/prod

For RHEL/CentOS 8: https://packages.microsoft.com/rhel/8/prod



# CENTOS

Based on the official Microsoft documentation, here are the steps to onboard a CentOS device to Microsoft Defender for Endpoint. There are two primary methods: a recommended automated script and a manual configuration.

The critical first step for either method is to download the onboarding package from the Microsoft Defender portal, as it contains the unique script that registers your specific device.

Method 1: Automated Script (Recommended)
This method uses a script that automatically detects your CentOS version, configures the correct repository, and installs the agent.

Prepare the Onboarding Package

Navigate to the Microsoft Defender portal (Settings > Endpoints > Device management > Onboarding).

Select Linux Server as the OS and Local Script as the deployment method.

Download the WindowsDefenderATPOnboardingPackage.zip file.

Extract the .zip file to get the onboarding script, typically named MicrosoftDefenderATPOnboardingLinuxServer.py.

Download and Run the Installer Script

Download the official installer script from Microsoft's GitHub repository.

Make the script executable and run it, providing the path to your onboarding script.

The --channel prod parameter installs the stable production version. You can also use insiders-fast or insiders-slow.

The --pre-req flag checks system requirements before installation



```
# Download the installer script
wget https://raw.githubusercontent.com/microsoft/mdatp-xplat/master/linux/installation/mde_installer.sh

# Make it executable
chmod +x mde_installer.sh

# Run the installer
sudo ./mde_installer.sh --install --onboard ./MicrosoftDefenderATPOnboardingLinuxServer.py --channel prod --pre-req
```



Method 2: Manual Configuration
This method involves manually adding the Microsoft repository and installing the package.

Configure the Repository

First, install yum-utils if it's not already present.

Identify the correct repository URL for your CentOS version. Use the table below as a guide:

CentOS Version	Repository URL
CentOS 7.2 - 7.9	https://packages.microsoft.com/config/rhel/7/prod.repo
CentOS 8.0 - 8.10	https://packages.microsoft.com/config/rhel/8/prod.repo
CentOS 9.0 - 9.8	https://packages.microsoft.com/config/rhel/9/prod.repo
Add the repository. For example, for CentOS 





```
sudo yum-config-manager --add-repo=https://packages.microsoft.com/config/rhel/7/prod.repo
```




```
mport the Microsoft GPG Key

This step is necessary to validate the integrity of the packages.

bash

```


From YOUTUBE
https://www.youtube.com/watch?v=-l7wTEE25I8


<img width="1186" height="407" alt="image" src="https://github.com/user-attachments/assets/0df8433f-f47f-4ca8-9299-d9c630d038b9" />

<img width="1315" height="711" alt="image" src="https://github.com/user-attachments/assets/c485f640-16c0-40d9-a492-c7e62fb68646" />

Funny check the version 


<img width="555" height="254" alt="image" src="https://github.com/user-attachments/assets/c3672d36-2330-4a56-8c28-8c46ae9d8453" />


make sure you have curl 

if some problems



<img width="694" height="122" alt="image" src="https://github.com/user-attachments/assets/59404993-14f8-4610-be7d-20e7c4ce1e53" />

Download key

<img width="943" height="97" alt="image" src="https://github.com/user-attachments/assets/11cd051f-2e4e-4412-af60-46018f40ff67" />


Move key

<img width="930" height="154" alt="image" src="https://github.com/user-attachments/assets/8d664d69-8051-4231-aafd-197baf58d043" />



install gpg packet 

<img width="953" height="297" alt="image" src="https://github.com/user-attachments/assets/1c11dc53-2b7b-44c7-bb2a-2cdac19a21fa" />

if problem withh gpg install gpnugp

<img width="712" height="186" alt="image" src="https://github.com/user-attachments/assets/c49adcb1-56d8-4202-80e6-372b9d259132" />



Register microsoft key,
after add put - add -

<img width="994" height="171" alt="image" src="https://github.com/user-attachments/assets/cc0cd5ef-ce6c-4060-8056-6e9238c7aa3b" />



Install http transport 

<img width="934" height="191" alt="image" src="https://github.com/user-attachments/assets/76a20ff3-5801-4574-a22d-44d7c0826c92" />



update repository 
<img width="556" height="96" alt="image" src="https://github.com/user-attachments/assets/ed6172ab-dbef-4232-a803-c09d81096a97" />



we should see microsoft links

<img width="930" height="82" alt="image" src="https://github.com/user-attachments/assets/e89ada98-8ddf-474e-9a92-aa7d8b23282d" />




install mdatp app

<img width="680" height="172" alt="image" src="https://github.com/user-attachments/assets/90db7116-2bbb-4767-b02d-dcf2688d72a8" />


<img width="687" height="158" alt="image" src="https://github.com/user-attachments/assets/fa40bd15-9f30-44f8-8b11-71b553aa9c03" />


<img width="946" height="502" alt="image" src="https://github.com/user-attachments/assets/89e8bc21-8f85-4299-959e-80841ba5dbb6" />


check if all good
<img width="580" height="51" alt="image" src="https://github.com/user-attachments/assets/273bedef-bbcb-435a-9242-08469499d2bf" />


thas means that machine is not onboarded

<img width="591" height="124" alt="image" src="https://github.com/user-attachments/assets/ae75f703-9f9b-413b-8cd9-9c519c205eed" />

check connectivity 
<img width="747" height="318" alt="image" src="https://github.com/user-attachments/assets/b7c84ef0-d693-440a-a7b0-e35b4d6146d5" />


<img width="763" height="106" alt="image" src="https://github.com/user-attachments/assets/2e96fcd2-da5d-49fa-88fb-eba88f8d08c9" />


from defender download python script 

<img width="461" height="272" alt="image" src="https://github.com/user-attachments/assets/73a9a288-ffe9-4421-b9bf-728ee6b8f84a" />

<img width="862" height="171" alt="image" src="https://github.com/user-attachments/assets/81224f28-baf4-43ac-ac18-751160f8b05d" />


this means that is installed
<img width="741" height="207" alt="image" src="https://github.com/user-attachments/assets/3dc66558-2c16-4dad-8466-5a9df6f435ba" />










```
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
```
