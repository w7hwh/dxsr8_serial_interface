"""
decode_screen_lcd.py

Decodes/Encodes the lcd info sent from the radio to the head

 original written by Josh, AJ9BM
 see https://github.com/jbm9/dxsr8_serial

 last edit: 20250710 1641 hrs by hwh


 edit history:

"""
#--------------------------------------------------------------------
"""


"""
class LCD16:
    """A 16 segment LCD display

    Layout is per Lite-On's naming convention:

     AAA BBB
    HK  M  NC
    H K M N C
      UU PP
    G T S R D
    GT  S  RD
     FFF EEE

    The alphabet is shown on page 54 of the DX-SR8 manual.
    
    """
    ALPHABET = {
        " " : "",
        "_" : "FE",
        "/" : "TN",
        "-" : "PU",
        "*" : "TKUPRN",
        "&" : "SUDPCEMF",
        "+" : "SUPM",
        "\\": "KR",
        "=" : "UPEF",
        "(" : "RN",
        ")" : "TK",
        "$" : "SAUHDPEMBF",

        # This is cyrillic, apparently. transliterating to the best of my ability
        "z" : "AUERNBF",
        "g" : "AGHB",
        "d" : "TDCENF",
        "s" : "TKAPEBF",
        "zh": "TSKRMN",

        "i" : "TGHDCN",
        "j" : "TAGHDCNB",
        "l" : "TDCN",
        "p" : "AGHDCB",
        "ch": "TKN",
        "|X|": "TSKGHDCRMN",
        "ts": "SGHEMF",
        "sh": "SGHDCEMF",
        "f": "SAERMBF",
        "yu": "GUHDCRN",
        "ya": "TAUHDPCB",
        "~": "ADPCEBF",
        "!": "TGUHDC",
        "@": "TGUH",
        
        "A": "TNPCD",
        "B": "ABCDMSFEP",
        "C": "ABHGFE",
        "D": "ABCDFEMS",
        "E": "ABHGFEUP",
        "F": "ABGHUP",
        "G": "BAHGFEDP",
        "H": "HGCDUP",
        "I": "ABMSFE",
        "J": "GFECD",
        "K": "HGUNR",
        "L": "HGFE",
        "M": "HGCDKN",
        "N": "HGKRCD",
        "O": "ABCDFEGH",
        "P": "ABCPUHG",
        "Q": "ABCDEFGHR",
        "R": "ABCUPGHR",
        "S": "ABKPDEF",
        "T": "ABMS",
        "U": "HGEFCD",
        "V": "HGTN",
        "W": "HGCDTR",
        "X": "KNRT",
        "Y": "KNS",
        "Z": "ABNTFE",
        "0": "ABCDEFGHNT",
        "1": "CD",
        "2": "ABCPUGFE",
        "3": "ABUPFECD",
        "4": "HUPCD",
        "5": "ABHUPDEF",
        "6": "ABHGFEDUP",
        "7": "ABCD",
        "8": "ABCDEFGHUP",
        "9": "ABHCUPDFE",
        }

    def fixup(self, l):
        """Fudges segments the same way the radio seems to.

        A and B are hardwired together, as are E and F"""


        fudges = [ ('A', 'B'),
                   ('E', 'F') ]

        for x,y in fudges:
            if x in l and y not in l:
                l += y
            if y in l and x not in l:
                l += x

        return l

    def __init__(self, lit=""):
        self.lit = self.fixup(lit)

        # create the alphabet lookup table. Yes, I want to do this
        # every runtime, since I have no proper tests, this makes me
        # feel much better about the delusion that everything is
        # working.
        
        self.lookup = {} # mask => character
        for c,m in self.ALPHABET.iteritems():
            m_sorted = "".join(sorted(list(m)))
            if m_sorted in self.lookup:
                raise Exception("Non-unique mask to character mapping: %s goes to both %s and %s" % (m, self.lookup[m_sorted], c))

            self.lookup[m_sorted] = c
            

    def draw(self):
        digit="""
     AAA BBB
    HK  M  NC
    H K M N C
      UU PP
    G T S R D
    GT  S  RD
     FFF EEE"""

        allsegments = set()
        for c in digit:
            allsegments.add(c)

        w = digit

        for c in allsegments:
            if c == "\n" or c == " " or c == ":"  or c.islower():
                continue
            if c in self.lit:
                w = w.replace(c, "#")
            else:
                w = w.replace(c, ".")

        return w
        
    def decode(self):
        lit_key = "".join(sorted([ c if c.isupper() else "" for c in self.lit]))

        if lit_key not in self.lookup:
            print(">>> %s MISSING: %s" % (str(self.__class__),  self.lit ))
            print(self.draw())
            return None

        return self.lookup[lit_key]

#--------------------------------------------------------------------
"""


"""
class LCD16_a(LCD16):

    # This is the segment associated with each bit in the input, in
    # ascending bit order.
    
    SEGMENT_MAP = "TSKAyGUHxDPCERMN"
    
    @classmethod
    def from_bytes(cls, bytes, offset):
        lit = ""
        for k in range(16):
            if 1 == _get_bit(bytes, offset+k):
                lit += cls.SEGMENT_MAP[k]

        return cls(lit)

#--------------------------------------------------------------------
"""


"""
class LCD16_b(LCD16_a):
    """This is the same as the other 16 segment display, just wired differently.
    """
    SEGMENT_MAP = "ERMNyDPCaGUHTSKA"

class LCD16_c(LCD16_a):
    SEGMENT_MAP = "FRMNEDPCxGUHTSKA"

class LCD16_d(LCD16_a):
    SEGMENT_MAP = "ERMNyDPCxGUHTSKA"
#--------------------------------------------------------------------
"""


"""
class LCD16_mode_a(LCD16_a):
    SEGMENT_MAP = "AKcdeGgHiCPDmnoE"

class LCD16_mode_b(LCD16_a):
    SEGMENT_MAP = "AKcTeGUHiCPDNnRE"

class LCD16_mode_c(LCD16_a):
    SEGMENT_MAP = "KAcEqCPDiGkHSNMp"

