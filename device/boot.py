# boot.py -- run on boot-up
import os
import time
from machine import UART
uart = UART(0, 115200)
os.dupterm(uart)
