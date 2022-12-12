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
YardRF is for capturing/replaying/rolljam fun

optional arguments:
  -h, --help            show this help message and exit
  -f FREQUENCY, --frequency FREQUENCY
                        Specify frequency to listen on
                        [default: 433.92MHz (433920000)]
  -m MODULATION, --modulation MODULATION
                        Specify modulation type [default:
                        ASK_OOK] example: 2fsk
  -b BAUDRATE, --baudrate BAUDRATE
                        Specify sample rate, baudrate
                        [default: 4800] example: 4000
  -d DEVIATION, --deviation DEVIATION
                        Specify deviation [default: 0]
                        examples: 23803.71, 47607.42, 2930
  -s CHANNEL_SPACING, --channel_spacing CHANNEL_SPACING
                        Specify Channel Spacing [Default:
                        24000]
  -cb CHANNEL_BANDWIDTH, --channel_bandwidth CHANNEL_BANDWIDTH
                        Specify channel bandwidth [default:
                        60000]
  -bs BLOCKSIZE, --blocksize BLOCKSIZE
                        Specify capture blocksize [default:
                        400]
  -min MINRSSI, --minRSSI MINRSSI
                        Specify minimum rssi db to accept
                        signal [default: -100]
  -max MAXRSSI, --maxRSSI MAXRSSI
                        Specify maximum rssi db to accept
                        signal [default 40]
  -n NUMBER, --number NUMBER
                        Specify number of signals to send
                        [Default: 1 transmission]
  -o OUTPUT, --output OUTPUT
                        Specify name of output file to
                        replay captured signals [.cap file
                        extension]
  -c CAP, --cap CAP     Specify cap file to replay
                        previously captured signals
  -l LIMIT, --limit LIMIT
                        Specify capture limit [Default 2]
  -rj, --rolljam        Enable to send 1st capture, THEN
                        second whenever specified
  -a, --auto            Enable to automatically send
                        captures/cap files / Use in
                        conjunction with -rj/--rolljam to
                        send the first signal automatically
  --lowball             enable lowball (noise)
  -rpiJ RPITX_JAMMER, --rpitx_jammer RPITX_JAMMER
                        Enable jammer with rpitx by
                        specifying rpitx directory [ie.
                        ~/Documents/rpitx]
  -ysJ, --yardstick_jammer
                        Enable jammer with an EXTRA
                        yardstick one
```

# Usage for yardRF
```
python3 yardRF.py -f 300000000 -l 2 -n 1 -rj --lowball -o unlock.cap
```
-- captures signals on frequency 300MHz, waits for 2 signals (-l/--limit), send the signals only once (-n/--number), rolljam enabled (so send the first capture only, THEN other captures), --lowball to capture some noise, -o saves the capture to a file (-o/--output). 

```
python3 yardRF.py -f 315000000 -l 2 -n 1 -d 47607.42 -m 2fsk -a
```
-- captures signals on frequency 315MHz, waits for 2 signals (-l/--limit), send the signals captured only once (-n/--number), set the deviation to 47607.42 (-d/--deviation), set modulation to 2fsk [default: ASK_OOK] (-m/--modulation), automatically send captued signals (-a/--automatic).
```
python3 yardRF.py -f 925000000 -l 2 -n 1 -cb 60000 -bs 200 -o unlock.cap
```
-- captures signals on frequency 925MHz, waits for 2 signals (-l/--limit), send the signals only once (-n/--number), set channel bandwidth to 60000 (-cb/--channel_bandwidth), set the blocksize [size of the capture/payload] (-bs/--blocksize), save captures to a file (-o/--output).

• Usage with jammers
rpitx usage
```
python3 yardRF.py -f 433920000 -l 2 -n 1 -rpiJ ~/rpitx/ -m 2fsk -d 47607.42 -o unlock.cap
```
-- captures signals on frequency 433.92MHz, waits for 2 signals (-l/--limit), send the signals only once (-n/--number), use rpitx for jammer by specifying the path to rpitx (-rpiJ/--rpitx_jammer), set the modulation to 2fsk [default: ASK_OOK] (-m/--modulation), we setting the deviation to 47607.42 (-d/--deviation), save captures to a file(-o/--output)

Extra Yardstick One Jammer
```
python3 yardRF.py -f 305000000 -l 2 -n 1 -ysJ -o unlock.cap
```
-- captures signals on frequency 305MHz, waits for 2 signals (-l/--limit), send the signals only once (-n/--number), use additional yardstick one to jam (-ysJ/--yardstick_jammer), set the modulation to 2fsk [default: ASK_OOK] (-m/--modulation), save captures to a file(-o/--output)

# Honorable Mention(s)
- https://github.com/cclabsInc/RFCrack
