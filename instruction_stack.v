module instruction_stack(in, out, push, pop, clk, reset_n);

	input[23:0] in;

	output reg[23:0] out;

	input push, pop;

	input clk;
	input reset_n;

	reg[23:0] memory[255:0];

	reg[7:0] stack_ptr;

	reg[2:0] current_state;
	reg[2:0] next_state;

	localparam 	HOLD = 3'd0,
			PUSH_0 = 3'd1,
			PUSH_1 = 3'd2,
			POP_0 = 3'd3,
			POP_1 = 3'd4;

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
	
	always@(posedge clk, negedge reset_n) 
	begin
		if(!reset_n) 
			stack_ptr <= 8'b0;
		else begin
			case(current_state)
				PUSH_0: stack_ptr <= stack_ptr + 1;
				PUSH_1: memory[stack_ptr] <= in;
				POP_0: out <= memory[stack_ptr];
				POP_1: stack_ptr <= stack_ptr - 1;
				default: out <= 24'b0;
			endcase
		end
	end

endmodule


				
			







