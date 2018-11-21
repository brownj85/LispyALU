from myhdl import *

st = enum('ERR', 'OP','VAL', 'START')

@block
def lexer(go, ret,
        char_in, inst, lut_out,
        ram_addr_next,
        clock, reset_n, err_flag):
    
    state = Signal(st.START)
    state_next = Signal(st.START)
    expect_val = Signal(bool(0))
    
    op_valid = Signal(bool(0))
    is_digit = Signal(bool(0))

    char_buffer = Signal(intbv(0)[8:0])
    lut_buffer = Signal(intbv(0)[3:0])

    i_body_buffer = Signal(intbv(0)[8:0])
    i_mask_buffer = Signal(intbv(0)[2:0])
    inst_wire = ConcatSignal(i_mask_buffer, i_body_buffer)
    
    @always_comb
    def wires():
        inst.next = inst_wire[10:0]
    
    @always_comb
    def struct():
        op_valid.next = lut_out[0] or lut_out[1]
        is_digit.next = lut_out[2]

    @always_comb
    def state_table():

        if reset_n == 0:
            state_next.next = st.START
        
        elif err_flag == 1:
            state_next.next = st.ERR

        elif is_digit == 1:
            state_next.next = st.VAL

        elif char_in == 32 or char_in == 40:
            state_next.next = st.START

        elif op_valid == 1:
            if char_in == 45 and expect_val:
                state_next.next = st.VAL
            else:
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

            if char_buffer == 40:
                expect_val.next = 0

        elif state == st.VAL:
        
            i_body_buffer.next = ram_addr_next[8:0]
            i_mask_buffer.next = lut_buffer[2:0]
            
            if state_next != st.VAL:
                ret.next = 1
                

        elif state == st.OP:

            i_body_buffer.next = char_buffer
            i_mask_buffer.next = lut_buffer[2:0]

            expect_val.next = 1
    
            ret.next = 1
            
        elif state == st.ERR:
            err_flag.next = 1
                
        state.next = state_next

    return ctrl_signals, state_table, struct, wires

        




                    




