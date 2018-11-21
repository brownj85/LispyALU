/**
 * #############
 * INSTRUCTIONS
 * #############
 *
 * This file contains a module providing a high-level interface for a PS/2
 * keyboard, with output wires indicating the status of each of the keys
 * being tracked by the controller. Which keys are supported can be easily
 * changed, and this module should be adapted to match the needs of each
 * individual project. An additional parameter allows you to choose whether
 * the output wires stay high as long as the key is pressed down, or go
 * high for a single clock cycle when the key is initially pressed.
 *
 * The module in this file was designed for and was only tested on a DE1_SoC
 * FPGA board. Any model of FPGA other than this is not guaranteed to give
 * expected performance.
 *
 * Modules has been provided at the bottom of the page for testing purposes,
 * to see if the keyboard controller works on your board. These test modules
 * should also be modified to suit each individual project, see documentation
 * for the keyboard_interface_test modules for more details. Be sure to run
 * the test module before incorporating this controller into your project.
 *
 * The controller can operate in two modes, controlled by an instantiation
 * parameter in the module named PULSE_OR_HOLD. This parameter can be set
 * by declaring the module as follows:
 *
 * keyboard_tracker #(.PULSE_OR_HOLD(1)) <name>( ... I/O port declarations...
 *
 * Setting PULSE_OR_HOLD high on instantiating the module will cause it to
 * operate in pulse mode, in which the output for each key is sent high for
 * only one clock cycle when the key is pressed. Holding the key will not
 * cause the output to go high a second time. By contrast, if PULSE_OR_HOLD
 * is set low, the module will operate in hold mode, and the output for each
 * key will be high any time the key is pressed down.
 *
 *
 * BUG NOTE:
 * The core driver does not behave normally when at least two of the arrow keys
 * are held at the same time as another arrow key is pressed. This includes
 * instances when three or more arrow keys are pressed simultaneously.
 * Which keys are registered as being pressed in such an event may be undefined.
 *
 *
 * #########################
 * KEYBOARD PROTOCOL PRIMER
 * #########################
 *
 * The keyboard communicates with another device by sending signals through
 * its data wire. A single byte from the keyboard usually forms a code that
 * identifies a specific key. For example, the letter W is identified by the
 * hexidecimal code 1D, and the space bar is identified by hexidecimal 29.
 * When a key is pressed on the keyboard, its code is sent through the bus.
 * When a key is released, a break signal (F0) is sent, followed by the code
 * of the key that was released. Key codes are as specified by Keyboard Scan
 * Code Set 2.
 *
 * Most keys follow this pattern, of sending the key's code as a 'make' (press)
 * signal, and F0 followed by the key's code as a 'break' (release) signal.
 * Some keys follow a different pattern of signals, referred to in this file as
 * secondary codes. The only difference with secondary codes is that each
 * transmission from the keyboard is preceded by a byte with the hexadecimal
 * value E0. For example, the right arrow key will send E0 followed by its code,
 * hex 74, when pressed; it will send E0, F0, and then 74 as a break code.
 *
 * The print screen and pause keys follow neither rules, and have more complicated
 * codes. For that reason, those two keys are not supported by this controller.
 *
 *
 * #############################
 * PERSONALIZING THE CONTROLLER
 * #############################
 *
 * To add a new key to the controller, first find its code from Scan Code Set 2.
 * Then, add a local parameter named <KEY>_CODE containing the key's code. A new
 * output reg port must be added for the key, and internal registers <KEY>_lock
 * and <KEY>_press should be added too. Next, code must be added to the always
 * block inside the module to manage the values of the output.
 * 
 * See the always block for examples of the setups for several different keys.
 * The code for those keys can be copied to implement any additional keys.
 * Places inside the module (excluding output ports) where code needs to be
 * added to implement a new key are marked with TODO labels.
 *
 *
 * ################################
 * INPUT AND OUTPUT SPECIFICATIONS
 * ################################
 *
 * clock - Main clock signal for the controller. This signal is separate from
 *         the keyboard's clock signal, PS2_CLK. This input should be plugged
 *         into the same clock as the rest of the system is synchronized to.
 *
 * reset - Synchronous active-low reset signal. Resetting the controller will
 *         turn off all active keys. Calling a reset while holding keys on the
 *         keyboard may cause only the most recently pressed key to register
 *         again, as a consequence of keyboard protocol.
 *
 * PS2_CLK and PS2_DAT -
 *    These inputs correspond to the PS2_CLK and PS2_DAT signals from the board.
 *    Do NOT use PS2_CLK2 or PS2_DAT2 unless using a PS/2 splitter cable, or else
 *    neither input will be connected to anything.
 *
 * w, a, s, d, left, right, up, down, space, enter -
 *    Signals corresponding to WASD, the four arrow keys, the space bar, and
 *    enter. How these signals operate depends on the setting of PULSE_OR_HOLD.
 *
 *
 * #################
 * ACKNOWLEDGEMENTS
 * #################
 *
 * Credit for low-level PS/2 driver module (also a resource for PS/2 protocol):
 * http://www.eecg.toronto.edu/~jayar/ece241_08F/AudioVideoCores/ps2/ps2.html
 *
 */
