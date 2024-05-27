import psutil
import platform
from datetime import datetime
from cpuinfo import get_cpu_info

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class SysInfoCommand():
    def execute(self, args):
        # Get information about the system, i.e., the OS, RAM, CPU, etc.
        uname = platform.uname()
        cpu_info = get_cpu_info()
        cpu_name = cpu_info['brand_raw']
        total_cpu_usage = psutil.cpu_percent()
        virtual_memory = psutil.virtual_memory()
        boot_time_timestamp = psutil.boot_time()
        boot_time = datetime.fromtimestamp(boot_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")

        system_info = f"""
System Information
-------------------
System: {uname.system}
CPU: {cpu_name} ({psutil.cpu_count(logical=False)} cores)
Total CPU Usage: {total_cpu_usage}%
 Memory: 
    Total: {get_size(virtual_memory.total)}
    Used: {get_size(virtual_memory.used)}
    Free: {get_size(virtual_memory.free)}
    Usage Percentage: {virtual_memory.percent}%
Boot Time: {boot_time}
        """

        print(system_info.strip())