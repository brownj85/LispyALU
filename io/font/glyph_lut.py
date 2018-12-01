from myhdl import *
from bdf_parse import *

#lut for 8 * 10 glyphs
@block
def glyph_lut(char_in, glyph_out, glyph_tup=()):

    data = glyph_tup

    @always_comb
    def glyph_sel():
        glyph_out.next = data[char_in]

    return glyph_sel





            


        
