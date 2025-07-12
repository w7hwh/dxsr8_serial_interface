"""
dxsr8_config.py

 last edit: 20250710 1920 hrs by hwh

 edit history:


 todo:


"""
from machine import Pin

class dxsr8_config():
    
    led=Pin("LED", Pin.OUT)
    
    baud_rate=38400
    bits=8
    parity=None
    stop=2
    
    # Pin numbers for head to radio
    head_rx_pin=Pin(5)
    head_tx_pin=Pin(4)
    
    # Pin numbers for radio to head
    radio_rx_pin=Pin(13)
    radio_tx_pin=Pin(12)
    
    # Pin numbers for display
    display_scl_pin=Pin(17)
    display_sda_pin=Pin(16)

