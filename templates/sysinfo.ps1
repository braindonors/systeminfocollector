# Required module for JSON manipulation
Import-Module -Name 'PowerShellGet' -Force
$ihostname=""
# Function to retrieve system information
function Get-SystemInfo {
    # Retrieve IP Address
    #$ipAddress = (Get-NetIPAddress | Where-Object {$_.AddressFamily -eq 'IPv4' -and $_.InterfaceAlias -ne 'Loopback'}).IPAddress

    $networkAdapters = Get-NetAdapter | Where-Object {$_.Status -eq 'Up'}

$nicInfoList = foreach ($adapter in $networkAdapters) {
    $ipAddresses = $adapter | Get-NetIPAddress | Where-Object {$_.AddressFamily -eq 'IPv4'} | Select-Object -ExpandProperty IPAddress
    $macAddress = $adapter.MacAddress

    [PSCustomObject]@{
        NIC = $adapter.Name
        IPAddress = $ipAddresses -join ', '
        MACAddress = $macAddress
    }
}
    # Retrieve Disk information
    $disks = Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, Size, FreeSpace

    # Retrieve Manufacturer and Model
    $systemInfo = Get-CimInstance -ClassName Win32_ComputerSystem
    $manufacturer = $systemInfo.Manufacturer
    $model = $systemInfo.Model

    # Retrieve Hostname
    $hostname = $env:COMPUTERNAME

    # Retrieve PowerShell version
    $psVersion = $PSVersionTable.PSVersion.ToString()

    # Retrieve Processor information
    $processor = Get-WmiObject -Class Win32_Processor
    $processorType = $processor.Name
    $processorCores = $processor.NumberOfCores
    $processorThreads = $processor.NumberOfLogicalProcessors

    # Retrieve Network link speed
    $network = Get-WmiObject -Class Win32_NetworkAdapter | Where-Object {$_.Speed -ne $null}
    $networkLinkSpeed = $network.Speed

    # Retrieve Dell service tag
    $dellServiceTag = Get-WmiObject -Namespace root\cimv2 -Class win32_Bios | Select-Object -ExpandProperty SerialNumber

    # Define system info object
    $systemInfo = [ordered]@{
        'machine_name' = $env:COMPUTERNAME
        'operating_system' = (Get-WmiObject -Class Win32_OperatingSystem).Caption
        'version' = (Get-WmiObject -Class Win32_OperatingSystem).Version
        'manufacturer' = $manufacturer
        'model' = $model
        'total_memory' = "{0:N2}" -f ((Get-WmiObject -Class Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum / 1GB)
        'disks' = $disks
        'system_type' = $manufacturer + ' ' + $model
        'hostname' = $hostname
        'python_version' = $psVersion
        'processor_type' = $processorType
        'processor_cores' = $processorCores
        'processor_threads' = $processorThreads
        'network_adapters' = $networkadapters
        'dell_service_tag' = $dellServiceTag
    }

    # Output the system info object
    $systemInfo
}

# Call the function to retrieve system information locally on the current system
$systemInfo = Get-SystemInfo

# Convert system info object to JSON
$jsonData = $systemInfo | ConvertTo-Json
$hostname = $env:COMPUTERNAME
# Submit JSON data to the Python web server
$PostURL = "{{app_url}}systeminfo/$hostname"
Write-Host "Submit to $PostURL"
Invoke-RestMethod -Uri $PostURL -Method Post -Body $jsonData -ContentType 'application/json'
