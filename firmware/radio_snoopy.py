"""
radio_snoopy.py

 Looks at what the radio chassis is sending to the head.
 
 original written by Josh, AJ9BM
 see https://github.com/jbm9/dxsr8_serial

 last edit: 20250721 2055 hrs by hwh


 edit history:


"""
VERSION="v0.4"

SHOW_LINE          = True
SHOW_COUNT         = True
USE_HEXBYTES       = True

SHOW_RADIO_READY   = False
SHOW_RADIO_LCSA    = False
SHOW_RADIO_STATE   = False
DECODE_RADIO_STATE = True

LCSA_LENGTH        = 34

import select
import time
from machine import Pin #, UART, I2C
from dxsr8_screen import *
from dxsr8 import *
from utility import *

dxsr8=dxsr8()

led = dxsr8.led


fdisp         = FrequencyDisplay()
mdisp         = ModeDisplay()
rfdisp        = RFPowerDisplay()
agcdisp       = AGCDisplay()
smeterdisp    = SMeterDisplay()
backlightdisp = BacklightDisplay()
miscdisp      = MiscDisplay()


def decode_state(sin):
    #print(hexBytes2(sin))
   
    if not sin.startswith("LCSA"):
        return
        
    try:
        mode   = mdisp.decode(sin)
        agc    = agcdisp.decode(sin)
        rf     = rfdisp.decode(sin)
        smeter = smeterdisp.decode_string(sin)
        
        if fdisp.is_freq(sin):
            freq = fdisp.freq(sin)
        else:
            freq2 = fdisp.decode(sin)

        misc = miscdisp.decode(sin)
        bl   = backlightdisp.decode(sin)
        
    except (Exception) as e:
        print()
        print("Caught exception: " + str(e))
        print()
        print("Input %s" % (sin))
        print("Input %s" % hexBytes2(sin))
        print()


def print_state(sin):
    #print(hexBytes2(sin))
   
    if not sin.startswith("LCSA"):
        return
        
    try:
        mode = mdisp.decode(sin)
        
        rxstate = "%s RF:%+2d %s" % (agcdisp.decode(sin), rfdisp.decode(sin), smeterdisp.decode_string(sin))
        
        line = ""

        if fdisp.is_freq(sin):
            line += "[%s] f = %s %s" % (mode, intWithCommas(fdisp.freq(sin)), rxstate)
        else:
            line += "[%s] > %s < %s" % (mode, fdisp.decode(sin), rxstate)

        line += str(sorted(miscdisp.decode(sin)))

        line += " <BL%2d>" % backlightdisp.decode(sin) # if you care about the backlight intensity.

        #print(line)
        
    except (Exception) as e:
        print()
        print("Caught exception: " + str(e))
        print()
        print("Input %s" % (sin))
        print("Input %s" % hexBytes2(sin))
        print()


def print_bit_header():
    print('-'*((LCSA_LENGTH*3)-1))
    for i in range(LCSA_LENGTH):
        print("%2d" % ((i*8)//100), end = ' ')
    print()
    for i in range(LCSA_LENGTH):
        print("%02d" % ((i*8)%100), end = ' ')
    print()
    print('-'*((LCSA_LENGTH*3)-1))


print("Radio Snoopy", VERSION)
print("radio2head only")

dxsr8.display.fill(0)
dxsr8.display.text("Radio Snoopy", 0, display_line(0))
dxsr8.display.text("radio2head only", 0, display_line(3))
dxsr8.display.text(VERSION, 0, display_line(7))
dxsr8.display.show()

curline = b""

if SHOW_LINE:
    print_bit_header()
    
while True:
    led.toggle()
    
    if dxsr8.radio_poll_obj.poll(0):
        x = dxsr8.radio_uart.read()
        curline += x
        
        if SHOW_LINE:
            if SHOW_COUNT:
                print("---> read %d bytes" % len(x))
            if USE_HEXBYTES:
                print(hexBytes(x))
            else:
                print(x)

        if -1 != curline.find(b"AL~READY"):
            if SHOW_RADIO_READY:
                print("GOT AL~READY.")
            n = curline.find(b"AL~READY")
            curline = curline[n+8+1:]
        
        if 1 <= curline.find(b"LCSA"):
            if SHOW_RADIO_LCSA:
                print("SEEK to LCSA: %d" % curline.find(b"LCSA"))
                print()
            n = curline.find(b"LCSA")
            # send the part before LCSA on to the head
            dxsr8.radio_uart.write(curline[0:n])
            # remove that part from the buffer
            curline = curline[n:]
        
        while len(curline) >= LCSA_LENGTH:
            if SHOW_RADIO_STATE:
                print_state(curline[0:LCSA_LENGTH])
            if DECODE_RADIO_STATE:
                decode_state(curline[0:LCSA_LENGTH])
            dxsr8.radio_uart.write(curline[0:LCSA_LENGTH])
            curline = curline[LCSA_LENGTH:]
        