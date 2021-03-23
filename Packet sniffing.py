from scapy.all import *
import signal
import sys
import time
import logging
logging.basicConfig(filename="tcp.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

pkts = sniff(count=550)
print(pkts)
print(pkts.summary())