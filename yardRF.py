import argparse, time, os
from core.subghz import yardstick_rx, yardstick_tx, format_signals, tesla_port
from core.yardstick import configure_stick
from core.jammy import roll_jam
from core.interactive import interactive_mode
from core.output_parser import parse_captured_file, save_signal_output
from core.interactive import menu
from rflib import *

def main():
    parser = argparse.ArgumentParser(description="YardRF is for your capturing/replaying/rolljam fun")
    parser.add_argument('-f', '--frequency', help='Specify frequency to listen on [default: 433.92MHz (433920000)]', default=433920000, type=int)
    parser.add_argument('-m', '--modulation', help='Specify modulation type [default: MOD_ASK_OOK] examples: 2FSK/AM270/AM650/FM238/FM476', default='MOD_ASK_OOK')
    parser.add_argument('-b', '--baudrate', help='Specify sample rate, baudrate [default: 3793] example: 3794', default=3794, type=int)
    parser.add_argument('-d', '--deviation', help='Specify deviation [default: 0] examples: 23803, 47607, 2930', default=0, type=float)
    parser.add_argument('-s', '--channel_spacing', help='Specify Channel Spacing, optional [Default: 25000]', type=int, default=25000)
    parser.add_argument('-cb', '--channel_bandwidth', help='Specify channel bandwidth, optional [default: 0]', default=0, type=int)
    parser.add_argument('-bs', '--blocksize', help='Specify blocksize for packet capture length [default: 250]', default=0, required=False, type=int)
    parser.add_argument('-min', '--minRSSI', help='Specify minimum rssi db to accept signal [default: -40]', default=10, type=int)
    parser.add_argument('-max', '--maxRSSI', help='Specify maximum rssi db to accept signal [default 100]', default=100, type=int)
    parser.add_argument('-amp', '--amp', help='Enable yardstick one amplifier', default=False, action='store_true')
    parser.add_argument('-n', '--number', help='Specify number of signals to send [Default: 1 transmission]', default=1, type=int)
    parser.add_argument('-o', '--output', help='Specify name of output file to replay captured signals [.cap file extension]', required=False)
    parser.add_argument('-c', '--cap', help='Specify cap file to replay previously captured signals', required=False)
    parser.add_argument('-auto', '--auto', help='Enable to automatically send captures/cap files / Use in conjunction with -rj/--rolljam to send the first signal automatically', action='store_true', required=False)
    parser.add_argument('-rpiJ', '--rpitx_jammer', help='Enable jammer with rpitx by specifying rpitx directory [ie. ~/Documents/rpitx]', required=False, type=str)
    parser.add_argument('-ysJ', '--yardstick_jammer', help='Enable jammer with an EXTRA yardstick one', required=False, action='store_true')
    parser.add_argument('-t', '--tesla_port', help='Send tesla charging port signal', required=False, action='store_true')
    parser.add_argument('-i', '--interactive', help='Enter "Interactive" mode [CMD GUI]', required=False, action='store_true')

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
    amp = args.amp
    number = args.number
    output = args.output
    cap = args.cap
    auto = args.auto
    rpitxJ = args.rpitx_jammer
    ysJ = args.yardstick_jammer
    tesla = args.tesla_port
    interactive = args.interactive


    # no medical frequency ranges please
    if (frequency >= 400000000) and (frequency <= 416000000):
        print("[*] Sorry, Medical frequency ranges are NOT permitted..\n")
        exit(0)

    d = RfCat(idx=0) # establish permissions with ys1

    signals = None
    # interactive mode
    if interactive:
        frequency, modulation, deviation, baudrate, bs = interactive_mode(d)
        configure_stick(d, frequency, modulation, baudrate, deviation, channel_bandwidth, channel_spacing, amp, tesla)
        yardstick = yardstick_rx()
        signals = yardstick.capture_signals(d, minRSSI, maxRSSI, bs)
        d.setModeIDLE()
        option = menu('[*] Save signals to output file: ', ['yes', 'no'])
        if 'yes' in option:
            input_file = input("[*] Enter file name [without extension]: ")
            save_signal_output(input_file, frequency, modulation, deviation, baudrate, bs, signals)
        print("[*] Formatting each signal captured..\n")
        payloads = format_signals(signals)
        print("[*] Transmitting signals captured..\n")
        yardstick_tx(d, payloads, True, number)
        d.setModeIDLE()
        interactive_mode(d)
    
    # jam with rpitx or another yardstick one, and stop after signals are captured
    if rpitxJ != None or ysJ:
        signals = roll_jam(rpitxJ, ysJ)
        print("[*] Formatting each signal captured..\n")
        payloads = format_signals(signals)
        print("[*] Transmitting signals captured..\n")
        yardstick_tx(d, payloads, auto, number)
        return True

    if tesla:
        print("[*] Popping charging port..\n")
        configure_stick(d, 315000000, 'MOD_ASK_OOK', 2500, 0, 0, 25000, True, True)
        tesla_port(d)
        configure_stick(d, 433920000, 'MOD_ASK_OOK', 2500, 0, 0, 25000, True, True)
        tesla_port(d)
        return True

    # read from captured file
    if cap:
        frequency, modulation, deviation, baudrate, bs, signals = parse_captured_file(cap)
    
    print(f"[*] Configuring yardstick:\n\n[*] Frequency: {frequency} Modulation: {modulation}\n -> Baudrate: {baudrate} Deviation: {deviation}\n")
    # configure yardstick one with settings
    configure_stick(d, frequency, modulation, baudrate, deviation, channel_bandwidth, channel_spacing, amp, tesla)
    # capture signals
    if signals == None:
        yardstick = yardstick_rx()
        signals = yardstick.capture_signals(d, minRSSI, maxRSSI, bs)
        os.system('clear')
        d.setModeIDLE()

    # if output file is specified, save as filename
    if output:
        save_signal_output(output, frequency, modulation, deviation, baudrate, bs, signals)

    print("[*] Formatting each signal captured..\n")
    payloads = format_signals(signals)
    print("[*] Transmitting signals captured..\n")
    yardstick_tx(d, payloads, auto, number)
    
    d.setModeIDLE()

if __name__=='__main__':
    main()