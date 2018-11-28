from myhdl import *

@block
def mem_unit16x128(data_out, data_in, addr, we, alloc, alloc_addr, clock, reset_n):

    mem = [Signal(intbv(0)[16:0]) for i in range(128)]

    @always(clock.posedge)
    def logic():
        if reset_n == 0:
            alloc_addr.next = 0

        elif alloc == 1:
            alloc_addr.next = alloc_addr + 1

        if we == 1:
            mem[addr].next = data_in

        data_out.next = mem[addr]


    return logic
        
            



