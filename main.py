#!/usr/bin/env python3

import argparse
import os
import platform
import socket
import psutil
import json
from datetime import datetime

def get_system_info():
    """Get basic system information"""
    info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
    return info

def get_cpu_info():
    """Get CPU information"""
    cpu_info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": psutil.cpu_freq().max if psutil.cpu_freq() else "N/A",
        "current_frequency": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
        "cpu_usage_per_core": [f"{x}%" for x in psutil.cpu_percent(percpu=True, interval=1)],
        "total_cpu_usage": f"{psutil.cpu_percent()}%"
    }
    return cpu_info

def get_memory_info():
    """Get memory information"""
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()
    
    # Convert bytes to GB
    def bytes_to_gb(bytes_val):
        return round(bytes_val / (1024**3), 2)
    
    memory_info = {
        "total": f"{bytes_to_gb(virtual_mem.total)} GB",
        "available": f"{bytes_to_gb(virtual_mem.available)} GB",
        "used": f"{bytes_to_gb(virtual_mem.used)} GB",
        "percentage": f"{virtual_mem.percent}%",
        "swap_total": f"{bytes_to_gb(swap_mem.total)} GB",
        "swap_used": f"{bytes_to_gb(swap_mem.used)} GB",
        "swap_percentage": f"{swap_mem.percent}%"
    }
    return memory_info

def get_disk_info():
    """Get disk information"""
    partitions = psutil.disk_partitions()
    disk_info = []
    
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "file_system": partition.fstype,
                "total_size": f"{round(partition_usage.total / (1024**3), 2)} GB",
                "used": f"{round(partition_usage.used / (1024**3), 2)} GB",
                "free": f"{round(partition_usage.free / (1024**3), 2)} GB",
                "percentage": f"{partition_usage.percent}%"
            })
        except:
            # Some partitions may not be accessible
            pass
    
    return disk_info

def get_network_info():
    """Get network information"""
    network_info = {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "interfaces": {},
    }
    
    net_io = psutil.net_io_counters(pernic=True)
    
    for interface, stats in net_io.items():
        network_info["interfaces"][interface] = {
            "bytes_sent": f"{round(stats.bytes_sent / (1024**2), 2)} MB",
            "bytes_received": f"{round(stats.bytes_recv / (1024**2), 2)} MB",
            "packets_sent": stats.packets_sent,
            "packets_received": stats.packets_recv,
        }
    
    return network_info

def get_process_info(sort_by="memory", limit=10):
    """Get top processes by memory or CPU usage"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            proc_info = proc.info
            processes.append({
                "pid": proc_info['pid'],
                "name": proc_info['name'],
                "username": proc_info['username'],
                "memory_percent": proc_info['memory_percent'],
                "cpu_percent": proc_info['cpu_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Sort processes by specified criteria
    if sort_by == "memory":
        processes.sort(key=lambda x: x['memory_percent'], reverse=True)
    else:  # sort by CPU
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    
    return processes[:limit]

def display_info(data, title=None):
    """Display information in a readable format"""
    if title:
        print(f"\n=== {title} ===\n")
    
    if isinstance(data, dict):
        max_key_length = max(len(key) for key in data.keys())
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            elif isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key:{max_key_length}}: {value}")
    elif isinstance(data, list):
        if data and isinstance(data[0], dict):
            # Get all possible keys
            keys = set()
            for item in data:
                keys.update(item.keys())
            
            # Print header
            if "name" in keys:  # Prioritize 'name' if it exists
                keys.remove("name")
                header = "Name"
                for key in keys:
                    header += f" | {key.capitalize()}"
                print(header)
                print("-" * len(header))
            
            # Print each item
            for item in data:
                if "name" in item:  # Prioritize 'name' if it exists
                    line = f"{item['name']}"
                    for key in keys:
                        if key != "name":
                            line += f" | {item.get(key, 'N/A')}"
                    print(line)
                else:
                    print(item)
        else:
            for item in data:
                print(f"- {item}")

def save_to_file(data, filename):
    """Save information to a file in JSON format"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Information saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="System Information Tool")
    parser.add_argument("-a", "--all", action="store_true", help="Show all system information")
    parser.add_argument("-s", "--system", action="store_true", help="Show basic system information")
    parser.add_argument("-c", "--cpu", action="store_true", help="Show CPU information")
    parser.add_argument("-m", "--memory", action="store_true", help="Show memory information")
    parser.add_argument("-d", "--disk", action="store_true", help="Show disk information")
    parser.add_argument("-n", "--network", action="store_true", help="Show network information")
    parser.add_argument("-p", "--processes", action="store_true", help="Show top processes")
    parser.add_argument("--sort-by", choices=["cpu", "memory"], default="memory", 
                       help="Sort processes by CPU or memory usage")
    parser.add_argument("--limit", type=int, default=10, help="Limit number of processes shown")
    parser.add_argument("-o", "--output", help="Save output to file")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    # If no specific option is selected, show basic system info
    if not any([args.all, args.system, args.cpu, args.memory, args.disk, args.network, args.processes]):
        args.system = True
    
    # Collect requested information
    results = {}
    
    if args.all or args.system:
        results["system"] = get_system_info()
    
    if args.all or args.cpu:
        results["cpu"] = get_cpu_info()
    
    if args.all or args.memory:
        results["memory"] = get_memory_info()
    
    if args.all or args.disk:
        results["disk"] = get_disk_info()
    
    if args.all or args.network:
        results["network"] = get_network_info()
    
    if args.all or args.processes:
        results["processes"] = get_process_info(args.sort_by, args.limit)
    
    # Output results
    if args.json:
        if args.output:
            save_to_file(results, args.output)
        else:
            print(json.dumps(results, indent=4))
    else:
        results["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if args.output:
            save_to_file(results, args.output)
        else:
            print(f"\nSystem Information - {results['timestamp']}\n")
            
            if "system" in results:
                display_info(results["system"], "System Information")
            
            if "cpu" in results:
                display_info(results["cpu"], "CPU Information")
            
            if "memory" in results:
                display_info(results["memory"], "Memory Information")
            
            if "disk" in results:
                display_info(results["disk"], "Disk Information")
            
            if "network" in results:
                display_info(results["network"], "Network Information")
            
            if "processes" in results:
                sort_type = "Memory" if args.sort_by == "memory" else "CPU"
                display_info(results["processes"], f"Top {args.limit} Processes by {sort_type} Usage")

if __name__ == "__main__":
    main()
