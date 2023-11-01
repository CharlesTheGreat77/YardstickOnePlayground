from bullet import Bullet
import os, time
from core.cc1101_registers import reset_registers_to_default
from core.subghz import yardstick_rx, yardstick_tx, format_signals, tesla_port
from core.output_parser import parse_captured_file, save_signal_output
from core.yardstick import configure_stick 
from rflib import *

def interactive_mode(d):
    '''
    Function for receiving or transmitting options
    '''
    option = menu('[*] Choose an option: ', ['Receive', 'Transmit', 'Exit'])
    if option == 'Receive':
        frequency, modulation, deviation, baudrate, bs = interactive_configure_stick()
        return int(frequency), modulation, int(deviation), int(baudrate), bs
    elif option == 'Transmit':
        interactive_mode_tx(d)
    else:
        d.setModeIDLE()
        exit(0)


def interactive_configure_stick():
    '''
    Function to set frequency, baudrate, and set registeres to match flipper zeros
    registers
    '''
    # set frequency
    frequency = menu('[*] Choose a frequency: ', ['300000000', '304000000', '310000000', '315000000', '433920000', 'CUSTOM'])
    if frequency == 'CUSTOM':
        frequency = int(input("[*] Enter frequency [433920000]: "))

    # set modulation
    modulation = menu('[*] Choose an option: ', ['MOD_ASK_OOK', 'MOD_2FSK'])
    if 'MOD_ASK_OOK' in modulation:
        deviation = 0
    else:
        deviation = menu('[*] Choose a deviation', ['23803', '47607', '2930', 'CUSTOM'])
        if 'CUSTOM' in deviation:
            deviation = int(input('[*] Enter custom deviation: '))

    # set deviation
    baudrate = menu('[*] Choose a baudrate [Default 3794]: ', ['2000', '2500', '3000', '4000', '4800', 'Default', 'CUSTOM'])
    if 'Default' in baudrate:
        baudrate = 3794
    elif 'CUSTOM' in baudrate:
        baudrate = int(input("[*] Enter baudrate [2000]: "))
    
    # set blocksize
    bs = menu('[*] Choose max blocksize [max size of each capture]: ', ['200', '300', '350', '400','450','Default','CUSTOM'])
    if bs == 'CUSTOM':
        bs = int(input("[*] Enter custom blocksize [max 500]: "))
    elif 'Default' in bs:
        bs = 0
    else:
        bs = 0

    return int(frequency), modulation, int(deviation), int(baudrate), int(bs)


def interactive_mode_tx(d):
    '''
    Function to transmit saved captured files or transmit the tesla
    charging port.
    '''
    option = menu('[*] Choose an option to transmit: ', ['Captured File', 'Tesla Charging Port'])
    if option == 'Captured File':
        input_file = input('[*] Enter path to file: ')
        os.system('clear')
        frequency, modulation, deviation, baudrate, bs, payloads = parse_captured_file(input_file)
        try:
            print(f"[*] Configuring yardstick:\n\n[*] Frequency: {frequency} Modulation: {modulation}\n -> Baudrate: {baudrate} Deviation: {deviation}\n")
            time.sleep(1.5)
            configure_stick(d, int(frequency), modulation, int(baudrate), int(deviation), channel_bandwidth=0, channel_spacing=0, amp=True, tesla=False)
        except Exception as e:
            print("[-] Failed to load file..\n")
            print(e)
    
        print('[*] Formatting signals to bytes..\n')
        payloads = format_signals(payloads)
        yardstick_tx(d, payloads, auto=True, number=1)
    else:
        print("[*] Popping tesla charging port..\n")
        time.sleep(1)
        tesla_port(d)
    interactive_mode(d)


def menu(question, options):
    '''
    Function to interact/choose options using bullet library
    type var: string [question]
    type var: array [options]
    return:
        type var: string [result]
    '''
    os.system('clear')
    cli = Bullet(
            prompt = question,
            choices = [option for option in options],
            indent = 0,
            align = 5,
            margin = 2,
            shift = 0,
            bullet = "",
            pad_right = 5,
            return_index = True
        )
    result = cli.launch()
    os.system('clear')
    return result[0]
