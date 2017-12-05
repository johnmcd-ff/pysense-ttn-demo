# See https://docs.pycom.io for more information regarding library specifics

from network import LoRa
import socket
import binascii
import struct
import keys
import lora_channels

from ipso_messages import Messages

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

# join a network using OTAA (Over the Air Activation)
lora = LoRa(mode=LoRa.LORAWAN)
app_eui = keys.get_app_eui(lora)
app_key = keys.get_app_key(lora)
lora_channels.configure_channels(lora)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    print('Waiting to join...')
    pycom.rgbled(red)
    time.sleep(0.1)
    pycom.rgbled(off)
    time.sleep(2)

pycom.heartbeat(False)
lora_channels.configure_channels(lora)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(True)

button = Pin("G17",  mode=Pin.IN,  pull=Pin.PULL_UP)


while(1):
    print("Battery Voltage: ", py.read_battery_voltage())
    print("Altitude: ", mp.altitude())
    print("Pressure: ", mpp.pressure())
    print("Temperature: ", si.temperature())
    print("Humidity: ", si.humidity())
    print("Light: ", lt.light())
    print("Acceleration: ", li.acceleration())
    print("Roll: ", li.roll())
    print("Pitch: ", li.pitch())

    payload = Messages.build_ipso_message(
            py.read_battery_voltage(),
            mpp.pressure(),
            si.temperature(),
            lt.light()[0],
            si.humidity(),
            li.acceleration())

    print("TX:", binascii.hexlify(payload))
    print("TX len: ", len(payload))

    s.send(payload)
    pycom.rgbled(green)
    time.sleep(0.1)
    pycom.rgbled(off)
    time.sleep(1)
    if(button() == 0):
        s.send(Messages.build_short_status(0,1))
        pycom.rgbled(red)

    for i in range(1,10):
        time.sleep(1)    # wait 10 sec for next sample
