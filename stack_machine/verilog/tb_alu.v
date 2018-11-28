module tb_alu;

reg [15:0] alu_a;
reg [15:0] alu_b;
reg [15:0] alu_op;
wire [15:0] alu_out;
reg go;
wire done;
wire err_flag;
reg clock;
reg reset_n;

initial begin
    $from_myhdl(
        alu_a,
        alu_b,
        alu_op,
        go,
        clock,
        reset_n
    );
    $to_myhdl(
        alu_out,
        done,
        err_flag
    );
end

alu dut(
    alu_a,
    alu_b,
    alu_op,
    alu_out,
    go,
    done,
    err_flag,
    clock,
    reset_n
);

endmodule
