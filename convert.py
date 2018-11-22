from myhdl import *

@block
def converter(char_in, lut_out,
                ram_addr_next, ram_write, ram_wr_addr, ram_we, ram_alloc, 
                err_flag, clock, reset_n):


    digit_buffer = [Signal(intbv(0)[15:0]) for i  in range(6)]
    #result = Signal(intbv(0, -2**15, 2**15).signed())

    #state
    enabled = Signal(bool(0))
    err_st = Signal(bool(0))

    sign = Signal(bool(0))

    ctr = Signal(intbv(0, 0, 6))

    digit = char_in(4, 0)
    is_digit = lut_out(2)
    lut_buffer = Signal(bool(0))

    result = Signal(intbv(0, -2**15, 2**15))

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
            ram_alloc.next = 0
            ctr.next = 0
            err_st.next = 0

        elif err_st:
            err_flag.next = 1
        
        elif char_in == 45:
            sign.next = 1

        elif is_digit:
            ram_we.next = 0
            ram_alloc.next = 0
            ram_wr_addr.next = ram_addr_next
            ctr.next = ctr + 1

        else:
            if lut_buffer == 1:
                ram_alloc.next = 1
                ram_we.next = 1
                ram_write.next = result
            else:
                ram_alloc.next = 0
                ram_we.next = 0

            sign.next = 0
            ctr.next = 0
        
        for i in range(6):
            if i > ctr:
                digit_buffer[i].next = 0
            elif i == ctr:
                digit_buffer[ctr].next = digit
            elif is_digit:
                digit_buffer[i].next = (digit_buffer[i] << 3) + (digit_buffer[i] << 1)

        lut_buffer.next = lut_out[2]

    return data, add
        







        



    

    



