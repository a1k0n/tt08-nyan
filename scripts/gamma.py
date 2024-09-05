import numpy as np

# Function to convert sRGB to linear RGB
def srgb_to_linear(srgb):
    srgb = srgb / 255.0
    return np.where(srgb <= 0.04045,
                    srgb / 12.92,
                    ((srgb + 0.055) / 1.055) ** 2.4)

def gamma_correct_srgb(palette):
    # Convert palette from sRGB to linear RGB
    linear_palette = np.zeros_like(palette)
    for i in range(0, len(palette), 3):
        r, g, b = palette[i:i+3]
        linear_r, linear_g, linear_b = srgb_to_linear(np.array([r, g, b]))
        linear_palette[i] = int(linear_r * 255)
        linear_palette[i+1] = int(linear_g * 255)
        linear_palette[i+2] = int(linear_b * 255)
    return linear_palette


def gamma_correct(palette, gamma=1.6):
    # leave the high bit alone, gamma correct the lower 7 bits
    return palette
    #return (255 * ((palette/255)**gamma)).astype(np.uint8)
    #return palette
    #high = palette >> 7
    #low = (palette << 1) & 0xff
    #low = (255 * ((palette/255)**gamma)).astype(np.uint8)
    #return (high << 7) | (low >> 1)

def dither_correct(palette):
    # pre-emphasize the palette entries so that full scale (0xff) is 0x30
    # so that adding the 4-bit dithering pattern will create the correct output in the 2 MSBs
    # return (palette * 0x30 / 0xff).astype(np.uint8)

    # actually let's just use 4-level dithering
    return (palette * 0xc / 0xff).astype(np.uint8)