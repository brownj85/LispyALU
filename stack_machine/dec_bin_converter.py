from myhdl import *

@block
def dec_to_bin_converter(
        #data_inputs
        char_in, 
        sign,
        #data_outputs
        result,
        #control_inputs
        enable,
        #        
        err_flag, 
        clock, 
        reset_n):

    digit_buffer = [Signal(intbv(0)) for i  in range(6)]

    #state
    err_st = Signal(bool(0))
    ctr = Signal(intbv(0, 0, 6))
    digit = char_in(4, 0)

    @always_comb
    def add():
        if sign:
            result.next = -(digit_buffer[0] + digit_buffer[1] + digit_buffer[2] + \
                            digit_buffer[3] + digit_buffer[4] + digit_buffer[5])
        else:
            result.next = digit_buffer[0] + digit_buffer[1] + digit_buffer[2] + \
                            digit_buffer[3] + digit_buffer[4] + digit_buffer[5]


    @always(clock.posedge)
    def data():
        if reset_n == 0:
            ctr.next = 0
            err_st.next = 0

        elif err_st:
            err_flag.next = 1
        
        elif enable:
            ctr.next = ctr + 1

        else:
            ctr.next = 0
        
        for i in range(6):
            if i > ctr:
                digit_buffer[i].next = 0
            elif i == ctr and enable:
                digit_buffer[ctr].next = digit
            elif enable:
                digit_buffer[i].next = (digit_buffer[i] << 3) + (digit_buffer[i] << 1)

    return data, add
        







        



    

    



