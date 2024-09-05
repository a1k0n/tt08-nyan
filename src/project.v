/*
 * Copyright (c) 2024 Andy Sloane
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_vga_example(
  input  wire [7:0] ui_in,    // Dedicated inputs
  output wire [7:0] uo_out,   // Dedicated outputs
  input  wire [7:0] uio_in,   // IOs: Input path
  output wire [7:0] uio_out,  // IOs: Output path
  output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
  input  wire       ena,      // always 1 when the design is powered, so you can ignore it
  input  wire       clk,      // clock
  input  wire       rst_n     // reset_n - low to reset
);

  // VGA signals
  wire hsync;
  wire vsync;
  wire [1:0] R;
  wire [1:0] G;
  wire [1:0] B;
  wire video_active;
  wire [9:0] pix_x;
  wire [9:0] pix_y;

  // TinyVGA PMOD
  assign uo_out = {hsync, B[0], G[0], R[0], vsync, B[1], G[1], R[1]};

  // Unused outputs assigned to 0.
  assign uio_out = 0;
  assign uio_oe  = 0;

  // Suppress unused signals warning
  wire _unused_ok = &{ena, ui_in, uio_in, r[2:0]};

  reg [9:0] counter;
  reg [3:0] nyanframe;

  hvsync_generator hvsync_gen(
    .clk(clk),
    .reset(~rst_n),
    .hsync(hsync),
    .vsync(vsync),
    .display_on(video_active),
    .hpos(pix_x),
    .vpos(pix_y)
  );
  
  wire [9:0] moving_x = pix_x + (counter<<2);

  reg [4:0] palette_r[0:7];
  reg [4:0] palette_g[0:7];
  reg [4:0] palette_b[0:7];
  initial begin
    $readmemh("../data/palette_r.hex", palette_r);
    $readmemh("../data/palette_g.hex", palette_g);
    $readmemh("../data/palette_b.hex", palette_b);
  end

  reg [4:0] rainbow_r[0:7];
  reg [4:0] rainbow_g[0:7];
  reg [4:0] rainbow_b[0:7];
  initial begin
    $readmemh("../data/rainbow_r.hex", rainbow_r);  
    $readmemh("../data/rainbow_g.hex", rainbow_g);
    $readmemh("../data/rainbow_b.hex", rainbow_b);
  end
  reg [2:0] nyan[0:12287];
  initial begin
    $readmemh("../data/nyan.hex", nyan);
  end

  wire [1:0] bi = pix_x[1:0]; // ^ {3{counter[0]}};
  wire [1:0] bj = pix_y[1:0];
  wire [9:0] bx = bi ^ bj;
  wire [3:0] bayer = {bx[0], bi[0], bx[1], bi[1]};

  wire [7:0] nyan_x = pix_x[9:3] - 24;
  wire [7:0] nyan_y = pix_y[9:3] - 19;

  wire [2:0] idx = ((nyan_x < 34) && (nyan_y < 21)) ? nyan[{nyanframe, nyan_y[4:0], nyan_x[5:0]}] : 0;
  wire rainbow_on = (idx == 0 || nyan_x > 33) && (pix_x < 300) && (nyan_y < 18);

  wire [3:0] rainbow_off = pix_y[7:3] - 5 + moving_x[6];
  wire [4:0] r = rainbow_on ? rainbow_r[rainbow_off[3:1]] : palette_r[idx];
  wire [4:0] g = rainbow_on ? rainbow_g[rainbow_off[3:1]] : palette_g[idx];
  wire [4:0] b = rainbow_on ? rainbow_b[rainbow_off[3:1]] : palette_b[idx];

  wire [4:0] dr = r[3:0] + bayer + {4'b0, r[0]};
  wire [4:0] dg = g[3:0] + bayer + {4'b0, g[0]};
  wire [4:0] db = b[3:0] + bayer + {4'b0, b[0]};

  assign R = video_active ? {r[4], dr[4]} : 2'b0;
  assign G = video_active ? {g[4], dg[4]} : 2'b0;
  assign B = video_active ? {b[4], db[4]} : 2'b0;
  
  always @(posedge vsync) begin
    if (~rst_n) begin
      counter <= 0;
      nyanframe <= 0;
    end else begin
      counter <= counter + 1;
      if (counter[1:0] == 0) begin
        if (nyanframe == 5) begin
          nyanframe <= 0;
        end else begin
          nyanframe <= nyanframe + 1;
        end
      end
      
    end
  end
  
endmodule
