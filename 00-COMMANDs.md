



# Version

splunk version
curl -k -u admin:password https://localhost:8089/services/server/info

# On Linux/Unix
rpm -qa | grep splunk
# or
dpkg -l | grep splunk

## Connectivity 



## How to check if conectivity to the port 8089 
curl -k -u admin:password https://localhost:8089/services/server/info



# Check all Splunk listening ports
    netstat -tlnp | grep splunk
    ss -tlnp | grep splunk
    lsof -i -P | grep splunk



## Windows
 Using netstat
netstat -ano | findstr "8000 8089 8088 9997 9998"

# Using PowerShell
Get-NetTCPConnection | Where-Object {$_.LocalPort -in @(8000,8089,8088,9997,9998,8191,8065)}







Here's how to add a Splunk user in Linux with proper groups and permissions:

## Method 1: Create Dedicated Splunk User (Recommended)

### Step 1: Create the user and group
```bash
# Create splunk group
sudo groupadd splunk

# Create splunk user with home directory and add to splunk group
sudo useradd -r -m -d /opt/splunk -s /bin/bash -g splunk -c "Splunk User" splunk

# OR for Universal Forwarder:
sudo useradd -r -m -d /opt/splunkforwarder -s /bin/bash -g splunk -c "Splunk Forwarder User" splunk
```

### Step 2: Set proper permissions on Splunk directories
```bash
# For Full Splunk/Heavy Forwarder
sudo chown -R splunk:splunk /opt/splunk
sudo chmod -R 755 /opt/splunk

# For Universal Forwarder
sudo chown -R splunk:splunk /opt/splunkforwarder
sudo chmod -R 755 /opt/splunkforwarder
```

### Step 3: Add user to additional groups if needed
```bash
# Add to adm group for system log access
sudo usermod -a -G adm splunk

# Add to root group for privileged access (if needed)
sudo usermod -a -G root splunk

# Verify group membership
groups splunk
```

## Method 2: Using a Script for Complete Setup
```bash
#!/bin/bash

# Variables
SPLUNK_USER="splunk"
SPLUNK_GROUP="splunk"
SPLUNK_HOME="/opt/splunk"  # Change to /opt/splunkforwarder for UF

# Create group if doesn't exist
if ! getent group $SPLUNK_GROUP > /dev/null; then
    sudo groupadd $SPLUNK_GROUP
    echo "Created group: $SPLUNK_GROUP"
fi

# Create user if doesn't exist
if ! id "$SPLUNK_USER" &>/dev/null; then
    sudo useradd -r -m -d $SPLUNK_HOME -s /bin/bash -g $SPLUNK_GROUP -c "Splunk User" $SPLUNK_USER
    echo "Created user: $SPLUNK_USER"
fi

# Set permissions
sudo chown -R $SPLUNK_USER:$SPLUNK_GROUP $SPLUNK_HOME
sudo chmod -R 755 $SPLUNK_HOME

# Add to additional groups for log access
sudo usermod -a -G adm $SPLUNK_USER
sudo usermod -a -G root $SPLUNK_USER

echo "Splunk user setup complete"
```

## Method 3: For Existing Splunk Installation
If Splunk is already installed and running as root or another user:

```bash
# Stop Splunk first
sudo /opt/splunk/bin/splunk stop

# Change ownership to splunk user
sudo chown -R splunk:splunk /opt/splunk

# Update Splunk to run as splunk user
sudo /opt/splunk/bin/splunk set default-confg -user splunk -group splunk

# Start Splunk as splunk user
sudo -u splunk /opt/splunk/bin/splunk start
```

## Method 4: Configure Systemd Service (for auto-start)

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/splunk.service
```

Add the following content:
```ini
[Unit]
Description=Splunk Enterprise
After=network.target

[Service]
Type=forking
RemainAfterExit=yes
ExecStart=/opt/splunk/bin/splunk start
ExecStop=/opt/splunk/bin/splunk stop
ExecReload=/opt/splunk/bin/splunk restart
User=splunk
Group=splunk
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable splunk.service
```

## Verify the Setup

### Check user and permissions:
```bash
# Verify user exists
id splunk

# Check directory permissions
ls -la /opt/splunk/

# Verify Splunk runs as correct user
ps aux | grep splunk
```

### Check file permissions structure:
```bash
# Important directories and their recommended permissions
sudo find /opt/splunk -type d -exec ls -ld {} \; | head -10
sudo find /opt/splunk -name "*.conf" -exec ls -l {} \; | head -5
```

## Additional Security Considerations

### Set up log directory permissions:
```bash
# Create splunk log directory
sudo mkdir -p /var/log/splunk
sudo chown splunk:splunk /var/log/splunk
sudo chmod 755 /var/log/splunk
```

### Secure the Splunk home directory:
```bash
# Remove unnecessary permissions
sudo chmod 700 /opt/splunk/.bash_history
sudo chmod 700 /opt/splunk/.bashrc
```

### Create a password for the splunk user (if needed for login):
```bash
sudo passwd splunk
```

## Important Notes:

1. **Universal Forwarder vs Full Splunk**: Use `/opt/splunkforwarder` for UF installations
2. **SELinux**: If SELinux is enabled, you may need to adjust contexts
3. **AppArmor**: On Ubuntu, ensure AppArmor profiles allow access
4. **Firewall**: Ensure necessary ports are open for Splunk communication

This setup ensures Splunk runs with the principle of least privilege while having access to necessary system resources and log files.
