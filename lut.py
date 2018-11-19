from myhdl import *

@block
def mask_lut(char_in, mask_out):

    mask_table = [Signal(intbv(0)[3:0])  for i in range(128)]

    mask_table[40] = 2 # (

    mask_table[41] = 3 # ) push

    mask_table[43] = 1 # +
    mask_table[45] = 1 # -
    mask_table[47] = 1 # /
    mask_table[42] = 1 # *

    for i in range(48, 58):
        mask_table[i] = 4

    @always_comb
    def lut():
        mask_out.next = mask_table[char_in]

    return lut




