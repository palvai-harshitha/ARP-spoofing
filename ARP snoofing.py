import time
import psutil
from pandas import DataFrame
import logging
from scapy.all import *
import signal
import sys

logging.basicConfig(filename="BAND.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')





def main():
    old_value = 0    

    while True:
        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        if old_value:
            send_stat(new_value - old_value)

        old_value = new_value

        time.sleep(1)

def convert_to_gbit(value):
    return value/1024./1024./1024.*8

def send_stat(value):
   # print ("%0.3f" % convert_to_gbit(value))
    logging.info(psutil.net_io_counters(pernic=True))
    

main()
