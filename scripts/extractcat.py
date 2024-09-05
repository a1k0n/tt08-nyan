import os
import sys
import numpy as np
from PIL import Image
from gamma import gamma_correct, dither_correct

bgr = 0x0f
bgg = 0x4d
bgb = 0x8f

# Open the original GIF
original_gif = Image.open("../original.gif")
palette = original_gif.getpalette()

# Extract palette
original_gif.seek(1)
frame = original_gif.copy()
frame = frame.convert('P', palette=palette, colors=len(palette)//3)
palette = frame.getpalette()
palette = np.array(palette)

palette[:3] = [bgr, bgg, bgb]  # extracted from rainbow.png
print(palette)

# Replace the original palette with the gamma-corrected one
palette = gamma_correct(palette)
palette = dither_correct(palette)

print("Gamma-corrected palette:")
print(palette)


# print this as a verilog `initial` block
print('  reg [5:0] palette_r[0:7];')
print('  reg [5:0] palette_g[0:7];')
print('  reg [5:0] palette_b[0:7];')
print('initial begin')
print('  palette_r = \'{')
print('    ', ', '.join([f'\'h{x:02x}' for x in palette[0::3]]))
print('  };')
print('  palette_g = \'{')
print('    ', ', '.join([f'\'h{x:02x}' for x in palette[1::3]]))
print('  };')
print('  palette_b = \'{')
print('    ', ', '.join([f'\'h{x:02x}' for x in palette[2::3]]))
print('  };')
print('end')

if True:
    palr = open("../data/palette_r.hex", "w")
    palg = open("../data/palette_g.hex", "w")
    palb = open("../data/palette_b.hex", "w")
    palr.write(' '.join([f'{x:02x}' for x in palette[0::3]]))
    palg.write(' '.join([f'{x:02x}' for x in palette[1::3]]))
    palb.write(' '.join([f'{x:02x}' for x in palette[2::3]]))
    palr.write('\n')
    palg.write('\n')
    palb.write('\n')
    palr.close()
    palg.close()
    palb.close()

# original image is 34x21; we need to pad that to 64x32 with x's

datasiz = 6 * 64 * 32

nyanhex = open("../data/nyan.hex", "w")

print('  reg [2:0] nyan[0:%d];' % (datasiz-1))
print('initial begin')
print('  nyan = \'{')

# Extract and process each frame
for i in range(6, 12):
    original_gif.seek(i)
    frame = original_gif.copy()
    
    frame = frame.convert('P', palette=palette)
    
    indexed_data = np.array(frame)[::8, ::8]
    
    for row in indexed_data:
        print('    ', ''.join([f'{x:01x},' for x in row]) + ''.join(['0,' for _ in range(64-len(row))]))
        nyanhex.write(' '.join([f'{x:01x}' for x in row]) + ' ' + ' '.join(['0' for _ in range(64-len(row))]) + '\n')
    for _ in range(32-indexed_data.shape[0]):
        print('    ', ''.join(['0,' for _ in range(64)]))
        nyanhex.write(' '.join(['0' for _ in range(64)]) + '\n')

print('  };')
print('end')

# fill nyan.hex with x's up to 16384 entries
print("filling nyan.hex with %d x's" % (16384 - datasiz))
for _ in range(16384 - datasiz):
    nyanhex.write('x ')
nyanhex.write('\n')

nyanhex.close()
