

module mem(
	address,
	clock,
	data,
	wren,
	counter_enable,
	counter_reset,
	counter_output,
	q
	);
	
	input	[7:0]  address;
	input	  clock;
	input	[15:0]  data;
	input	  wren;
	
	input counter_enable;
	input counter_reset;
	output counter_output; 
	output	[15:0]  q;
	
	reg [3:0] count;
	
	ram256x16 mem( 
		.address   	(address),
		.clock		(clock), 
		.data		(data), 
		.wren		(wren), 
		.q 			(q)
		);
	
	always @(posedge clock)
	begin
		if (counter_reset) 
			count <= 3'd0 ;
		else if (counter_enable) 
	    	count <= count + 3'd1;
	end
	assign counter_out = count;
	
		
endmodule