module keyboard_tracker #(parameter PULSE_OR_HOLD = 0) (
    input clock,
	 input reset,
	 
	 inout PS2_CLK,
	 inout PS2_DAT,
	 
	 output w, a, s, d,
	 output left, right, up, down,
	 output space, enter
	 );
	 
	 // A flag indicating when the keyboard has sent a new byte.
	 wire byte_received;
	 // The most recent byte received from the keyboard.
	 wire [7:0] newest_byte;
	 	 
	 localparam // States indicating the type of code the controller expects
	            // to receive next.
	            MAKE            = 2'b00,
	            BREAK           = 2'b01,
					SECONDARY_MAKE  = 2'b10,
					SECONDARY_BREAK = 2'b11,
					
					// Make/break codes for all keys that are handled by this
					// controller. Two keys may have the same make/break codes
					// if one of them is a secondary code.
					// TODO: ADD TO HERE WHEN IMPLEMENTING NEW KEYS	
					
										
					// all numbers, square brackets, -,
					9_CODE = 8'h46,
					8_CODE = 8'h3E,
					7_CODE = 8'h3D,
					6_CODE = 8'h36,
					5_CODE = 8'h2E,
					4_CODE = 8'h25,
					3_CODE = 8'h26,
					2_CODE = 8'h1E,
					1_CODE = 8'h16,
					0_CODE = 8'h45,

					SPACE_CODE = 8'h29,
					MINUS_CODE = 8'h4E,
					LEFT_BRACKET_CODE = 8'h54,
					RIGHT_BRACKET_CODE = 8'h5B,
					ENTER_CODE = 8'h5a;


    reg [1:0] curr_state;
	 
	 // Press signals are high when their corresponding key is being pressed,
	 // and low otherwise. They directly represent the keyboard's state.
	 // TODO: ADD TO HERE WHEN IMPLEMENTING NEW KEYS	 
    reg 0_press, 1_press, 2_press, 3_press, 4_press, 5_press, 6_press, 7_press, 8_press, 9_press;
	 reg left_bracket_press, right_bracket_press, minus_press;
	 reg space_press, enter_press;
	 
	 // Lock signals prevent a key press signal from going high for more than one
	 // clock tick when pulse mode is enabled. A key becomes 'locked' as soon as
	 // it is pressed down.
	 // TODO: ADD TO HERE WHEN IMPLEMENTING NEW KEYS
	 reg 0_lock, 1_lock, 2_lock, 3_lock, 3_lock, 4_lock, 5_lock, 6_lock, 7_lock, 8_lock, 9_lock;
	 reg left_bracket_lock, right_bracket_lock, minus_lock;
	 reg space_lock, enter_lock;
	 
	 // Output is equal to the key press wires in mode 0 (hold), and is similar in
	 // mode 1 (pulse) except the signal is lowered when the key's lock goes high.
	 // TODO: ADD TO HERE WHEN IMPLEMENTING NEW KEYS
    assign zero = 0_press && ~(0_lock && PULSE_OR_HOLD);
    assign one = 1_press && ~(1_lock && PULSE_OR_HOLD);
    assign two = 2_press && ~(2_lock && PULSE_OR_HOLD);
    assign three = 3_press && ~(3_lock && PULSE_OR_HOLD);
    assign four = 4_press && ~(4_lock && PULSE_OR_HOLD);
    assign five = 5_press && ~(5_lock && PULSE_OR_HOLD);
    assign six = 6_press && ~(6_lock && PULSE_OR_HOLD);
    assign seven = 7_press && ~(7_lock && PULSE_OR_HOLD);
    assign eight = 8_press && ~(8_lock && PULSE_OR_HOLD);
    assign nine = 9_press && ~(9_lock && PULSE_OR_HOLD);

    assign left_bracket  = left_bracket_press && ~(left_bracket_lock && PULSE_OR_HOLD);
    assign right_bracket = right_bracket_press && ~(right_bracket_lock && PULSE_OR_HOLD);
    assign minus  = minus_press && ~(minus_lock && PULSE_OR_HOLD);

    assign space = space_press && ~(space_lock && PULSE_OR_HOLD);
    assign enter = enter_press && ~(enter_lock && PULSE_OR_HOLD);
	 
	 // Core PS/2 driver.
	 PS2_Controller #(.INITIALIZE_MOUSE(0)) core_driver(
	     .CLOCK_50(clock),
		  .reset(~reset),
		  .PS2_CLK(PS2_CLK),
		  .PS2_DAT(PS2_DAT),
		  .received_data(newest_byte),
		  .received_data_en(byte_received)
		  );
		  
    always @(posedge clock) begin
	     // Make is default state. State transitions are handled
        // at the bottom of the case statement below.
		  curr_state <= MAKE;
		  
		  // Lock signals rise the clock tick after the key press signal rises,
		  // and fall one clock tick after the key press signal falls. This way,
		  // only the first clock cycle has the press signal high while the
		  // lock signal is low.
		  // TODO: ADD TO HERE WHEN IMPLEMENTING NEW KEYS
		  0_lock <= 0_press;
		  1_lock <= 1_press;
		  2_lock <= 2_press;
		  3_lock <= 3_press;
		  4_lock <= 4_press;
		  5_lock <= 5_press;
		  6_lock <= 6_press;
		  7_lock <= 7_press;
		  8_lock <= 8_press;
		  9_lock <= 9_press;
		  
		  left_bracket_lock <= left_bracket_press;
		  right_bracket_lock <= right_bracket_press;
		  minus_lock <= minus_press;
		  
		  space_lock <= space_press;
		  enter_lock <= enter_press;
		  
	     if (~reset) begin
		      curr_state <= MAKE;
				
				// TODO: ADD TO HERE WHEN IMPLEMENTING NEW KEYS
				0_press <= 1'b0;
				1_press <= 1'b0;
				2_press <= 1'b0;
				3_press <= 1'b0;
				4_press <= 1'b0;
				5_press <= 1'b0;
				6_press <= 1'b0;
				7_press <= 1'b0;
				8_press <= 1'b0;
				9_press <= 1'b0;

				left_bracket_press  <= 1'b0;
				right_bracket_press <= 1'b0;
				minus_press    <= 1'b0;
				
				space_press <= 1'b0;
				enter_press <= 1'b0;
				
				0_lock <= 1'b0;
				1_lock <= 1'b0;
				2_lock <= 1'b0;
				3_lock <= 1'b0;
				4_lock <= 1'b0;
				5_lock <= 1'b0;
				6_lock <= 1'b0;
				7_lock <= 1'b0;
				8_lock <= 1'b0;
				9_lock <= 1'b0;

				left_brakcet_lock  <= 1'b0;
				right_bracket_lock <= 1'b0;
				
				minus_lock  <= 1'b0;
				space_lock <= 1'b0;
				enter_lock <= 1'b0;
        end
		  else if (byte_received) begin
		      // Respond to the newest byte received from the keyboard,
				// by either making or breaking the specified key, or changing
				// state according to special bytes.
				case (newest_byte)
				    // TODO: ADD TO HERE WHEN IMPLEMENTING NEW KEYS
		          ZERO_CODE: 0_press <= curr_state == MAKE;
					 ONE_CODE: 1_press <= curr_state == MAKE;
					 TWO_CODE: 2_press <= curr_state == MAKE;
					 THREE_CODE: 3_press <= curr_state == MAKE;
					 FOUR_CODE: 4_press <= curr_state == MAKE;
					 FIVE_CODE: 5_press <= curr_state == MAKE;
					 SIX_CODE: 6_press <= curr_state == MAKE;
					 SEVEN_CODE: 7_press <= curr_state == MAKE;
					 EIGHT_CODE: 8_press <= curr_state == MAKE;
					 NINE_CODE: 9_press <= curr_state == MAKE;

					 
					 LEFT_BRACKET_CODE:  left_bracket_press  <= curr_state == MAKE;
					 RIGHT_BRACKET_CODE: right_bracket_press <= curr_state == MAKE;
					 MINUS_CODE:    minus_press    <= curr_state == MAKE;
					 
					 SPACE_CODE: space_press <= curr_state == MAKE;
					 ENTER_CODE: enter_press <= curr_state == MAKE;

					 // State transition logic.
					 // An F0 signal indicates a key is being released. An E0 signal
					 // means that a secondary signal is being used, which will be
					 // followed by a regular set of make/break signals.
					 8'he0: curr_state <= SECONDARY_MAKE;
					 8'hf0: curr_state <= curr_state == MAKE ? BREAK : SECONDARY_BREAK;
		      endcase
        end
        else begin
		      // Default case if no byte is received.
		      curr_state <= curr_state;
		  end
    end
