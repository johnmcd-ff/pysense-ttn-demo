import binascii
from network import LoRa


def get_app_eui(lora):
    my_mac = binascii.hexlify(lora.mac())
    if my_mac == b'70b3d54991ec9977':
        app_eui = '70B3D57ED0006DFF'
    else:
        print ("Unknown Device EUI")
        app_eui = 0

    return binascii.unhexlify(app_eui)


def get_app_key(lora):
    my_mac = binascii.hexlify(lora.mac())
    if my_mac == b'70b3d54991ec9977':
        app_key = 'A15A8613A3B800CA36F29D44D33F7EB7'
    else:
        print ("Unknown Device EUI")
        app_key = 0

    return binascii.unhexlify(app_key)
