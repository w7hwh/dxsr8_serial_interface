#!/usr/bin/env python3
"""
bit_documentation.py

 last edit: 20250723 1649 hrs by hwh

 edit history:


 todo:

"""
from datetime import datetime

now = datetime.now()
now_formatted = now.strftime("%B %d %Y %H:%M:%S")

#------------------------------------------------------    
class Bits:
    def __init__(self, start, length):
        self.start  = start
        self.length = length


lcsa = {
    # identifying header
    "'L'":          Bits(0, 8),
    "'C'":          Bits(8, 8),
    "'S'":          Bits(16, 8),
    "'A'":          Bits(24, 8),
    # first usable bit is 32
    
    # the XXX_DIGIT_* are numbered right to left so the least
    # significant digit is 0 and most significant is the highest
    # number.
    "FREQ_DIGIT_0": Bits(176, 16),
    "FREQ_DIGIT_1": Bits(192, 16),
    "FREQ_DIGIT_2": Bits(208, 16),
    "FREQ_DIGIT_3": Bits(120, 16),
    "FREQ_DIGIT_4": Bits(104, 16),
    "FREQ_DIGIT_5": Bits(88, 16),
    "FREQ_DIGIT_6": Bits(72, 16),
    
    "MODE_DIGIT_0": Bits(32, 16),
    "MODE_DIGIT_1": Bits(240, 16),
    "MODE_DIGIT_2": Bits(224, 16),
    
    # the SMETER_* are numbered left to right so the least
    # significant digit is 0 and most significant is the highest
    # number.
    "SMETER_0":     Bits(136, 1),
    "SMETER_1":     Bits(137, 1),
    "SMETER_2":     Bits(138, 1),
    "SMETER_3":     Bits(139, 1),
    "SMETER_4":     Bits(140, 1),
    "SMETER_5":     Bits(141, 1),
    "SMETER_6":     Bits(142, 1),
    "SMETER_7":     Bits(143, 1),
    "SMETER_8":     Bits(144, 1),
    "SMETER_9":     Bits(145, 1),
    "SMETER_10":    Bits(146, 1),
    "SMETER_11":    Bits(147, 1),
    "SMETER_12":    Bits(148, 1),
    "SMETER_13":    Bits(149, 1),
    "SMETER_14":    Bits(150, 1),
    "SMETER_15":    Bits(151, 1),
    "SMETER_16":    Bits(152, 1),
    "SMETER_17":    Bits(153, 1),
    "SMETER_18":    Bits(154, 1),
    "SMETER_19":    Bits(155, 1),
    "SMETER_20":    Bits(156, 1),
    "SMETER_21":    Bits(157, 1),
    "SMETER_22":    Bits(158, 1),
    "SMETER_23":    Bits(159, 1),
    "SMETER_24":    Bits(160, 1),
    "SMETER_25":    Bits(161, 1),
    "SMETER_26":    Bits(162, 1),
    
    "RF_P10":       Bits(40, 1),
    "RF_0":         Bits(244, 1),
    "RF_M10":       Bits(228, 1),
    #"RF_M20":      Bits(xxx, 1),   # TODO: unknown
    
    #"RX_LED":      Bits(xxx, 1),   # TODO: unknown
    #"TX_LED":      Bits(xxx, 1),   # TODO: unknown

    "BUSY":         Bits(80, 1),
    
    "AGC-S":        Bits(36, 1),
    "AGC-F":        Bits(248, 1),
    
    "BACKLIGHT":    Bits(32*8, 8),   # backlight value
    
    "MISC_FUNC":    Bits(76, 1),
    "MISC_KEY":     Bits(92, 1),
    "MISC_STAR":    Bits(232, 1),
    "MISC_NB":      Bits(212, 1),
    #"MISC_NAR":    Bits(200, 1),   # TODO: Narrow is lost!
    "MISC_T":       Bits(184, 1),
    "MISC_TUNE":    Bits(52, 1),
    "MISC_SPLIT":   Bits(54, 1),

    "LED_RX":       Bits(267, 1),
    }

if __name__ == '__main__':
    lcsa_bits = []
    for x in range(34*8):
        lcsa_bits.append('-')
        
    
    for name, i in lcsa.items():
        #print("%3d for %3d = %-14s" % (i.start, i.length, name))
        
        for x in range(i.length):
            if lcsa_bits[i.start+x] != '-':
                lcsa_bits[i.start+x] = lcsa_bits[i.start+x] + ' <<<multiple>>> ' + name
            else:
                lcsa_bits[i.start+x] = name
          
    print(f"Generated: {now_formatted}")
    print()
    print('Byte Bit  Usage')
    
    for x in range(34*8):
        if (x%8) == 0:
            print()
        b = x//8
        print("%2d %3d = %s" % (b, x, lcsa_bits[x]))
