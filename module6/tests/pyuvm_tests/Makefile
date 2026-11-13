# Makefile for Module 6 pyuvm tests
# Usage: make TEST=test_complex_testbench     (VHDL on GHDL)  |  make WAVES=1  |  make SIM=verilator
# See common.mk at the repository root for all options.

# Test to run (Python module name)
TEST ?= test_complex_testbench

MODULE   = $(TEST)
TOPLEVEL = axi4_lite_slave
DUT_DIR  = ../../dut/protocols

include ../../../common.mk
