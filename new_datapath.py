from myhdl import *

@block
def cu_data(
        #data inputs
        inst_body, 
        alu_out,
        ram_out, ram_addr_out,
        #data outputs
        out,
        ram_in, ram_addr_in,
        alu_op, alu_a, alu_b,
        top_mask,
        stack_empty,
        #control inputs
        load_op, load_addr,
        stack_pop, stack_push,
        fetch,
        sto,
        ret,
        clock, reset_n
        ):

    stack = [Signal(intbv(0)[18:0]) for i in range(128)]
    stack_ctr = Signal(modbv(128)[8:0])
    stack_ptr = Signal(intbv(0)[7:0])


    @always_comb
    def struct():
        stack_empty.next = stack_ctr[7]
        top_mask[0].next = stack[stack_ptr][0]
        top_mask[1].next = stack[stack_ptr][9]

        ram_in.next = alu_out
        out.next = alu_out

    @always(clock.posedge)
    def datapath():

        if reset_n == 0:
            stack_ctr.next = 128
            stack_ptr.next = 0

        elif load_addr == 1:
            if top_mask == 0:
                stack[stack_ptr][9:1].next = inst_body
                stack[stack_ptr][0].next = 1
            elif top_mask == 1:
                stack[stack_ptr][18:10] = inst_body
                stack[stack_ptr][9].next = 1

        elif load_op == 1:
            alu_op.next =  inst_body

        elif stack_pop == 1:
            stack[stack_ptr][0].next = 0
            stack[stack_ptr][9].next = 0
            stack_ptr.next = stack_ptr - 1
            stack_ctr.next = stack_ctr + 1

        elif stack_push == 1:
            stack_ptr.next = stack_ptr + 1
            stack_ctr.next = stack_ctr + 1

            if top_mask == 0:
                stack[stack_ptr][9:1].next = ram_addr_out
            elif top_mask == 1:
                stack[stack_ptr][18:10].next = ram_addr_out

        elif fetch == 1:
            ram_addr_in.next = stack[stack_ptr][9:1]

        elif fetch == 2:
            ram_addr_in.next = stack[stack_ptr][18:9]

        elif fetch == 3:
            alu_b.next = ram_out

        elif fetch == 4:
            alu_a.next = ram_out

        elif store == 1:
            if top_mask == 0:
                ram_addr_in.next = stack[stack_ptr][9:1]
            elif top_mask == 1:
                ram_addr_in.next = stack[stack_ptr][18:10]

    return datapath, struct


                

            


        



