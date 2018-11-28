from myhdl import *

@block
def char_lut(
        #inputs
        char_in, 
        #outputs
        is_digit, 
        is_op):

    mask_table = [Signal(intbv(0)[2:0])  for i in range(128)]

    mask_table[43] = Signal(intbv(1)) # +
    mask_table[45] = Signal(intbv(1)) # -
    mask_table[47] = Signal(intbv(1)) # /
    mask_table[42] = Signal(intbv(1)) # *

    for i in range(48, 58):
        mask_table[i] = Signal(intbv(2))

    @always_comb
    def lut():
        is_digit.next = mask_table[char_in][1]
        is_op.next = mask_table[char_in][0]

    return lut




