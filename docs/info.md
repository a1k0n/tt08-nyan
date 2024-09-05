<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

# VGA nyan cat

![nyancat preview](preview.png)

## How it works

Outputs nyancat on VGA with music!

Colors and animation are all from the original nyan.cat site, using a 2x2 Bayer
dithering matrix which inverts on alternate frames for better color rendition on
the Tiny VGA Pmod.

Sound is generated from a MIDI file, split into melody and bass parts. Melody
and bass are each square waves mixed with a simple exponential decay envelope,
which is then fed to a 7-bit sigma-delta stage.

Unfortunately I had to prune the backround starfield to fit within 1 tile.

## How to test

Set clock to 25.175MHz or thereabouts, give reset pulse, and enjoy

## External hardware

[TinyVGA Pmod](https://github.com/mole99/tiny-vga) for video on o[7:0].

1-bit sound on io[7], compatible with [Tiny Tapeout Audio
Pmod](https://github.com/MichaelBell/tt-audio-pmod), or any basic ~20kHz RC filter
on io7 to an amplifier will work.
