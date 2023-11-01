from rflib import *

def configure_stick(d, frequency, modulation, baudrate, deviation, channel_bandwidth, channel_spacing, amp, tesla):
    '''
    Function to configure yardstick one with settings set by user
    type var: object [d]
    type var: int [frequency]
    type var: string [modulation]
    type var: int [baudrate]
    type var: int [deviation]
    type var: int [channel_bandwidth]
    type var: int [channel_spacing]
    type var: boolean [amp]
    type var: boolean [tesla]
    '''
    d.setFreq(frequency)
    if modulation == "MOD_ASK_OOK" or modulation == "ASK_OOK":
        d.setMdmModulation(MOD_ASK_OOK) # my vehicle used 2fsk but may be ASK/OOK for older cars
    else:
        d.setMdmModulation(MOD_2FSK)
    d.setMdmDRate(baudrate)
    if channel_bandwidth != 0:
        d.setMdmChanBW(channel_bandwidth)
    else:
        d.calculatePktChanBW()
    d.setMdmSyncMode(0)
    d.setChannel(0)
    if (deviation != 0):
        d.setMdmDeviatn(deviation) # for my vehicle, my deviation needed to he 4760, but 2930 is also what I have seen work on other vehicles
    if amp:
        d.setAmpMode(1)
    if tesla != True:
        d.lowball(0) # allow all signals (noise)


