# YardstickOnePlayground
Yardstick One Scripts for your RF Adventures


# Disclaimer
  I am not responsible for the usage of this utility, it is simply for researching and experimentation for myself.
  The user, YOU take full responsibility for your actions. 

# Key Notes
  To use rpitx as a jammer, please be sure you have it INSTALLED!
  - and have an antenna (copper wire) connected to GPIO 4
    -- put the jammer.iq file into the rpitx directory
    -- sendiq IN rpitx needs sudo so be wary of such (for me at least)

# Prerequisite
   rpitx (if using rpitx to jam)
    -- https://github.com/F5OEO/rpitx
       Read at Key Notes

   Two yardstick ones ONLY if using other as jammer for rolljam

# Usage
```
YardRF is for relaying/capturing/jamming/rolljam fun

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
                        examples: 2.380371, 47.60742, 29.30
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
                        conjunction with -rn/--rolljam to
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
