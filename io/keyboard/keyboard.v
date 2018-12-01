module keyboard(
			
			input CLOCK_50,
			input[3:0] KEY,
			
			inout PS2_CLK,
			inout PS2_DAT,
			
			output reg[7:0] char,
            output reg break,
            output reg delete,
            output reg return,
	
			output[6:0] HEX0,
			output[6:0] HEX1
			);
		
	wire[7:0] newest_byte;
	wire byte_received;
	
	reg shift;
	
	localparam
			
			SHIFT = 8'h12,
			ZERO	= 8'h45,
			ONE	= 8'h16,
			TWO	= 8'h1e,
			THREE	= 8'h26,
			FOUR	= 8'h25,
			FIVE	= 8'h2e,
			SIX	= 8'h36,
			SEVEN	= 8'h3d,
			EIGHT	= 8'h3e,
			NINE	= 8'h46,
			MNS	= 8'h4e,
			PLS	= 8'h55,
			SLSH	= 8'h2F,
			
			BREAK = 8'hF0,

            ENTER = 8'h53,
            BKSP = 8'h66,

	
	
	PS2_Controller #(.INITIALIZE_MOUSE(0)) core_driver(
	     .CLOCK_50(CLOCK_50),
		  .reset(~KEY[0]),
		  .PS2_CLK(PS2_CLK),
		  .PS2_DAT(PS2_DAT),
		  .received_data(newest_byte),
		  .received_data_en(byte_received)
		  );
	
	hex_decoder hex0(
			.hex_digit(char[3:0]),
			.segments(HEX0)
			);
	hex_decoder hex1(
			.hex_digit(char[7:4]),
			.segments(HEX1)
			);
		
	always @(posedge CLOCK_50)
	begin: set_byte
		if (KEY[0] == 0) begin
			char <= 0;
			shift <= 0;
            delete <= 0;
            return <= 0;
		end
	
		else if (byte_received) begin
		
			if (newest_byte == BREAK)
				break <= 1;
			
			else if (newest_byte == SHIFT)
				shift <= ~break;

            else if (newest_byte == BKSP):
                delete <= ~break;

            else if (newest_byte == ENTER):
                return  <= ~break;
			
			if (break) begin
					break <= 0;
                    return <= 0;
                    delete <= 0;

					case(newest_byte)
						ZERO: begin
							if(shift)
								char <= 8'd41;
							else
								char <= 8'd48;
						end
						NINE: begin
							if(shift)
								char <= 8'd40;
							else
								char <= 8'd57;
						end
						EIGHT: begin
							if(shift)
								char <= 8'd42;
							else
								char <= 8'd56;
						end
						SEVEN: char <= 8'd55;
						SIX: char <= 8'd54;
						FIVE: char <= 8'd53;
						FOUR: char <= 8'd52;
						THREE: char <= 8'd51;
						TWO: char <= 8'd50;
						ONE: char <= 8'd49;
						MNS: char <= 8'd45;
						PLS: char <= 8'd43;
						SLSH: char <= 8'd47;
                        ENTER: char <= 8'd128;
					endcase	
			end
		end
	end
	
endmodule
			
	
