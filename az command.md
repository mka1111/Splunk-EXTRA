


az ad app permission list --id e042ec79-34cd-498f-9d9f-1234234

az network vnet

To get information about Virtual Machines (VMs) and Virtual Networks (VNets) using the Azure CLI, you'll use commands in the `az vm` and `az network vnet` groups. Below are the essential commands for listing, viewing details, and finding connections between these resources.

### **Core Commands for VMs and VNets**

Here are the primary Azure CLI commands to retrieve information about your VMs and virtual networks.

| **Goal** | **Azure CLI Command** | **Example & Notes** |
| :--- | :--- | :--- |
| **List all VMs** | `az vm list` | Lists all VMs in the current subscription. Use `--resource-group` to filter . |
| **Get detailed VM info** | `az vm show --name <vm_name> --resource-group <rg_name>` | Returns detailed JSON configuration, including hardware profile, OS profile, and network interfaces . |
| **Get VM IP addresses** | `az vm list-ip-addresses --name <vm_name> --resource-group <rg_name>` | Quickly retrieve the public and private IP addresses of a VM . |
| **List all virtual networks** | `az network vnet list` | Lists all VNets in the current subscription. Use `--resource-group` to filter . |
| **Get detailed VNet info** | `az network vnet show --name <vnet_name> --resource-group <rg_name>` | Shows detailed info about a specific VNet, including its address space, subnets, and DNS servers . |
| **List subnets in a VNet** | `az network vnet subnet list --vnet-name <vnet_name> --resource-group <rg_name>` | Lists all subnets within a specific virtual network . |

### **Finding the Connection Between a VM and its VNet**

A VM is not directly connected to a VNet but through a Network Interface (NIC). You can follow these steps to find the VNet for a specific VM.

1.  **Get the NIC ID**: First, query your VM to get the ID of the Network Interface it uses.
    ```bash
    az vm show --name <vm_name> --resource-group <rg_name> --query 'networkProfile.networkInterfaces[].id' --output tsv
    ```
    This command uses a JMESPath query (`--query`) to extract just the NIC ID and formats it as clean text (`--output tsv`) .

2.  **Show NIC Details**: Use the NIC ID from the previous step to get the NIC's configuration.
    ```bash
    az network nic show --ids <nic_id_from_step_1>
    ```
    Replace `<nic_id_from_step_1>` with the actual ID. The output will contain a section like `ipConfigurations[].subnet.id`, which holds the full resource ID of the subnet and its parent VNet .

3.  **Show the VNet (Optional)**: With the VNet ID from the NIC's subnet, you can directly view the virtual network's details.
    ```bash
    az network vnet show --ids <vnet_id_from_step_2>
    ```

### **Tips for Effective Queries**

- **Use `--output table` for Readability**: When you need a quick overview, format the output as a table. For example, `az vm list --output table` provides a clean list of your VMs .
- **Master `--query` for Specific Data**: The `--query` parameter uses the JMESPath query language, allowing you to extract precise values from the JSON output. This is incredibly useful for scripting . For instance, to get just the VM size, you would use:
    ```bash
    az vm show --name <vm_name> --resource-group <rg_name> --query 'hardwareProfile.vmSize' --output tsv
    ```
- **Use Short Arguments**: To save time, you can use shorthand like `-g` for `--resource-group`, `-n` for `--name`, and `-o` for `--output` .

By combining these commands and techniques, you can effectively gather any information you need about your VMs and the virtual networks they are connected to.





Based on our conversation history and a compilation of the most frequently used and highly-rated Azure CLI commands from official Microsoft documentation and community experts , I have curated a list of the top 20 most useful commands. These are categorized to help you manage everything from your account setup to your core compute and network resources.

### 🚀 Getting Started & Setup
These are the first commands you'll need to authenticate and configure your working environment.

1.  **`az login`**: Authenticates with your Azure account. This typically opens a browser for you to sign in .
2.  **`az account show`**: Displays details of your currently active Azure subscription, confirming you're working in the right context .
3.  **`az account list`**: Lists all the Azure subscriptions you have access to. You can use this to get the ID for `az account set` .
4.  **`az account set --subscription "MySub"`**: Switches your active subscription to the one named "MySub" .
5.  **`az config set defaults.group=MyRG defaults.location=westus2`**: Saves time by setting default resource groups and locations, so you don't have to type them for every command .
6.  **`az upgrade`**: Upgrades the Azure CLI to the latest version .
7.  **`az find "storage account"`**: Uses an AI-driven search to find command examples related to your keywords (like "storage account") .
8.  **`az interactive`**: Launches an interactive mode with auto-completion and command descriptions, great for learning .

### 📦 Resource & Asset Management
Commands for organizing your resources and querying the specific information you need.

9.  **`az group list --output table`**: Lists all resource groups in your subscription in a clean, readable table format .
10. **`az resource list --resource-group MyRG --output table`**: Lists all resources (VMs, networks, storage, etc.) contained within a specific resource group .
11. **`[command] --help`**: Appends `--help` to any command (e.g., `az vm create --help`) to see its full documentation, parameters, and examples right in the terminal .
12. **`az account show --query "{tenantId:tenantId, subscriptionId:id}"`**: A powerful querying example that extracts only the `tenantId` and `subscriptionId` and displays them in a friendly format . You can use `--query` with any command.

### 🖥️ Virtual Machine (VM) Management
Commands to handle your core compute resources, as discussed in our history.

13. **`az vm create --resource-group MyRG --name MyVM --image Ubuntu2204`**: Creates a new Ubuntu Linux VM in the specified resource group . It generates SSH keys by default.
14. **`az vm list-ip-addresses --name MyVM --resource-group MyRG`**: Quickly retrieves the public and private IP addresses of your VM .
15. **`az vm show --name MyVM --resource-group MyRG`**: Displays detailed JSON configuration of a specific VM, including its hardware, OS, and network settings .
16. **`az vm stop --name MyVM --resource-group MyRG`**: Powers off the running VM. The compute resources are stopped, but you continue to be billed for the storage .
17. **`az vm deallocate --name MyVM --resource-group MyRG`**: Stops and **deallocates** the VM, releasing the compute resources and stopping billing for them .
18. **`az vm list-sizes --location eastus`**: Lists all available VM sizes (cores, memory, storage performance) in a specific Azure region .

### 🌐 Networking & Storage
Commands to manage the supporting infrastructure for your VMs and applications.

19. **`az network vnet list --resource-group MyRG --output table`**: Lists all virtual networks within a resource group, as we discussed earlier .
20. **`az storage account list --resource-group MyRG --output table`**: Lists all storage accounts in a resource group, providing names, locations, and SKUs .

I hope this list gives you a powerful toolkit for navigating Azure from the command line. Are there any other specific services, like Azure Kubernetes Service (AKS) or Azure Databases, that you'd like a top-20 list for?
