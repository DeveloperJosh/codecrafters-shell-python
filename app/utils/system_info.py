import os
import platform
import subprocess

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
