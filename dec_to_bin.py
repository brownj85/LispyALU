from myhdl import *

st = enum("PUSH", "CONVERT", "RET",  "START")

@block
def converter(digit, out, push, ret, clock, reset_n):

    digit_buffer = [Signal(intbv(0)[8:0]) for i in range(6)]
    counter = Signal(intbv(0)[3:0])
    convert_buffer = Signal(modbv(0)[16:0])

    powers = [Signal(intbv(10 ** i)) for i in range(6)]

    state = Signal(st.START)
    state_next = Signal(st.START)

    input_buffer = Signal(intbv(0)[16:0])

    @always_comb
    def state_table():
        if reset_n == 0:
            state_next.next = st.START

        elif state == st.START:
            if push == 1:
                state_next.next = st.PUSH
            else:
                state_next.next = st.START

        elif state == st.PUSH:
            if push == 1:
                state_next.next = st.PUSH
            else:
                state_next.next = st.CONVERT

        elif state == st.CONVERT:
            if counter == 0:
                state_next.next = st.RET

        elif state == st.RET:
            state_next.next = st.START

        out.next = convert_buffer.next


    @always(clock.posedge)
    def ctrl_signals():
        if state == st.START:
            counter.next = 0
            convert_buffer.next = 0
            ret.next = 0

        elif state == st.PUSH:
            counter.next = counter + 1
            digit_buffer[counter].next = input_buffer

        elif state == st.CONVERT:
            if counter != 0:
                counter.next = counter - 1

            convert_buffer.next = convert_buffer + digit_buffer[counter] * powers[counter]

        elif state == st.RET:
            ret.next = 1

        input_buffer.next = digit
        state.next = state_next


    return ctrl_signals, state_table

