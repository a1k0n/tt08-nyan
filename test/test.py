# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 39, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # the first scanline on the first frame will have some uninitialized data
    # (since necessary regs for rendering are computed during the hsync of the
    # previous scanline); skip it
    await ClockCycles(dut.clk, 640+48+16+96)

    # hsync and vsync should be de-asserted (high)
    assert dut.uo_out[3].value == 1
    assert dut.uo_out[7].value == 1

    # hsync should go low after the front porch
    await ClockCycles(dut.clk, 640+16+2)
    assert dut.uo_out[7].value == 0

    # and high again
    await ClockCycles(dut.clk, 96)
    assert dut.uo_out[7].value == 1
