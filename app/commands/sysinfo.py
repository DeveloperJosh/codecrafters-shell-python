# src/commands/sysinfo.py

import datetime
import os
import platform
import subprocess
from datetime import datetime

import psutil

def get_cpu_name() -> str:
    system = platform.system()

    if system == "Windows":
        try:
            import wmi
            c = wmi.WMI()
            for processor in c.Win32_Processor():
                return processor.Name
        except ImportError:
            return platform.processor()
    elif system == "Linux":
        command = "cat /proc/cpuinfo"
        cpu_info = subprocess.check_output(command, shell=True).strip().decode()
        for line in cpu_info.split("\n"):
            if "model name" in line:
                return line.split(":")[1].strip()
    elif system == "Darwin":
        command = "sysctl -n machdep.cpu.brand_string"
        cpu_info = subprocess.check_output(command, shell=True).strip().decode()
        return cpu_info
    return platform.processor()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class SysInfoCommand:
    def execute(self, args):
     try:
        processes = list(psutil.process_iter(attrs=[
            'pid', 'name', 'username', 'cpu_percent', 'memory_percent', 
            'memory_info', 'status', 'create_time'
        ]))
        
        # Sort processes by name to group them
        processes.sort(key=lambda p: p.info['name'])
        
        print(f"{'USER':<20} {'PID':<5} {'%CPU':<4} {'%MEM':<4} {'VSZ':<8} {'RSS':<8} {'TTY':<7} {'STAT':<7} {'START':<8} {'TIME':<12} {'COMMAND'}")
        
        for proc in processes:
            try:
                pinfo = proc.info
                if not pinfo['username']:
                    continue
                username = pinfo['username']
                pid = pinfo['pid']
                cpu_percent = pinfo['cpu_percent']
                memory_percent = pinfo['memory_percent']
                vms = get_size(pinfo['memory_info'].vms) if pinfo['memory_info'] else '0B'
                rss = get_size(pinfo['memory_info'].rss) if pinfo['memory_info'] else '0B'
                status = pinfo['status'] if pinfo['status'] else 'N/A'
                create_time = datetime.fromtimestamp(pinfo['create_time']) if pinfo['create_time'] else datetime.now()
                start_time = create_time.strftime('%H:%M:%S')
                run_time = str(datetime.now() - create_time).split('.')[0]  # format to remove microseconds
                
                name = pinfo['name']
                # Append PID to name if there are duplicates
                same_name_count = len([p for p in processes if p.info['name'] == pinfo['name']])
                if same_name_count > 1:
                    name = f"{pinfo['name']}[{pid}]"
                
                print(f"{username:<20} {pid:<5} {cpu_percent:<4.1f} {memory_percent:<4.1f} {vms:<8} {rss:<8} {'?':<7} {status:<7} {start_time:<8} {run_time:<12} {name}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
     except Exception as e:
        print(f"ps: An error occurred: {e}")