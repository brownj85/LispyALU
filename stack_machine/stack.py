from myhdl import *


@block
def program_stack(
        #data outputs
        stack_top,
        #data inputs
        data_in, 
        #control inputs
        push, 
        pop, 
        #control outputs
        empty, 
        #
        err_flag, 
        clock, 
        reset_n):

    stack = [Signal(intbv(0)[18:0]) for i in range(129)]
    stack[128] = Signal(intbv(2**17))
    
    stack_ptr = Signal(modbv(128, 0, 255))
    
    size_ctr = Signal(modbv(0, 0, 255))

    @always_comb
    def wires():
        stack_top.next = stack[stack_ptr]
        empty.next = stack_ptr[7]

    @always(clock.posedge)
    def logic():
        if reset_n == 0:
            stack_ptr.next = 128
            size_ctr.next = 0

        elif push == 1:
            stack_ptr.next = stack_ptr - 1
            stack[stack_ptr - 1].next = data_in
            size_ctr.next = size_ctr + 1

        elif pop == 1 and not stack_ptr[7]:
            stack_ptr.next = stack_ptr + 1
            size_ctr.next = size_ctr - 1
            stack[stack_ptr].next = 0


    return logic, wires
            
