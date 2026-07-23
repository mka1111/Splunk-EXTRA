
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



```
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
```
