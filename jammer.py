from rflib import *
import argparse
from time import time

def main():
    parser = argparse.ArgumentParser(description="Replay Attacks for YardStick One")
    parser.add_argument('-f', '--frequency', help='Specify frequency to jam on [Nine Digits for the freq.] example: 315000000, 433920000')
    parser.add_argument('-b', '--baudrate', help='Specify the baudrate (how long each bit is transmitted for) [default: 4800] example: 4000', default=4800)
    parser.add_argument('-cb', '--channel_bandwidth', help='Specify the channel bandwidth [default: 60000]', default=60000)
    parser.add_argument('-s', '--channel_spacing', help='Specify the channel spacing [default: 24000]', default=24000)

    args = parser.parse_args()
    frequency = args.frequency
    channel_bandwidth = args.channel_bandwidth
    channel_spacing = args.channel_spacing

    print("[*] Setting Up Configuration Settings..")
    time.sleep(2)
    d = setup(frequency, channel_bandwidth, channel_spacing)
    jam(d)

def setup(frequency, channel_bandwidth, channel_spacing):
    d = RfCat()
    d.setFreq(frequency)
    d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmDRate(baudrate)
    d.setMdmChanBW(channel_bandwidth)
    d.setMdmChanSpc(channel_spacing)
    d.setMaxPower()
    return d

def jam(d):
    input("[PRESS ENTER TO START JAMMER]\n")
    try:
        print("[JAMMING]")
        print("[*] CTRL-C to Stop Jamming")
        d.setModeTX()
    except KeyboardInterrupt:
        d.setModeIDLE()
        print("[-] Jammer off.. all done ;)")
        exit(0)
    

main()
