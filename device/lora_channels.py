from network import LoRa

def configure_channels(lora):
    # remove all the non-default channels
    if lora.frequency() == 868000000:
        min_channel=3
        max_channel=15
    else:
        min_channel=0
        max_channel=72


    for i in range(min_channel, max_channel):
        lora.remove_channel(i)

    if lora.frequency() == 868000000:
        print("Connecting KotahiNet frequency plan")
        dr_min=0
        dr_max=5
        # New KotahiNet band plan
        lora.add_channel(0, frequency=864862500, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(1, frequency=865062500, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(2, frequency=865402500, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(3, frequency=865602500, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(4, frequency=865985000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(5, frequency=866200000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(6, frequency=866400000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(7, frequency=866600000, dr_min=dr_min, dr_max=dr_max)

    else:

        # print("Connecting to AS923")
        #
        # # Uplink
        # dr_min=0
        # dr_max=3
        # lora.add_channel(0, frequency=923200000, dr_min=dr_min, dr_max=dr_max)
        # lora.add_channel(1, frequency=923400000, dr_min=dr_min, dr_max=dr_max)

        print("Connecting to AU_915_928")

        # Uplink
        dr_min=0
        dr_max=3
        lora.add_channel(0, frequency=916800000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(1, frequency=917000000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(2, frequency=917200000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(3, frequency=917400000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(4, frequency=917600000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(5, frequency=917800000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(6, frequency=918000000, dr_min=dr_min, dr_max=dr_max)
        lora.add_channel(7, frequency=918100000, dr_min=dr_min, dr_max=dr_max)
