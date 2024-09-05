import numpy as np
from gamma import gamma_correct, dither_correct

bgr = 0x0f
bgg = 0x4d
bgb = 0x8f

palette = np.array([
  bgr, bgg, bgb,
  0xff, 0x00, 0x00,
  0xff, 0x99, 0x00,
  0xff, 0xff, 0x00,
  0x33, 0xff, 0x00,
  0x00, 0x99, 0xff,
  0x66, 0x33, 0xff,
  bgr, bgg, bgb])

print(palette)
palette = gamma_correct(palette)
palette = dither_correct(palette)
print(palette)


print('  reg [4:0] rainbow_r[0:7];')
print('  reg [4:0] rainbow_g[0:7];')
print('  reg [4:0] rainbow_b[0:7];')
print('initial begin')
print('  rainbow_r = \'{')
print('    ', ', '.join([f'\'h{x:02x}' for x in palette[0::3]]))
print('  };')
print('  rainbow_g = \'{')
print('    ', ', '.join([f'\'h{x:02x}' for x in palette[1::3]]))
print('  };')
print('  rainbow_b = \'{')
print('    ', ', '.join([f'\'h{x:02x}' for x in palette[2::3]]))
print('  };')
print('end')

rhex = open("../data/rainbow_r.hex", "w")
ghex = open("../data/rainbow_g.hex", "w")
bhex = open("../data/rainbow_b.hex", "w")

rhex.write(' '.join([f'{x:02x}' for x in palette[0::3]]))
ghex.write(' '.join([f'{x:02x}' for x in palette[1::3]]))
bhex.write(' '.join([f'{x:02x}' for x in palette[2::3]]))
rhex.write('\n')
ghex.write('\n')
bhex.write('\n')

rhex.close()
ghex.close()
bhex.close()