endmodule


/**
 * ########
 * TESTING
 * ########
 *
 * The modules below will test the functionality of the keyboard controller
 * in this file. Each of the two modules tests one mode of the keyboard, which is
 * specified in the module name. The ten default keys supported by the controller
 * are all displayed on LEDR. Behaviours of the LEDs are described in the test
 * modules' documentation headers.
 *
 * Keys are mapped to the LEDs as follows:
 *
 * Left, right, up, down arrows = LEDR[0 - 3]
 * WASD      = LEDR[4 - 7]
 * Space bar = LEDR[8]
 * Enter     = LEDR[9]
 *
 * Pressing KEY[0] causes the system to reset.
 *
 * If none of the lights turn on when any of those keys are pressed, it is
 * possible that the core PS/2 driver does not work on your board. In that
 * case you should find another keyboard controller that works for your board.
 * For any other problems, it is probably the case that registers are being
 * updated at the wrong clock ticks. For that case, it may be worth
 * disconnecting the controller from its core driver and manually setting the
 * bytes received from the keyboard in a Modelsim simulation. Another option
 * is to add several outputs to the keyboard_tracker module which are assigned
 * to the few most recently received bytes from the keyboard. These bytes can
 * be displayed on hex displays (hex decoder module not provided) to see what
 * codes are arriving from the keyboard.
 *
 * To test extra keys that you have added to the controller, simply change the
 * output ports on the keyboard controller module instantiated inside to
 * include your new keys. How these keys are displayed on the LEDs is up to you,
 * and you may remove and reassign any outputs on the LEDs for keys that are
 * not used by your project.
 *
 *
 * BUG REMINDER:
 * The core driver does not behave normally when at least two of the arrow keys
 * are held at the same time as another arrow key is pressed. This includes
 * instances when three or more arrow keys are pressed simultaneously.
 * Which keys are registered as being pressed in such an event may be undefined.
 */

