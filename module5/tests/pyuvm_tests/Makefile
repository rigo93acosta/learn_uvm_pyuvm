# Makefile for Module 5 pyuvm tests
# Usage: make TEST=test_advanced_uvm     (VHDL on GHDL)  |  make WAVES=1  |  make SIM=verilator
# See common.mk at the repository root for all options.

# Test to run (Python module name)
TEST ?= test_advanced_uvm

MODULE   = $(TEST)
TOPLEVEL = multi_channel
DUT_DIR  = ../../dut/advanced
WAVES    = 1
include ../../../common.mk
