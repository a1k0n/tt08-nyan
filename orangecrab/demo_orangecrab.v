module demo_orangecrab (
    input clk48,
    output gpio_0,  // vsync
    output gpio_1,  // hsync
    output gpio_a0, // BlueH
    output gpio_a1, // GreenH
    output gpio_a2, // RedH
    output gpio_a3, // BlueL
    output gpio_a4, // GreenL
    output gpio_a5, // RedL
    output gpio_13 // audio out
);

// assign uo_out = {hsync, B[0], G[0], R[0], vsync, B[1], G[1], R[1]};

wire [7:0] uo_out, uio_out, uio_oe;
reg [1:0] poweron_reset = 3;
wire [1:0] R = {uo_out[0], uo_out[4]};
wire [1:0] G = {uo_out[1], uo_out[5]};
wire [1:0] B = {uo_out[2], uo_out[6]};
wire hsync = uo_out[7];
wire vsync = uo_out[3];
wire audio_out = uio_out[7];

reg clkdiv = 0;
always @(posedge clk48) begin
  clkdiv <= ~clkdiv;
end

tt_um_a1k0n_nyancat nyan(
  .ui_in(0),
  .uo_out(uo_out),
  .uio_in(0),
  .uio_out(uio_out),
  .uio_oe(uio_oe),
  .clk(clkdiv),
  .rst_n(poweron_reset == 0)
);

always @(posedge clk48) begin
  if (poweron_reset != 0)
    poweron_reset <= poweron_reset - 1;
end

assign gpio_a0 = B[1];
assign gpio_a1 = G[1];
assign gpio_a2 = R[1];
assign gpio_a3 = B[0];
assign gpio_a4 = G[0];
assign gpio_a5 = R[0];
assign gpio_0 = vsync;
assign gpio_1 = hsync;
assign gpio_13 = audio_out;

endmodule
