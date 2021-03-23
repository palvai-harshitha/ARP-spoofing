#Program for device monitoring

import psutil
import platform
from datetime import datetime
import logging  # It is a package which is used for writting output in text files or log files
logging.basicConfig(filename="details.txt", level=logging.DEBUG, format='%(message)s')
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
print("="*40, "System Information", "="*40)
uname = platform.uname()
logging.info(f"System: {uname.system}")
logging.info(f"Node Name: {uname.node}")
logging.info(f"Release: {uname.release}")
logging.info(f"Version: {uname.version}")
logging.info(f"Machine: {uname.machine}")
logging.info(f"Processor: {uname.processor}")
logging.info("="*40, "Boot Time", "="*40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
logging.info(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
logging.info("="*40, "CPU Info", "="*40)
# number of cores
logging.info("Physical cores:", psutil.cpu_count(logical=False))
logging.info("Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
cpufreq = psutil.cpu_freq()
logging.info(f"Max Frequency: {cpufreq.max:.2f}Mhz")
logging.info(f"Min Frequency: {cpufreq.min:.2f}Mhz")
logging.info(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
logging.info("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    logging.info(f"Core {i}: {percentage}%")
logging.info(f"Total CPU Usage: {psutil.cpu_percent()}%")
# Memory Information
logging.info("="*40, "Memory Information", "="*40)
# get the memory details
svmem = psutil.virtual_memory()
logging.info(f"Total: {get_size(svmem.total)}")
logging.info(f"Available: {get_size(svmem.available)}")
logging.info(f"Used: {get_size(svmem.used)}")
logging.info(f"Percentage: {svmem.percent}%")
logging.info("="*20, "SWAP", "="*20)
# get the swap memory details (if exists)
swap = psutil.swap_memory()
logging.info(f"Total: {get_size(swap.total)}")
logging.info(f"Free: {get_size(swap.free)}")
logging.info(f"Used: {get_size(swap.used)}")
logging.info(f"Percentage: {swap.percent}%")
# Disk Information
logging.info("="*40, "Disk Information", "="*40)
logging.info("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    logging.info(f"=== Device: {partition.device} ===")
    logging.info(f"  Mountpoint: {partition.mountpoint}")
    logging.info(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    logging.info(f"  Total Size: {get_size(partition_usage.total)}")
    logging.info(f"  Used: {get_size(partition_usage.used)}")
    logging.info(f"  Free: {get_size(partition_usage.free)}")
    logging.info(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
logging.info(f"Total read: {get_size(disk_io.read_bytes)}")
logging.info(f"Total write: {get_size(disk_io.write_bytes)}")
# Network information
logging.info("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        logging.info(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            logging.info(f"  IP Address: {address.address}")
            logging.info(f"  Netmask: {address.netmask}")
            logging.info(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            logging.info(f"  MAC Address: {address.address}")
            logging.info(f"  Netmask: {address.netmask}")
            logging.info(f"  Broadcast MAC: {address.broadcast}")
# get IO statistics since boot
net_io = psutil.net_io_counters()
logging.info(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
logging.info(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
