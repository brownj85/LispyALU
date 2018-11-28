from myhdl import *

st = enum('WAIT','RET', 'GET', 'EVAL')

@block
def control_unit(
        #data_outputs
        ret,
        #control_inputs
        go,
        #control_outputs
        done,
        #program stack inputs
        pr_stack_pop,
        #program stack outputs
        pr_stack_top,
        pr_stack_empty,
        #alu inputs
        alu_go, 
        alu_op, 
        alu_a, 
        alu_b, 
        #alu outputs
        alu_out, 
        alu_done, 
        #
        err_flag,
        clock, 
        reset_n):

    stack = [Signal(intbv(0)[16:0]) for i in range(130)]
    stack_ptr = Signal(modbv(128, 0, 255))

    mask = pr_stack_top(18, 16)
    desc = pr_stack_top(16, 0)

    state = Signal(st.WAIT)

    @always(clock.posedge)
    def logic():
        if reset_n == 0:
            stack_ptr.next = 0
            alu_go.next = 0
            done.next = 0
            state.next = st.WAIT
            err_flag.next = 0

        elif state == st.WAIT:
            if not pr_stack_empty and go:
                pr_stack_pop.next = 1
                state.next = st.GET

        elif state == st.GET:
            if pr_stack_empty:
                state.next = st.RET
            if mask == 0:
                stack[stack_ptr -1].next = desc
                stack_ptr.next = stack_ptr - 1

            elif mask == 3:
                alu_op.next = desc
                alu_go.next = 1
                alu_a.next = stack[stack_ptr].signed()
                alu_b.next = stack[stack_ptr + 1].signed()
                pr_stack_pop.next = 0
                state.next = st.EVAL

        elif state == st.EVAL:
            if alu_done:
                stack[stack_ptr + 1] = alu_out.signed()
                stack_ptr.next = stack_ptr + 1
                state.next = st.GET
                alu_go.next = 0
                pr_stack_pop.next = 1


        elif state == st.RET:
            ret.next = stack[stack_ptr]
            done.next = 1


    return logic
            
            
            
