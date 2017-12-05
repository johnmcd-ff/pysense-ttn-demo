# Start main usercode
import binascii
import pycom
import socket
import time
from network import LoRa
import machine
from network import WLAN
from machine import Pin
import keys
import struct

if __name__ == '__main__':

    # Colors
    off = 0x000000
    red = 0xff0000
    green = 0x00ff00
    blue = 0x0000ff


    # Turn off hearbeat LED
    pycom.heartbeat(False)

    # connect to DorisNet
    wlan = WLAN(mode=WLAN.STA)

    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'YOUR_WIFI_SSID':
            print(net.ssid + ' found!')
            wlan.connect(net.ssid, auth=(net.sec, 'YOUR_WIFI_PASSWORD'), timeout=5000)
            connectingToWiFi = True
            break

        if net.ssid == 'DorisNet':
            print(net.ssid + ' found!')
            wlan.connect(net.ssid, auth=(net.sec, '4lawnmix'), timeout=5000)
            connectingToWiFi = True
            break

    if connectingToWiFi:
        while not wlan.isconnected():
            pycom.rgbled(green)
            time.sleep(0.1)
            pycom.rgbled(off)
            time.sleep(1) # save power while waiting
        print('WLAN connection succeeded!')

    # get the EUI
    lora = LoRa()
    print("LoRa EUI:", binascii.hexlify(lora.mac()))

    #get the IP on the WiFi
    print("IP:", wlan.ifconfig()[0])
    print("Try  typing a command like os.uname()")
    print("Run the LoRa OTAA demo execfile(\"otaa.py\")")
    print("Run the Pysense TTN demo execfile(\"pysense_demo.py\")")
    print("\n\nHit ctrl+c to stop auto booting the pysense demo...\n\n")

    for i in range(1,10):
        time.sleep(1)

    execfile("pysense_demo.py")
