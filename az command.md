


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
