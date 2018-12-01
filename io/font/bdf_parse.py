from myhdl import *
import sys

def glyph_myhdl(filename, first=0, last=128):
    gtup = get_glyph_bmp(filename)
    gtup = flatten_glyphs(gtup)

    return dict_to_ascii_tup(gtup, first, last)


def dict_to_ascii_tup(glyph_tup, first, last):
    bbx, glyphs = glyph_tup
   
    chars = [0 for i in range(first, last)]

    for enc in glyph_tup[1].keys():
        if first <= enc < last:
            if enc in glyph_tup[1].keys():
                chars[enc - first] = glyph_tup[1][enc]

    return (bbx, tuple(chars))

def get_glyph_bmp(filename):

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except IOError as e:
        print("IO ERROR!");
        return {}

    
    for line in lines:
        line = line.strip()
        if "FONTBOUNDINGBOX" in line:
            spl = line.split()
            bbx = (int(spl[1]), int(spl[2]), int(spl[3]), int(spl[4]))
            break

    chars = {}
    curr = []
    enc = 0
    line_ctr = 0

    for line in lines:
        line = line.strip()
        if "COMMENT" in line:
            pass

        elif line_ctr == 0:
            if "STARTCHAR" in line:
                line_ctr = line_ctr + 1

        elif line_ctr == 1:
            enc = int(line.split()[-1])
            line_ctr = line_ctr + 1
        
        elif 2 <= line_ctr < 6:
            line_ctr = line_ctr + 1

        elif 6 <= line_ctr < 6 + bbx[1]:
            curr.append(line)
            line_ctr = line_ctr + 1

        elif line_ctr == 6 + bbx[1]:
            chars[enc] = tuple(curr)
            
            line_ctr = 0
            curr = []

    return (bbx, chars)

def print_flat(bbx, font_int):
    font_int = intbv(font_int)[bbx[0] * bbx[1]:0]
    bit_ctr = 0
    for y in reversed(range(0, bbx[1])):
        bitstr = ""
        for x in reversed(range(0, bbx[0])):
            bitstr = bitstr + " "
            if font_int[y * bbx[0] + x] == 1:
                bitstr = bitstr + "0"
            else:
                bitstr = bitstr + " "
            bit_ctr = bit_ctr + 1
        print(bitstr)

    print(bit_ctr)

    
#convert font glyphs to k-bit integers
def flatten_glyphs(font_tup):
    bbx, glyphs = font_tup

    if bbx[0] <= 4:
        hx_digits = 1
        bbx = (4,) + bbx[1:]
    else:
        hx_digits = 2
        bbx = (8,) + bbx[1:]
    
    glyph_ints = {}
    for enc in glyphs.keys():
        hxstr = "";
        glyph = glyphs[enc]
        for val in glyph:
            hxstr = hxstr + val[0:hx_digits]

        glyph_ints[enc] = int(hxstr, 16)
    
    return (bbx, glyph_ints)


            
if __name__ == "__main__":
    font_tup = get_glyph_bmp(sys.argv[1])
    ffont_tup = flatten_glyphs(font_tup)

    tuplze = dict_to_ascii_tup(ffont_tup,0, 128) 
     
    getln = "true"

    while getln:
        getln = int(input("Enter ascii code :"))
        curr = tuplze[1][getln]
        print(hex(curr))
        print_flat(tuplze[0], curr)
