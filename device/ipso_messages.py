"""
`ipso_messages`
====================================================

IPSO Communicatations driver for generating payload data
to publish sensor data to myDevices using Cayenne LPP

* Author(s): virtualguy
"""
import time, math
from micropython import const
import struct
import json

LPP_DIGITAL_INPUT     = const(0)       # 1 byte
LPP_DIGITAL_OUTPUT    = const(1)       # 1 byte
LPP_ANALOG_INPUT      = const(2)       # 2 bytes, 0.01 signed
LPP_ANALOG_OUTPUT     = const(3)       # 2 bytes, 0.01 signed
LPP_LUMINOSITY        = const(101)     # 2 bytes, 1 lux unsigned
LPP_PRESENCE          = const(102)     # 1 byte, 1
LPP_TEMPERATURE       = const(103)     # 2 bytes, 0.1°C signed
LPP_RELATIVE_HUMIDITY = const(104)     # 1 byte, 0.5% unsigned
LPP_ACCELEROMETER     = const(113)     # 2 bytes per axis, 0.001G
LPP_BAROMETRIC_PRESSURE = const(115)     # 2 bytes 0.1 hPa Unsigned
LPP_GYROMETER         = const(134)     # 2 bytes per axis, 0.01 °/s
LPP_GPS               = const(136)     # 3 byte lon/lat 0.0001 °, 3 bytes alt 0.01m

class Messages:
    def build_short_status(battery, status_flags):
        """Generate message 0x01 - Short Status"""
        for v in battery, status_flags:
            v = clamp(v, 0, 255)

        payload = struct.pack("<BBB", 0x01, battery, status_flags)
        return payload

    def build_ipso_message(battery, pressure, temperature, light, humidity, acceleration):
        """Generate message IPSO Message"""

        humidity = humidity * 2
        humidity = clamp(humidity, 0, 0xff)

        pressure = pressure / 10
        pressure = clamp(pressure, 0, 0xffff)

        battery = battery * 100
        battery = clamp(battery, 0, 0xffff)

        light = clamp(light, 0, 0xffff)

        acceleration_x = clamp(acceleration[0] * 1000, -30000, 30000)
        acceleration_y = clamp(acceleration[1] * 1000, -30000, 30000)
        acceleration_z = clamp(acceleration[2] * 1000, -30000, 30000)

        # temperature is scaled by 10 and is signed
        temperature = temperature * 10
        temperature = clamp(temperature,-30000, 30000)

        # send using Cayenne Low Power Protocol(LPP) NB: big endian format
        payload = struct.pack(">BBhBBHBBhBBHBBBBBhhh",
            0x01, LPP_ANALOG_INPUT, battery,
            0x02, LPP_BAROMETRIC_PRESSURE, pressure,
            0x03, LPP_TEMPERATURE, temperature,
            0x04, LPP_LUMINOSITY, light,
            0x05, LPP_RELATIVE_HUMIDITY, humidity,
            0x06, LPP_ACCELEROMETER, acceleration_x, acceleration_y, acceleration_z)

        return payload

def clamp(n, minn, maxn):
    """Ensure n falls between range"""
    n = int(n)
    return max(min(maxn, n), minn)
