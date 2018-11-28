from myhdl import *
from dec_bin_converter import dec_to_bin_converter
from lut import char_lut

st = enum('ERR', 'ST0', 'EXPR_W', 'DIGIT0', 'DIGIT', 'OP', 'PUSH')

@block
def lexer(
        #data_inputs
        char_in,
        #data_outputs
        stack_in,
        #control_outputs
        push,
        #
        err_flag, 
        clock, 
        reset_n):

    state = Signal(st.ST0)
    state_next = Signal(st.ST0) 
    
    is_digit = Signal(bool(0))
    is_op = Signal(bool(0))
    
    lut = char_lut(char_in, is_digit, is_op) 

    sign = Signal(bool(0))
    result = Signal(intbv(0, -2**15, 2**15))
    convert = dec_to_bin_converter(char_in, sign, result, is_digit, err_flag, clock, reset_n);
    
    inst_mask = Signal(intbv(0)[2:0])
    inst_desc = Signal(intbv(0, -2**15, 2**15))
    inst = ConcatSignal(inst_mask, inst_desc)

    @always_comb
    def wire():
        stack_in.next = inst

    @always(clock.posedge)
    def control():
        if reset_n == 0:
            sign.next = 0
            push.next = 0
            err_flag.next = 0

        elif state == st.OP:
            push.next = 1
            inst_desc.next = char_in
            inst_mask.next = 3

        elif state == st.EXPR_W:
            push.next = 0
            sign.next = 0

        elif state == st.DIGIT0:
            sign.next = 1

        elif state == st.DIGIT:

            if state_next == st.EXPR_W:
                push.next = 1
                inst_desc.next = result
                inst_mask.next = 0

        state.next = state_next


    @always_comb
    def state_table():

        if reset_n == 0:
            state_next.next = st.ST0

        elif err_flag == 1:
            state_next.next = st.ERR

        elif state == st.ST0:
            if char_in == 32: #space
                state_next.next = st.ST0
            elif char_in == 40: #(
                state_next.next = st.OP
            else:
                state_next.next = st.ERR

        elif state == st.OP:
            if is_op:
                state_next.next = st.EXPR_W
            else:
                state_next.next = st.ERR
        
        elif state == st.EXPR_W:
            if char_in == 32: #space
                state_next.next = st.EXPR_W
            elif char_in == 45:
                state_next.next = st.DIGIT0
            elif is_digit:
                state_next.next = st.DIGIT
            elif char_in == 40:
                state_next.next = st.OP
            elif char_in == 0:
                state_next.next = st.ST0
            else:
                state_next.next = st.ERR

        elif state == st.DIGIT0:
            if is_digit:
                state_next.next = st.DIGIT
            else:
                state_next.next = st.ERR

        elif state == st.DIGIT:
            if is_digit:
                state_next.next = st.DIGIT
            elif char_in == 32 or char_in == 41:
                state_next.next = st.EXPR_W
            else:
                state_next.next = st.ERR


    return state_table, control, convert, lut, wire
