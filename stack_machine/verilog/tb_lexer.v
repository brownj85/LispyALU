module tb_lexer;

reg [7:0] char_in;
wire [17:0] stack_in;
wire push;
wire err_flag;
reg clock;
reg reset_n;

initial begin
    $from_myhdl(
        char_in,
        clock,
        reset_n
    );
    $to_myhdl(
        stack_in,
        push,
        err_flag
    );
end

lexer dut(
    char_in,
    stack_in,
    push,
    err_flag,
    clock,
    reset_n
);

endmodule
