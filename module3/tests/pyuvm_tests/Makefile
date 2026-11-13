# Makefile for Module 3 pyuvm tests
# Usage: make TEST=test_simple_uvm     (VHDL on GHDL)  |  make WAVES=1  |  make SIM=verilator
# See common.mk at the repository root for all options.

# Test to run (Python module name)
TEST ?= test_simple_uvm

MODULE   = $(TEST)
TOPLEVEL = adder
DUT_DIR  = ../../dut/simple_blocks
WAVES    = 1
include ../../../common.mk
