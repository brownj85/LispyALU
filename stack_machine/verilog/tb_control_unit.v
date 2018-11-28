module tb_control_unit;

wire ret;
reg go;
wire done;
wire pr_stack_pop;
reg [17:0] pr_stack_top;
reg pr_stack_empty;
wire alu_go;
wire [15:0] alu_op;
wire [15:0] alu_a;
wire [15:0] alu_b;
reg [15:0] alu_out;
reg alu_done;
wire err_flag;
reg clock;
reg reset_n;

initial begin
    $from_myhdl(
        go,
        pr_stack_top,
        pr_stack_empty,
        alu_out,
        alu_done,
        clock,
        reset_n
    );
    $to_myhdl(
        ret,
        done,
        pr_stack_pop,
        alu_go,
        alu_op,
        alu_a,
        alu_b,
        err_flag
    );
end

control_unit dut(
    ret,
    go,
    done,
    pr_stack_pop,
    pr_stack_top,
    pr_stack_empty,
    alu_go,
    alu_op,
    alu_a,
    alu_b,
    alu_out,
    alu_done,
    err_flag,
    clock,
    reset_n
);

endmodule
