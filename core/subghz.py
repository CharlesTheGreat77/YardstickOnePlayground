import bitstring, time
from rflib import *

class yardstick_rx:
    def __init__(self):
        self.signals = []

    def capture_signals(self, d, minRSSI, maxRSSI, bs):
        '''
        Function to capture live signals based on filtering 
        'f' count out of hex data.
        type var: object [d]
        type var: int [minRSSI & maxRSSI]
        type var: int [bs (blocksize)]
        
        returns type var: array
        var name: signals
        '''
        print("[*] Live Packet Capture: \n")
        try:
            while True:
                if bs != 0:
                    capture, _ = d.RFrecv(timeout=1, blocksize=bs)
                else:
                    capture, _ = d.RFrecv()
                cap = capture.hex()
                strength = int(d.getRSSI().hex(), 16)  # RSSI
                #if minRSSI < strength < maxRSSI:
                if cap.count('f') < 300:
                    self.signals.append(cap)
                    print(f"Signal: \033[36m{cap}\033[0m\nRSSI: \033[36m{strength}\033[0m\n")  
        except ChipconUsbTimeoutException:
            pass
        except KeyboardInterrupt:
            raise
        return self.signals


def yardstick_tx(d, payloads, auto, number):
    '''
    Function to transmit signals captured
    : if auto is enabled, enter must be hit for every payload in signals list.
    type var: object [d]
    type var: array [payloads]
    type var: boolean [auto]
    type var: int [number]
    '''
    emptyKey = b'\x00\x00\x00\x00\x00\x00'
    for payload in payloads:
        d.makePktFLEN(len(payload))
        if not auto:
            input('[Enter to transmit]')
        d.RFxmit(payload + emptyKey * number)
        time.sleep(.5)
        #d.RFxmit(payload)
    print("[*] Payload transmittions complete..\n")
    d.setModeIDLE()

def format_signals(signals):
    '''
    Function to format the signals from hex to bytes
    type var: list [signals]
    
    returns type var: array
    var name: payloads
    '''
    payloads = []
    for signal in signals:
        payload = bitstring.BitArray(hex=signal).tobytes()
        payloads.append(payload)

    return payloads


def tesla_port(d):
    '''
    function to send tesla charging port signal at both 315 and 433.92 Mhz
    type var: object [d]
    # Credits to pickeditmate
    # -> https://github.com/pickeditmate

    '''
    d.RFxmit(b'\x15\x55\x55\x51\x59\x4C\xB5\x55\x52\xD5\x4B\x4A\xD3\x4C\xAB\x4B\x15\x94\xCB\x33\x33\x2D\x54\xB4\x56\x9A\x65\x5A\x48\xAC\xC6\x59\x99\x99\x69\xA5\xB2\xB4\xD4\x2A\xD2\x80' * 5)
    d.setModeIDLE()
