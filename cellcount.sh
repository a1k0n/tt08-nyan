LIB=$HOME/.volare/volare/sky130/versions/bdc9412b3e468c102d01b7cf6337be06ec6e9c9a/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib

yosys -p "read_verilog $*; flatten; synth; opt -full; opt_clean; dfflibmap -liberty $LIB; abc -liberty $LIB; clean; opt -full; abc -liberty $LIB; ltp; stat"
