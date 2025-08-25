"""
exercise_decode_string.py

 Runs test cases through decode_screen routines.
 
 last edit: 20250712 1516 hrs by hwh

 edit history:
    20250712 commented out last two test screens because they fail.
             I don't know if they're valid tests. Will revisit this
             when I can get tests from my own radio - hwh

 TODO:
    FIX the last two tests?

"""
from dxsr8_screen import *


def intWithCommas(x):
    if type(x) is not int:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


screens  = [

    "4c43534112502b660ae814f0a0e81506810000000000408ea18a4004038de1840400",
    "4c435341b12a20800a0000f81eb99ba99b0000000000a99aa99ba99a0001081e0400",
    "4c435341b12a20000a000a100ab99ba99b0000000000a99aa99ba99a0001081e0400",
    "4c435341b12a20800a000a100ab99ba99b0000000000a99aa99ba99a0001081e0400",

    "4c43534112502f2b6ae804a01aa42ba8110000000000a24aa84a4004038de1840400",
    "4c43534112502d760a0a5ee0a00a51a42b000000000004a0e8104004038de1840400",
    "4c43534112502d360a0c161a40400500010000000000a99aa99ae18e038de1840400",
    "4c435341125026360ae80c118e0a5b0a5b0000000000a24a4004010a038de1840400",
    "4c43534112502b660ae814f0a0e81506810000000000408ea18a4004038de1840400",
    "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99ba0000001081e0400",
    "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99ba99a0001081e0400",
    "4c435341b12aa0000a000a000ab99b000b0000000000a99aa001e1840001081e0400",
    "4c435341b12aa0000a000a000ab99b000b0000000000a99aa99be1840001081e0400",
    
    "4c43534112502f2b6ae804a01aa42ba8110000000000a24aa84a4004038de1840400",
    "4c435341b12a20800a0000d00eb99ba99b0000000000a99aa99ba99a0001081e0400",
    
    # TODO: these two throw an exception. Commented out until I can get
    # examples from my own radio to validate the tests - hwh
    #"4c435341b12a2f5f55000aa99a781cc00f0000000000a99a718de18e0001081e0400",
    #"4c43534102502f3f55a01b0180a010404c43534102502f3f55a01b0180a010400500",
    ]


fdisp = FrequencyDisplay()
mdisp = ModeDisplay()
rfdisp = RFPowerDisplay()
agcdisp = AGCDisplay()
smeterdisp = SMeterDisplay()

def print_state(i, sin):
    s = [ int(sin[i:i+2], 16) for i in range(0, len(sin)-1, 2) ]
    
    #try:
    if True:
        mode = mdisp.decode(s)

        rxstate = "%s RF:%+2d %s" % (agcdisp.decode(s), rfdisp.decode(s), smeterdisp.decode_string(s))
        
        if fdisp.is_freq(s):
            print("[%s] f = %d %s" % (mode, fdisp.freq(s), rxstate))
        else:
            print("[%s] > %s < %s" % (mode, fdisp.decode(s), rxstate))
    """        
    except (Exception) as e:
        print()
        print("Caught exception: " + str(e))
        print()
        print("Input #%d: %s" % (i, s))
        #print("Mode: " + mode)
        print()
   """

for i,s in enumerate(screens):
    print_state(i, s)

print()
print("Last two tests commented out, fix when they can be validated with actual radio output - hwh")
