#!/bin/env python3
import subprocess
import re
import platform
import socket
import psutil
import json
import requests
class SystemInfo:
    def __init__(self, machine_name, operating_system, version, manufacturer, model, total_memory,
                 disks, system_type, hostname, python_version, processor_type, processor_cores, processor_threads,
                 network_adapters, dell_service_tag):
        self.machine_name = machine_name
        self.operating_system = operating_system
        self.version = version
        self.manufacturer = manufacturer
        self.model = model
        self.total_memory = total_memory
        self.disks = json.dumps(disks)
        self.system_type = system_type
        self.hostname = hostname
        self.python_version = python_version
        self.processor_type = processor_type
        self.processor_cores = processor_cores
        self.processor_threads = processor_threads
        self.network_adapters = json.dumps(network_adapters)
        self.dell_service_tag = dell_service_tag

def submit_system_info(system_info):
   
    try:
        system = SystemInfo(
            machine_name=system_info['Hostname'],
            operating_system=system_info['Operating System'],
            version=system_info['Version'],
            manufacturer=system_info['Manufacturer'],
            model=system_info['Model'],
            total_memory=system_info['Total Memory (GB)'],
            disks=system_info['Disks'],
            system_type=system_info['System Type'],
            hostname=system_info['Hostname'],
            python_version=system_info['Python Version'],
            processor_type=system_info['Processor Type'],
            processor_cores=system_info['Processor Cores'],
            processor_threads=system_info['Processor Threads'],
            network_adapters=system_info['Network Adapters'],
            dell_service_tag=system_info['Dell Service Tag']
        )
        api_url = '{{app_url}}systeminfo/' + system.hostname  # Replace with your API endpoint URL
        response = requests.post(api_url, json=system.__dict__)
        response.raise_for_status()
        print('System information submitted successfully.')
    except requests.exceptions.RequestException as e:
        print('Failed to submit system information:', e)


def get_system_info():
   
    # Retrieve Disk information
    disks = []
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        if partition.device.startswith('/dev/'):
            disk = {
                'DeviceID': partition.device,
                'Size': psutil.disk_usage(partition.mountpoint).total,
                'FreeSpace': psutil.disk_usage(partition.mountpoint).free
            }
            disks.append(disk)

    # Retrieve Manufacturer and Model
    manufacturer = platform.system()
    model = platform.machine()

    # Retrieve Hostname
    hostname = platform.node()

    # Retrieve Python version
    python_version = platform.python_version()

    # Retrieve Processor information
    processor = {
        'Type': platform.processor(),
        'Cores': psutil.cpu_count(logical=False),
        'Threads': psutil.cpu_count(logical=True)
    }

    # Retrieve Network link speed
    
    network_adapters = psutil.net_if_stats()
    network_info = {}
    for adapter, stats in network_adapters.items():
        if stats.isup and not ('loopback' in stats.flags.split(',')):
            ip_address = ', '.join([addr.address for addr in psutil.net_if_addrs()[adapter] if addr.family == socket.AF_INET])
            network_info[adapter] = ip_address

    # Retrieve Dell service tag
    dell_service_tag=''
    try:
      

      dell_service_tag = subprocess.check_output(['dmidecode', '-t', 'system'], universal_newlines=True)
      dell_service_tag = re.search(r'Serial Number:\s*(.*)', dell_service_tag).group(1)
    except FileNotFoundError:
        print ("DMIDecode not installed on system")
    except subprocess.CalledProcessError as e:
        print (e)
    except Exception as e:
        pass

    # Define system_info variables for the current machine
    system_info = {
        'Operating System': platform.system(),
        'Version': platform.release(),
        'Manufacturer': manufacturer,
        'Model': model,
        'Total Memory (GB)': round(psutil.virtual_memory().total / 1024**3, 2),
        'Disks': disks,
        'System Type': f'{manufacturer} {model}',
        'Hostname': hostname,
        'Python Version': python_version,
        'Processor Type': processor['Type'],
        'Processor Cores': processor['Cores'],
        'Processor Threads': processor['Threads'],
        'Network Adapters': network_info,
        'Dell Service Tag': dell_service_tag
    }

    return system_info

# Specify the machine name
#machine_name = 'your_machine_name'

# Call the function to retrieve system information for the specified machine
system_info = get_system_info()

# Output the system information in the specified format
for key, value in system_info.items():
    print(f"|{key}:|{value}|")

submit_system_info(system_info)