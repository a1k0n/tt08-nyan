#include <stdint.h>
#include "Vtt_um_a1k0n_nyancat.h"
#include "verilated.h"
#include <SDL2/SDL.h>

#define H_TOTAL 640+48+16+96
#define H_DISPLAY 640
#define V_TOTAL 525
#define V_DISPLAY 480

#undef SAVE_FRAMES

#if SAVE_FRAMES
#include <SDL2/SDL_image.h>
#endif

static inline uint32_t lowextend6(uint32_t x) {
  // take a 2-bit input, shift left extending to 8 bits, but cloning into the
  // remaining 6 bits
  // 00 -> 00000000
  // 01 -> 01010101
  // 10 -> 10101010
  // 11 -> 11111111
  return x * 0x55;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);

  Vtt_um_a1k0n_nyancat* top = new Vtt_um_a1k0n_nyancat;

  top->rst_n = 1;
  top->clk = 0; top->eval(); top->clk = 1; top->eval();
  top->rst_n = 0;
  top->clk = 0; top->eval(); top->clk = 1; top->eval();
  top->rst_n = 1;

  // Initialize SDL
  if (SDL_Init(SDL_INIT_VIDEO) != 0) {
    SDL_Log("Failed to initialize SDL: %s", SDL_GetError());
    return 1;
  }

  // Create a window
  SDL_Window* window = SDL_CreateWindow("VGA Demo", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, H_DISPLAY, V_DISPLAY, 0);
  if (window == nullptr) {
    SDL_Log("Failed to create window: %s", SDL_GetError());
    SDL_Quit();
    return 1;
  }

  // Create a renderer and get a pointer to a framebuffer
  SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
  if (renderer == nullptr) {
    SDL_Log("Failed to create renderer: %s", SDL_GetError());
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 1;
  }

  // Create a texture that we'll use as our framebuffer
  SDL_Texture* texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING, H_DISPLAY, V_DISPLAY);
  if (texture == nullptr) {
    SDL_Log("Failed to create texture: %s", SDL_GetError());
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 1;
  }

  // Main loop
  bool quit = false;
  int frame = 0;
  while (!quit) {
    // Handle events
    SDL_Event event;
    while (SDL_PollEvent(&event)) {
      if (event.type == SDL_QUIT) {
        quit = true;
      }
    }

    // Get a framebuffer pointer
    uint32_t* pixels;
    int pitch;
    int ret = SDL_LockTexture(texture, nullptr, (void**)&pixels, &pitch);
    if (ret != 0) {
      SDL_Log("Failed to lock texture: %s", SDL_GetError());
      break;
    }

    if (pitch != H_DISPLAY*4) {
      SDL_Log("Unexpected pitch: %d", pitch);
      break;
    }

    int k = 0;
    for(int v = 0; v < V_TOTAL; v++) {
      for(int h = 0; h < H_TOTAL; h++) {
        // clock the system
        top->clk = 0; top->eval(); top->clk = 1; top->eval();
        if (v < V_DISPLAY && h < H_DISPLAY) {
          //   assign uo_out = {hsync, B[0], G[0], R[0], vsync, B[1], G[1], R[1]};
          uint8_t o = top->uo_out;
          uint32_t r = ((o & 1) << 1) | ((o & 16) >> 4);
          uint32_t g = (o & 2) | ((o & 32) >> 5);
          uint32_t b = ((o & 4) >> 1) | ((o & 64) >> 6);
          r = lowextend6(r&3) << 16;
          g = lowextend6(g&3) << 8;
          b = lowextend6(b&3);
          uint32_t color = 0xFF000000 | r | g | b;
          pixels[k] = color;
          k++;
        }
      }
    }

#if SAVE_FRAMES
    // Save the frame to a file
    if (frame&1) {
      char filename[64];
      sprintf(filename, "frame%04d.png", frame>>1);
      SDL_Surface* surface = SDL_CreateRGBSurfaceFrom(pixels, H_DISPLAY, V_DISPLAY*2, 32, H_DISPLAY*4, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000);
      IMG_SavePNG(surface, filename);
      SDL_FreeSurface(surface);
    }
#endif
    frame++;
    
    // Unlock the texture
    SDL_UnlockTexture(texture);

    SDL_RenderCopy(renderer, texture, nullptr, nullptr);

    // Update the screen
    SDL_RenderPresent(renderer);
  }

  // Cleanup
  SDL_DestroyRenderer(renderer);
  SDL_DestroyWindow(window);
  SDL_Quit();

  return 0;
}
