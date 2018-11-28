from myhdl import *
from alu import alu
from control_unit import control_unit
from lexer import lexer
from stack import program_stack

clock = Signal(bool(0))
reset_n = Signal(bool(1))

alu_a, alu_b, alu_op, alu_out = (Signal(intbv(0)[16:0]) for i in range(4))
alu_go, alu_done, alu_err = (Signal(bool(0)) for i in range(3))

alu = alu(
    alu_a,
    alu_b,
    alu_op,
    alu_out,
    alu_go,
    alu_done,
    alu_err,
    clock,
    reset_n)

alu.convert()


pr_stack_top, pr_stack_in = (Signal(intbv(0)[18:0]) for i in range(2))
pr_stack_push, pr_stack_pop, pr_stack_empty, pr_stack_err = (Signal(bool(0)) for i in range(4))

pr_stack = program_stack(
    pr_stack_top,
    pr_stack_in,
    pr_stack_push,
    pr_stack_pop,
    pr_stack_empty,
    pr_stack_err,
    clock,
    reset_n)

pr_stack.convert()

lex_err = Signal(bool(0))
char_in = Signal(intbv(0)[8:0])

lex = lexer(
    char_in,
    pr_stack_in,
    pr_stack_push,
    lex_err,
    clock,
    reset_n)

lex.convert()


cu_ret, cu_go, cu_done, cu_err = (Signal(bool(0)) for i in range(4))

control = control_unit(
    cu_ret, 
    cu_go, 
    cu_done, 
    pr_stack_pop,
    pr_stack_top,
    pr_stack_empty,
    alu_go,
    alu_op,
    alu_a,
    alu_b,
    alu_out,
    alu_done,
    cu_err,
    clock,
    reset_n)

control.convert()
    


