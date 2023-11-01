# YardstickOnePlayground
Yardstick One Scripts for your RF Adventures
![00DEA4C9-2C54-43AB-953D-E68D4F0A9D72](https://user-images.githubusercontent.com/27988707/207140390-7b5ed47b-d0ec-4821-8831-7253384973a3.jpeg)


# Disclaimer
  I am not responsible for the usage of this utility, it is simply for researching and experimentation for myself.
  The user, YOU take full responsibility for your actions. 

# Prerequisite
   Python3/2
   One Yardstick one minimum (rfcat installed)

# Optional Settings
   If you are using a raspberry pi to do your duties
   1. RaspAP to connected to rpi w/o internet (create ap)
      -- https://raspap.com

   2. rpitx (if using rpitx to rolljam)
     -- https://github.com/F5OEO/rpitx
        Read Key Notes 

   3. Two yardstick ones ONLY if using for rolljam
   
# Key Notes
  To use rpitx for rolljam attacks, please be sure you have it INSTALLED!
  
  - and have an antenna (copper wire) connected to GPIO 4

    -- put the jammer.iq file into the rpitx directory (I got lazy so do it for me)

    -- sendiq IN rpitx needs sudo so be wary of such (for me at least)

# Usage
```
usage: yardRF.py [-h] [-f FREQUENCY] [-m MODULATION] [-b BAUDRATE] [-d DEVIATION]
                 [-s CHANNEL_SPACING] [-cb CHANNEL_BANDWIDTH] [-bs BLOCKSIZE] [-min MINRSSI]
                 [-max MAXRSSI] [-amp] [-n NUMBER] [-o OUTPUT] [-c CAP] [-auto]
                 [-rpiJ RPITX_JAMMER] [-ysJ] [-t] [-i]

YardRF is for your capturing/replaying/rolljam fun

options:
  -h, --help            show this help message and exit
  -f FREQUENCY, --frequency FREQUENCY
                        Specify frequency to listen on [default: 433.92MHz (433920000)]
  -m MODULATION, --modulation MODULATION
                        Specify modulation type [default: MOD_ASK_OOK] examples:
                        2FSK/AM270/AM650/FM238/FM476
  -b BAUDRATE, --baudrate BAUDRATE
                        Specify sample rate, baudrate [default: 3793] example: 3794
  -d DEVIATION, --deviation DEVIATION
                        Specify deviation [default: 0] examples: 23803, 47607, 2930
  -s CHANNEL_SPACING, --channel_spacing CHANNEL_SPACING
                        Specify Channel Spacing, optional [Default: 25000]
  -cb CHANNEL_BANDWIDTH, --channel_bandwidth CHANNEL_BANDWIDTH
                        Specify channel bandwidth, optional [default: 0]
  -bs BLOCKSIZE, --blocksize BLOCKSIZE
                        Specify blocksize for packet capture length [default: 250]
  -min MINRSSI, --minRSSI MINRSSI
                        Specify minimum rssi db to accept signal [default: -40]
  -max MAXRSSI, --maxRSSI MAXRSSI
                        Specify maximum rssi db to accept signal [default 100]
  -amp, --amp           Enable yardstick one amplifier
  -n NUMBER, --number NUMBER
                        Specify number of signals to send [Default: 1 transmission]
  -o OUTPUT, --output OUTPUT
                        Specify name of output file to replay captured signals [.cap file
                        extension]
  -c CAP, --cap CAP     Specify cap file to replay previously captured signals
  -auto, --auto         Enable to automatically send captures/cap files / Use in conjunction
                        with -rj/--rolljam to send the first signal automatically
  -rpiJ RPITX_JAMMER, --rpitx_jammer RPITX_JAMMER
                        Enable jammer with rpitx by specifying rpitx directory [ie.
                        ~/Documents/rpitx]
  -ysJ, --yardstick_jammer
                        Enable jammer with an EXTRA yardstick one
  -t, --tesla_port      Send tesla charging port signal
  -i, --interactive     Enter "Interactive" mode [CMD GUI]

```

# Usage for yardRF
```
python3 yardRF.py -tesla US [change to EU or anything else for other countries]
```
-- sends the signal to open teslas charging port on frequency 315MHz (US frequency range for tesla port)
```
python3 yardRF.py -f 300000000 -l 2 -n 1 -rj --lowball -o unlock.cap
```
-- captures signals on frequency 300MHz, waits for 2 signals (-l/--limit), send the signals only once (-n/--number), rolljam enabled (so send the first capture only, THEN other captures), --lowball to capture some noise, -o saves the capture to a file (-o/--output). 

```
python3 yardRF.py -f 315000000 -l 2 -n 1 -d 2930 -m 2fsk -a
```
-- captures signals on frequency 315MHz, waits for 2 signals (-l/--limit), send the signals captured only once (-n/--number), set the deviation to 2930 [29.30] (-d/--deviation), set modulation to 2fsk [default: ASK_OOK] (-m/--modulation), automatically send captued signals (-a/--automatic).
```
python3 yardRF.py -f 925000000 -l 2 -n 1 -cb 60000 -bs 200 -o unlock.cap
```
-- captures signals on frequency 925MHz, waits for 2 signals (-l/--limit), send the signals only once (-n/--number), set channel bandwidth to 60000 (-cb/--channel_bandwidth), set the blocksize [size of the capture/payload] (-bs/--blocksize), save captures to a file (-o/--output).
```
python3 yardRF.py -f 330000000 -l 5 -n 1 -minRSSI -80 -maxRSSI 20 -b 4000 -o output.cap
```
-- captures signals on frequency 300MHz, waits for 5 signals (-l/--limit), sets minimum signal strength to -80 db [used in conjunction with --maxRSSI to only capture signals between a certain range] (-minRSSI, --minRSSI), set maximum signal strength of 40 db (-maxRSSI/--maxRSSI), set baudrate to 4000 [how long each bit is transmitted for] (-b/--baudrate), save captured signals to an output file (-o/--output)

• Usage with rpitx & extra yardstick for rolljam

rpitx usage -- see Key Notes for setup
```
python3 yardRF.py -f 433920000 -l 2 -n 1 -rpiJ ~/rpitx/ -m 2fsk -d 47607.42 -o unlock.cap
```
-- captures signals on frequency 433.92MHz, waits for 2 signals (-l/--limit), send the signals only once (-n/--number), use rpitx for jammer by specifying the path to rpitx (-rpiJ/--rpitx_jammer), set the modulation to 2fsk [default: ASK_OOK] (-m/--modulation), we setting the deviation to 47607.42 [47.60742] (-d/--deviation), save captured signals to a file (-o/--output)

Extra Yardstick One rolljam usage
```
python3 yardRF.py -f 305000000 -l 2 -n 1 -ysJ -m 2fsk -o unlock.cap
```
-- captures signals on frequency 305MHz, waits for 2 signals (-l/--limit), send the signals only once (-n/--number), use additional yardstick one to jam (-ysJ/--yardstick_jammer), set the modulation to 2fsk [default: ASK_OOK] (-m/--modulation), save captures to a file (-o/--output)

* If jamming signal is all thats being captured, be sure to adjust the offset frequency as necessary on line 90 & 93 IF using extra yardstick one OR line 192 & 194 IF using rpitx

# Honorable Mention(s)
- https://github.com/cclabsInc/RFCrack
- https://github.com/pickeditmate
