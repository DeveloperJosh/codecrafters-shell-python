import psutil

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class Ps:
    def execute(self, args):
        # Print the header
        print(f"{'PID':<10} {'NAME':<25} {'STATUS':<10} {'CPU%':<10} {'MEMORY%':<10} {'MEMORY':<15}")

        # Iterate over all running processes
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent', 'memory_info']):
            try:
                # Fetch process details
                pid = proc.info['pid']
                name = proc.info['name']
                status = proc.info['status']
                cpu_percent = proc.info['cpu_percent']
                memory_percent = proc.info['memory_percent']
                memory_info = get_size(proc.info['memory_info'].rss)

                # Print process details
                print(f"{pid:<10} {name:<25} {status:<10} {cpu_percent:<10.2f} {memory_percent:<10.2f} {memory_info:<15}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass