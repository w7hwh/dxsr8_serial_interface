# snoop.py
#
# last edit: 20250708 1500 hrs by hwh
#
# edit history:
#
#
import select
import sys
import time
from machine import Pin, UART
import decode_head
import decode_screen

BAUD_RATE=38400

# Pin numbers for head to chassis
head_rx_pin=Pin(5)
head_tx_pin=Pin(4)

# Pin numbers for chassis to head
chassis_rx_pin=Pin(13)
chassis_tx_pin=Pin(12)


head_uart = UART(1, baudrate=BAUD_RATE, tx=head_tx_pin, rx=head_rx_pin)
head_uart.init(bits=8, parity=None, stop=2)
head_poll_obj = select.poll()
head_poll_obj.register(head_uart,select.POLLIN)

chassis_uart = UART(0, baudrate=BAUD_RATE, tx=chassis_tx_pin, rx=chassis_rx_pin)
chassis_uart.init(bits=8, parity=None, stop=2)
chassis_poll_obj = select.poll()
chassis_poll_obj.register(chassis_uart,select.POLLIN)

#led=machine.Pin("LED",machine.Pin.OUT)

dh = decode_head


print("DXSR8 Snoop - currently looking at head to chassis only")

curline = ""

while True:
    if head_poll_obj.poll(0):
        x = head_uart.readline()
        print("head:", x)

        if x.startswith("SWDS"):
            print("KEYS DOWN: " + str(dh.decode_SWDS(x)))

        head_uart.write(x)      # pass it on to the chassis

    if chassis_poll_obj.poll(0):
        x = chassis_uart.readline()
        print("chassis:", x)

        chassis_uart.write(x)      # pass it on to the head
        
    time.sleep(0.1)

ser.close()
