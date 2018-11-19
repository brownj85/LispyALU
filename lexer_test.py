from myhdl import *
from lut import mask_lut
from lexer import lexer


@block
def testbench(line, ram, commands):

    clock, store, ret,  err_flag = (Signal(bool(0)) for i in range(4))
    
    go = Signal(bool(0))
    reset_n = Signal(bool(1))

    char_in, ram_addr = Signal(intbv(ord(line[0]))[8:0]), Signal(intbv(0)[8:0])
    char_in.next = ord(line[0])
    lut_out = Signal(intbv(0)[3:0])
    inst = Signal(intbv(0)[10:0])
    mem_in = Signal(intbv(0)[16:0])

    table = mask_lut(char_in, lut_out)

    lex = lexer(go, ret, store, char_in, inst, lut_out, mem_in,
            ram_addr, clock, reset_n, err_flag)

    i = Signal(intbv(0))

    HALF_PERIOD = delay(10)
    
    @always(HALF_PERIOD)
    def clockgen():
        clock.next = not clock

    @always(clock.posedge)
    def app():

        if i < len(line):
            go.next = 1
            char_in.next = ord(line[i])
            i.next = i + 1
        else:
            go.next = 0

        if store:
            ram.append(int(mem_in[16:0]))
            ram_addr.next = ram_addr + 1

        if ret and go:
            commands.append((int(inst[10:8]),int(inst[8:0])))
        

    return clockgen, lex, table, app

ram, commands = [], []
line = input().rstrip()[::-1]
line = line.replace("(", "")
line = " " + line
tb = testbench(line, ram, commands)
tb.config_sim(trace=True)
tb.run_sim(2000)
print(commands)
print(ram)

                    


            



    
