from myhdl import *
st = enum( "ST0", "ERR", "START", 
        "LOAD_OP", "LOAD_VAL", "PUSH",
        "FETCH", "STORE", "EVAL0","EVAL1", "RET")

@block
def cu_ctrl(
        #inputs
        go,
        inst_mask,
        top_mask,
        alu_flag,
        stack_flag,
        clock, reset_n,
        #outputs
        get,
        alu_eval,
        load_op, load_val,
        stack_pop, stack_push, 
        fetch, store,
        ram_alloc, ram_we,
        ret
        ):

    state_ctr = intbv(0)
    state = Signal(st.S0)
    state_next = Signal(st.S0)

    err_flag = Signal(bool(0))
    
    #internal state control
    @always(clock.posedge)
    def int_state():
        if state_next != state:
            state_ctr.next = 0
        else:
            state_ctr.next = state_ctr + 1

        state.next = state_next
    
    
    @always(clock.posedge)
    def ctrl_signals():
        if state == st.ST0:
            get.next = 0
            ret.next = 0
            err_flag.next = 0

        elif state == st.START:
            get.next = 1
            stack_push.next = 0
            load_val.next = 0
            ram_we.next = 0
            
        elif state == st.PUSH:
            stack_push.next = 1

        elif state == st.LOAD_VAL:
            if top_mask == 3:
                err_flag.next = 1
            else:
                load_val.next = 1

        elif state == st.LOAD_OP:
            if top_mask == 3:
                load_op.next = 1
                get.next = 0
            else:
                err_flag.next = 1

        elif state == st.FETCH:
            load_op.next = 0
            fetch.next = state_ctr + 1

        elif state == st.EVAL0:
            fetch.next = 0
            if state_ctr == 0:
                alu_eval.next = 1
                stack_pop.next = 1
            else:
                alu_eval.next = 0
                stack_pop.next = 0

        elif state == st.STORE
            if state_ctr == 0:
                store.next = 1
            else:
                store.next = 0
                ram_we.next = 1

        elif state == st.RET:
            ret.next = 1   

        else:
            err_flag.next = 1
    
    
    @always_comb
    def state_table():

        if reset_n == 0:
            state_next.next = st.ST0

        elif err_flag == 1:
            state_next.next = st.ERR
        
        elif state == st.ST0:
            if go:
                state_next.next = st.START
            else:
                state_next.next = st.ST0

        elif state == st.START:
            if inst_mask == 0:
                state_next.next = st.LOAD_VAL
            elif inst_mask == 1:
                state_next.next = st.START
            elif inst_mask == 2:
                state_next.next = st.LOAD_OP
            elif inst_mask == 3:
                state_next.next = st.PUSH

        elif state == st.LOAD_VAL:
            state_next.next = st.START
        
        elif state == st.LOAD_OP:
            state_next.next = st.FETCH

        elif state == st.PUSH:
            state_next.next = st.START

        elif state == st.FETCH:
            if state_ctr == 4:
                state_next.next = st.EVAL0
            else:
                state_next.next = st.FETCH

        elif state == st.EVAL0:
            if alu_flag == 1:
                state_next.next = st.EVAL1
            else:
                state_next.next = st.EVAL0

        elif state == st.EVAL1:
            if stack_empty == 1:
                state_next.next = st.RET
            else:
                state_next.next = st.WRITE

        elif state == st.STORE:
            if state_ctr == 1:
                state_next.next = st.START
            else state_next.next = st.WRITE
        
        elif state == st.RET:
            state_next.next = st.ST0

        elif state == st.ERR:
            state_next.next = st.ERR

        else:
            state_next.next = st.ERR


    return state_table, ctrl_signals, int_state

