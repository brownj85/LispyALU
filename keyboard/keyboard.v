module keyboard(
			
			input CLOCK_50,
			input[4:0] KEY,
			
			inout PS2_CLK,
			inout PS2_DAT,
			
			output[10:0] LEDR,
			
			output reg[8:0] code_out
			);
			
	
	wire zero, one, two, three, four, five, six, seven, eight, nine;
   wire left_bracket, right_bracket, minus;
   wire space, enter;
	
	
	keyboard_tracker(
			.clock(CLOCK_50),
			.reset(KEY[0]),
			.PS2_CLK(PS2_CLK),
			.PS2_DAT(PS2_DAT),
			
			.zero(zero),
			.one(one),
			.two(two),
			.three(three),
			.four(four),
			.five(five),
			.six(six),
			.seven(seven),
			.eight(eight),
			.nine(nine),
			.right_bracket(right_bracket),
			.left_bracket(left_bracket),
			.minus(minus),
			.plus(plus),
			.mult(mult),
			.space(space),
			.enter(enter)
			);
	
	
	
	
	always @(*)
	begin set_code:
		
		if (zero)
			code_out <= 8'd48;
		else if (one)
			code_out <= 8'd49;
		else if (two)
			code_out <= 8'd50;
		else if (three)
			code_out <= 8'd51;
		else if (four)
			code_out <= 8'd52;
		else if (five)
			code_out <= 8'd53;
		else if (six)
			code_out <= 8'd54;
		else if (seven)
			code_out <= 8'd55;
		else if (eight)
			code_out <= 8'd56;
		else if (nine)
			code_out <= 8'd57;
		
		else if (right_bracket)
			code_out <= 8'd93;
		else if (left_bracket)
			code_out <= 8'd91;
		
		else if (minus)
			code_out <= 8'd45;
			
		else if (space)
			code_out <= 8'd32;
		else if (enter)
			code_out <= 8'd3;
		
		else if (mult)
			code_out <= 8'd42;
		else if (plus)
			code_out <= 8'd43;
	end
	
	assign LEDR[8:0] = code_out;
	
endmodule
			
	