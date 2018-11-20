from myhdl import *

expect_st = enum('ST0', 'OP', 'A', 'B', 'CLOSE')
st = enum('ERR', 'OP', 'VAL_WAIT', 'VAL', 'START', 'WAIT', 'RST')

@block
def lexer(go, ret, store, char_in, inst, lut_out, 
             mem_addr,  clock, reset_n, err_flag,
             to_converter, conv_push)
    
    state = Signal(st.START)
    state_next = Signal(st.START)

    expect_state = Signal(st.START)
    expect_state_next = Signal(st.OP)

    convert_buffer = Signal(intbv(0)[16:0])

    state_ctr = Signal(intbv(0))[3:0]
    
    op_valid = Signal(bool(0))
    is_digit = Signal(bool(0))

    char_buffer = Signal(intbv(0)[8:0])
    lut_buffer = Signal(intbv(0)[3:0])

    i_body_buffer = Signal(intbv(0)[8:0])
    i_mask_buffer = Signal(intbv(0)[2:0])

    inst_int = ConcatSignal(i_mask_buffer, i_body_buffer)

    @always_comb
    def struct():
        op_valid.next = lut_out[0] or lut_out[1]
        is_digit.next = lut_out[2]
        inst.next = inst_int

    @always_comb
    def state_table():

        if reset_n == 0:
            state_next.next = st.START
        
        elif err_flag == 1:
            state_next.next = st.ERR

        elif is_digit == 1:
            state_next.next = st.VAL

        elif char_in == 32:
            state_next.next = st.START

        elif op_valid == 1:
            state_next.next = st.OP

        else:
            state_next.next = st.ERR
            

    @always(clock.posedge)
    def ctrl_signals():

        char_buffer.next = char_in
        lut_buffer.next = lut_out

        if state == st.START:
            err_flag.next = 0
            ret.next = 0
            store.next = 0

        elif state == st.VAL:
        
            i_body_buffer.next = mem_addr
            i_mask_buffer.next = lut_buffer[2:0]
            
            if state_next == st.START:
                store.next = 1
                ret.next = 1
                
        elif state == st.OP:

            i_body_buffer.next = char_buffer
            i_mask_buffer.next = lut_buffer[2:0]
            
            ret.next = 1

        elif state == st.ERR:
            err_flag.next = 1
                
        state.next = state_next

        if state_next == state:
            state_ctr.next = state_ctr + 1
        else:
            state_ctr.next = 0


    return ctrl_signals, state_table, struct

        




                    




