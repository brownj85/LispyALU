from myhdl import *
from glyph_lut import glyph_lut
from bdf_parse import *

bbx, glyph_data = glyph_myhdl("bitocra7.bdf", 0, 128)

glyph_bus = Signal(intbv(0)[bbx[0] * bbx[1]:0])
char_in = Signal(intbv(0)[8:0])

gl_lut = glyph_lut(char_in, glyph_bus, glyph_data[1])

gl_lut.convert(hdl='Verilog')
