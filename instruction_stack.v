module instruction_stack(in, out, push, pop, current_state, clk, reset_n);

	input[23:0] in;

	output reg[23:0] out;

	input push, pop;

	input clk;
	input reset_n;

	output[3:0]  current_state;


	reg[23:0] memory[255:0];

	reg[7:0] stack_ptr;

	wire incr, decr, read, write;
	
	control ctrl(push, pop, incr, decr, read, write, clk, reset_n);

	always@(posedge clk)
	begin
		if(!reset_n)
			out <= 24'b0;
		else begin
			if(incr)
				stack_ptr <= stack_ptr + 1;
			if(decr)
				stack_ptr <= stack_ptr - 1;
			if(read)
				out <= memory[stack_ptr];
			if(write)
				memory[stack_ptr] <= in;
		end
	end

endmodule


module control(push, pop, incr, decr, read, write, clk, reset_n);
	
	input push, pop;

	reg[3:0] current_state;
	reg[3:0] next_state;
	
	input clk, reset_n;

	localparam	HOLD = 4'b0000,
			PUSH_0 = 4'b1000,
			PUSH_1 = 4'b0001,
			POP_0 = 4'b0010,
			POP_1 = 4'b0100;

	output incr, decr, read, write;

	assign {incr, decr, read, write} = current_state;

	//state table
	always@(*)
	begin: state_table
		case(current_state)
			HOLD: begin
				if(push) 
					next_state = PUSH_0;
				else if(pop)
					next_state = POP_0;
				else
					next_state = HOLD;
			end
			PUSH_0: next_state = PUSH_1;
			PUSH_1: begin
				if(push)
					next_state = PUSH_0;
				else if(pop)
					next_state = POP_0;
				else
					next_state = HOLD;
			end
			POP_0: next_state = POP_1;
			POP_1: begin
				if(push)
					next_state = PUSH_0;
				else if(pop)
					next_state = POP_0;
				else
					next_state = HOLD;
			end
			default: next_state = HOLD;
		endcase
	end

	always@(posedge clk) 
	begin
		if(!reset_n) 
			current_state <= HOLD;
		else 
			current_state <= next_state;
	end

	endmodule
	




			