/**
 * Tester module for mode 0 (hold) mode. LED's on the board should turn on whenever
 * the corresponding key is pressed, and turn off when the key is released.
 */ 
module keyboard_interface_test_mode0(
    input CLOCK_50,
	 input [3:0] KEY,
	 
	 inout PS2_CLK,
	 inout PS2_DAT,
	 
	 output [9:0] LEDR
	 );
	 
	 keyboard_tracker #(.PULSE_OR_HOLD(0)) tester(
	     .clock(CLOCK_50),
		  .reset(KEY[0]),
		  .PS2_CLK(PS2_CLK),
		  .PS2_DAT(PS2_DAT),
		  .w(LEDR[4]),
		  .a(LEDR[5]),
		  .s(LEDR[6]),
		  .d(LEDR[7]),
		  .left(LEDR[0]),
		  .right(LEDR[1]),
		  .up(LEDR[2]),
		  .down(LEDR[3]),
		  .space(LEDR[8]),
		  .enter(LEDR[9])
		  );
endmodule


/**
 * Tester module for mode 1 (pulse). LEDs on the board should flip once as soon
 * as the corresponding key is pressed down. Holding a key should not continue
 * to change the output, nor should the output change on key release.
 */ 
module keyboard_interface_test_mode1(
    input CLOCK_50,
	 input [3:0] KEY,
	 
	 inout PS2_CLK,
	 inout PS2_DAT,
	 
	 output [9:0] LEDR
	 );
	 
	 // Wires representing direct output from the keyboard controller.
	 wire w_pulse,
	      a_pulse,
			s_pulse,
			d_pulse,
			left_pulse,
			right_pulse,
			up_pulse,
			down_pulse,
			space_pulse,
			enter_pulse;
			
    // Registers holding the values displayed on the LEDs.
    reg  w_tot,
	      a_tot,
			s_tot,
			d_tot,
			left_tot,
			right_tot,
			up_tot,
			down_tot,
			space_tot,
			enter_tot;

    assign LEDR[4] = w_tot;
	 assign LEDR[5] = a_tot;
	 assign LEDR[6] = s_tot;
	 assign LEDR[7] = d_tot;
	 assign LEDR[0] = left_tot;
	 assign LEDR[1] = right_tot;
	 assign LEDR[2] = up_tot;
	 assign LEDR[3] = down_tot;
	 assign LEDR[8] = space_tot;
	 assign LEDR[9] = enter_tot;
	 
	 keyboard_tracker #(.PULSE_OR_HOLD(1)) tester_mode1(
	     .clock(CLOCK_50),
		  .reset(KEY[0]),
		  .PS2_CLK(PS2_CLK),
		  .PS2_DAT(PS2_DAT),
		  .w(w_pulse),
		  .a(a_pulse),
		  .s(s_pulse),
		  .d(d_pulse),
		  .left(left_pulse),
		  .right(right_pulse),
		  .up(up_pulse),
		  .down(down_pulse),
		  .space(space_pulse),
		  .enter(enter_pulse)
		  );

    always @(posedge CLOCK_50) begin
	     if (~KEY[0]) begin
		      // Reset signal
		      w_tot <= 1'b0;
				a_tot <= 1'b0;
				s_tot <= 1'b0;
				d_tot <= 1'b0;
				
				left_tot  <= 1'b0;
				right_tot <= 1'b0;
				up_tot    <= 1'b0;
				down_tot  <= 1'b0;
				
				space_tot <= 1'b0;
				enter_tot <= 1'b0;
		  end
		  else begin
		      // State display wires (xxx_tot) flip values when their
				// corresponding key is pressed.
	         w_tot <= w_tot + w_pulse;
		      a_tot <= a_tot + a_pulse;
		      s_tot <= s_tot + s_pulse;
		      d_tot <= d_tot + d_pulse;
				
		      left_tot <= left_tot + left_pulse;
		      right_tot <= right_tot + right_pulse;
		      up_tot <= up_tot + up_pulse;
		      down_tot <= down_tot + down_pulse;
				
		      space_tot <= space_tot + space_pulse;
		      enter_tot <= enter_tot + enter_pulse;
		  end
    end
endmodule