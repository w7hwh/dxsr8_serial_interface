"""
dxsr8_screen.py

 Decodes/Encodes the info sent from the radio to the head

 original written by Josh, AJ9BM
 see https://github.com/jbm9/dxsr8_serial

 last edit: 20250719 2239 hrs by hwh

 edit history:


 todo:

"""    

class FrequencyDisplay:
    def decode(self, b):
        digits = [ LCD16_a.from_bytes(b, o) for o in [72, 88, 104, 120] ]
        digits += [ LCD16_b.from_bytes(b, 208) ]
        digits += [ LCD16_c.from_bytes(b, 192) ]
        digits += [ LCD16_d.from_bytes(b, 176) ]    

        return "".join([d.decode() for d in digits])
     
#------------------------------------------------------    

class SMeterDisplay():
    def decode(self, b):
        busy = get_bit(b, 80)
        if 0 == busy:
            return None

        maxtick = max([ i-136 if 1 == get_bit(b, i) else 0 for i in range(136, 162) ])

        if maxtick == 0:
            return 0

        if maxtick < 9*2:
            return 1 + float(maxtick-1)/2

        step = 1.259921 # 2^(1/3)
        db = 10

        for i in range(18, maxtick):
            db *= step

        return db

    def decode_string(self, b):
        g = self.decode(b)
        if None == g:
            return "squelch"
        return "%.2f" % g

#------------------------------------------------------    

sets = {
    "MODE_DIGIT_0": 224,   # 16 LCD bits
    "MODE_DIGIT_1": 240,   # 16 LCD bits
    "MODE_DIGIT_2":  32,   # 16 LCD bits 
    "RF_P10":        40,   # single bit
    "RF_0":         244,   # single bit
    "RF_M10":       228,   # single bit
    #"RF_M20":      xxx,   # single bit TODO: unknown
    #"RX_LED":      xxx,   # single bit TODO: unknown
    #"TX_LED":      xxx,   # single bit TODO: unknown
    "AGC-S":         36,   # single bit
    "AGC-F":        248,   # single bit
    "BACKLIGHT":     32,   # 8 bit value
    "MISC_FUNC":     76,   # single bit
    "MISC_KEY":      92,   # single bit
    "MISC_STAR":    232,   # single bit
    "MISC_NB":      212,   # single bit
    #"MISC_NAR":    200,   # single bit TODO: Narrow is lost!
    "MISC_T":       184,   # single bit
    "MISC_TUNE":     52,   # single bit
    "MISC_SPLIT":    54,   # single bit
    }

print()
for name, i in sets.items():
    print("%-14s= %3d" % (name, i))
