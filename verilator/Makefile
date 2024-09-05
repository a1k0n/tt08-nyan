TARGETS = tt_um_vga_example 
VERILATOR = verilator
VERILATOR_FLAGS = -Wall --trace -cc --exe -I../src
CPP = g++
CPP_FLAGS = -std=c++11 -Wall

all: $(TARGETS)

tt_um_vga_example: ../src/project.v ../src/hvsync_generator.v tt_um_vga_example_tb.cpp
	$(VERILATOR) -Wno-widthexpand -Wno-widthtrunc --trace -cc --exe $^ -CFLAGS "-g -O3" --LDFLAGS "-lSDL2" --top-module tt_um_vga_example
	$(MAKE) -C obj_dir -f V$@.mk
	cp obj_dir/V$@ $@

#audiotrack: ../src/audiotrack.v ../src/songrom.v audiotrack_tb.cpp
#	$(VERILATOR) --trace -cc --exe $^ -CFLAGS "-g -O3" --LDFLAGS "-lSDL2" --top-module audiotrack
#	$(MAKE) -C obj_dir -f V$@.mk
#	cp obj_dir/V$@ $@

%: ../src/%.v %_tb.cpp
	$(VERILATOR) $(VERILATOR_FLAGS) $< $*_tb.cpp
	$(MAKE) -C obj_dir -f V$@.mk
	cp obj_dir/V$@ $@

clean:
	rm -rf obj_dir
	rm -f $(TARGETS)
	rm -f *.vcd

.PHONY: all clean
