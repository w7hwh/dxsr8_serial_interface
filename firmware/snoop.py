"""
snoop.py

 last edit: 20250721 2120 hrs by hwh

 edit history:


 todo:
    add radio decodes

"""
VERSION="v0.3"

MONITOR     = 1        # 0=head, 1=radio, 2=both

SHOW_LINE   = True

SHOW_HEAD_READY  = False
DECODE_HEAD_SWDS = False
DECODE_HEAD_SWDR = False
DECODE_HEAD_SWDA = False
DECODE_HEAD_SWDV = False

SHOW_RADIO_READY = True
SHOW_RADIO_LCSA  = True
DECODE_RADIO_xxx = False
DECODE_RADIO_yyy = False
DECODE_RADIO_zzz = False

import select
import sys
import time
from machine import Pin, UART, I2C
#import sh1106

from dxsr8 import *
from dxsr8_head import decode_head
import dxsr8_screen

dxsr8=dxsr8()

led = dxsr8.led

print("DXSR8 Snoop", VERSION)

dxsr8.display.fill(0)
dxsr8.display.text("DXSR8 Snoop", 0, display_line(0))
if MONITOR == 0:
    dxsr8.display.text("head2radio only", 0, display_line(3))
elif MONITOR == 1:
    dxsr8.display.text("radio2head only", 0, display_line(3))
elif MONITOR == 2:
    dxsr8.display.text("head and radio", 0, display_line(3))
else:
    dxsr8.display.text(f"MONITOR={MONITOR}?", 0, display_line(3))

dxsr8.display.text(VERSION, 0, display_line(7))
dxsr8.display.show()

curline = ""

if MONITOR == 2:
    TAGHEAD  ="head  : %s"
    TAGRADIO ="radio : %s"
else:
    TAGHEAD  ="%s"
    TAGRADIO ="%s"

while True:

    if (MONITOR==0 or MONITOR==2):
        # packets from head to chassis
        if dxsr8.head_poll_obj.poll(0):
            x = dxsr8.head_uart.readline()
            
            if SHOW_LINE:
                print(TAGHEAD % x)

            if SHOW_HEAD_READY:
                if x.startswith("AL~READY"):
                    print("got AL~READY")

            if DECODE_HEAD_SWDS:
                if x.startswith("SWDS"):
                    print("KEYS DOWN: " + str(decode_head.decode_SWDS(x)))

            if DECODE_HEAD_SWDR:
                if x.startswith("SWDR"):
                    print("SWDR: " + str(decode_head.decode_SWDR(x)))

            if DECODE_HEAD_SWDA:
                if x.startswith("SWDA"):
                    print("SWDA: " + str(decode_head.decode_SWDA(x)))

            if DECODE_HEAD_SWDV:
                if x.startswith("SWDV"):
                    print("SWDV: " + str(decode_head.decode_SWDV(x)))

            dxsr8.head_uart.write(x)      # pass it on to the radio

    if MONITOR==1 or MONITOR==2:
        # packets from chassis to head
        if dxsr8.radio_poll_obj.poll(0):
            x = dxsr8.radio_uart.readline()
            if SHOW_LINE:
                print(TAGRADIO % x)

            if SHOW_RADIO_READY:
                if x.startswith("AL~READY"):
                    print("got AL~READY")

            if SHOW_RADIO_LCSA:
                if x.startswith("LCSA"):
                    print("got LCSA")

            
            dxsr8.radio_uart.write(x)      # pass it on to the head
        
    led.toggle()                 # toggle led so we can see it's running
    time.sleep(0.2)
