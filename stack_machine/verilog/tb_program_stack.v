module tb_program_stack;

wire [17:0] stack_top;
reg [17:0] data_in;
reg push;
reg pop;
wire empty;
wire err_flag;
reg clock;
reg reset_n;

initial begin
    $from_myhdl(
        data_in,
        push,
        pop,
        clock,
        reset_n
    );
    $to_myhdl(
        stack_top,
        empty,
        err_flag
    );
end

program_stack dut(
    stack_top,
    data_in,
    push,
    pop,
    empty,
    err_flag,
    clock,
    reset_n
);

endmodule
