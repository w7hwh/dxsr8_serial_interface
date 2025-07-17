"""
snoop.py

 last edit: 20250717 1223 hrs by hwh

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
import sh1106

from dxsr8_config import dxsr8_config
from dxsr8_head import decode_head
import dxsr8_screen

dxsr8_config=dxsr8_config()

led = dxsr8_config.led

#,rxbuf=1024
head_uart = UART(1, baudrate=dxsr8_config.baud_rate, tx=dxsr8_config.head_tx_pin, rx=dxsr8_config.head_rx_pin, rxbuf=dxsr8_config.rxbuf)
head_uart.init(bits=dxsr8_config.bits, parity=dxsr8_config.parity, stop=dxsr8_config.stop)
head_poll_obj = select.poll()
head_poll_obj.register(head_uart,select.POLLIN)

radio_uart = UART(0, baudrate=dxsr8_config.baud_rate, tx=dxsr8_config.radio_tx_pin, rx=dxsr8_config.radio_rx_pin, rxbuf=dxsr8_config.rxbuf)
radio_uart.init(bits=dxsr8_config.bits, parity=dxsr8_config.parity, stop=dxsr8_config.stop)
radio_poll_obj = select.poll()
radio_poll_obj.register(radio_uart,select.POLLIN)

i2c = I2C(scl=dxsr8_config.display_scl_pin, sda=dxsr8_config.display_sda_pin, freq=400000)
# display is 128x64 giving 8 lines of 16 characters
display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
display.sleep(False)
display.rotate(True)

def display_line(x):
    return x * 8

print(head_uart)

print("DXSR8 Snoop", VERSION)
print("head2radio only")

display.fill(0)
display.text("DXSR8 Snoop", 0, display_line(0))
if MONITOR == 0:
    display.text("head2radio only", 0, display_line(3))
elif MONITOR == 1:
    display.text("radio2head only", 0, display_line(3))
elif MONITOR == 2:
    display.text("head and radio", 0, display_line(3))
else:
    display.text(f"MONITOR={MONITOR}?", 0, display_line(3))

display.text(VERSION, 0, display_line(7))
display.show()

curline = ""

if MONITOR == 2:
    TAGHEAD  ="head:%s"
    TAGRADIO ="rad :%s"
else:
    TAGHEAD  ="%s"
    TAGRADIO ="%s"

while True:

    if (MONITOR==0 or MONITOR==2):
        # packets from head to chassis
        if head_poll_obj.poll(0):
            x = head_uart.readline()
            
            if SHOW_LINE:
                print(TAGHEAD % x)

            if SHOW_HEAD_READY:
                if x.startswith("AL~READY"):
                    print("AL~READY")

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

            head_uart.write(x)      # pass it on to the radio

    if MONITOR==1 or MONITOR==2:
        # packets from chassis to head
        if radio_poll_obj.poll(0):
            x = radio_uart.readline()
            if SHOW_LINE:
                print(TAGRADIO % x)

            if SHOW_RADIO_READY:
                if x.startswith("AL~READY"):
                    print("AL~READY")

            if SHOW_RADIO_LCSA:
                if x.startswith("LCSA"):
                    print("got LCSA")

            
            radio_uart.write(x)      # pass it on to the head
        
    led.toggle()                 # toggle led so we can see it's running
    time.sleep(0.1)
