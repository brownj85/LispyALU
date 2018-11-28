from myhdl import *
from lexer import lexer
from stack import program_stack
from alu import alu
from control_unit import control_unit
@block
def testbench(line):

    clock = Signal(bool(0))
    reset_n = Signal(bool(1))
    alu_err, cu_err, lex_err, stack_err = (Signal(bool(0)) for i in range(4))

    HALF_PERIOD = delay(10)

    @always(HALF_PERIOD)
    def clockgen():
        clock.next = not clock


    push, pop = (Signal(bool(0)) for i in range(2))
    stack_empty = Signal(bool(0))

    stack_top = Signal(intbv(0)[18:0])
    data_in = Signal(intbv(0)[18:0])
    
    stack = program_stack(
                    stack_top, 
                    data_in, 
                    push, 
                    pop, 
                    stack_empty, 
                    stack_err,
                    clock, 
                    reset_n)

    char_in = Signal(intbv(32)[8:0])

    lex = lexer(
            char_in, 
            data_in, 
            push, 
            lex_err,
            clock, 
            reset_n)

    alu_op = Signal(intbv(0)[16:0])

    alu_a, alu_b, ret, alu_out = (Signal(intbv(0, -2**15, 2**15)) for i in range(4))

    alu_go, alu_done, cu_done, cu_go = (Signal(bool(0)) for i in range(4))
    
    al = alu(
            alu_a, 
            alu_b, 
            alu_op, 
            alu_out, 
            alu_go, 
            alu_done,
            alu_err,
            clock, 
            reset_n)
    
    
    cu = control_unit(
            ret,
            cu_go,
            cu_done,
            pop,
            stack_top,
            stack_empty,
            alu_go,
            alu_op,
            alu_a,
            alu_b,
            alu_out,
            alu_done,
            cu_err,
            clock,
            reset_n)

    i = Signal(intbv(0))
    
    @always(clock.posedge)
    def bench():

        if i < len(line):
            char_in.next = ord(line[i])
        else:
            char_in.next = 0
            
        if i > len(line):
            cu_go.next = 1

            if cu_done:
                print(int(ret.signed()))
                raise StopSimulation

        i.next = i + 1

    return bench, clockgen, lex, stack, al, cu


line = input().rstrip()

tb = testbench(line)
tb.config_sim(trace=True)
tb.run_sim()



    
