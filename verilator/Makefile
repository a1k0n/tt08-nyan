TARGETS = tt_um_a1k0n_nyancat 
VERILATOR = verilator
VERILATOR_FLAGS = -Wall --trace -cc --exe -I../src
CPP = g++
CPP_FLAGS = -std=c++11 -Wall

all: $(TARGETS)

tt_um_a1k0n_nyancat: ../src/tt_um_a1k0n_nyancat.v ../src/hvsync_generator.v nyancat.cpp
#tt_um_a1k0n_nyancat: ../src/reduced.v nyancat.cpp
	$(VERILATOR) -Wno-widthexpand -Wno-widthtrunc --trace -cc --exe $^ -CFLAGS "-g -O3" --LDFLAGS "-lSDL2" --top-module tt_um_a1k0n_nyancat
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
