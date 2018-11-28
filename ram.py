from myhdl import *

@block
def ram(addr, we, data_in, data_out, clock, reset_n, word_size, nwords):
    mem = [Signal(intbv(0)[word_size:0])
            for i in range(nwords)]

    @always(clock.posedge)
    def write():
        if we:
            mem[addr].next = data_in


    @always_comb
    def read():
        data_out.next = mem[addr]


    return read, write




