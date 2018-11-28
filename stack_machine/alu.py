from myhdl import *


@block
def alu(
        #data inputs
        alu_a, 
        alu_b, 
        alu_op, 
        #data outputs
        alu_out, 
        #control inputs
        go,
        #control outputs
        done,
        #
        clock, 
        reset_n):

    @always(clock.posedge)
    def alu_ops():
        if go:
            if alu_op == 43:
                alu_out.next = alu_a.signed() + alu_b.signed()
            elif alu_op == 45:
                alu_out.next = alu_a.signed() - alu_b.signed()
            elif alu_op == 47:
                alu_out.next = alu_a.signed() / alu_b.signed()
            else:
                alu_out.next = alu_a.signed() * alu_b.signed()

            done.next = 1
        else:
            done.next = 0


    return alu_ops
