# Makefile for Module 4 pyuvm tests
# Usage: make TEST=test_complete_agent     (VHDL on GHDL)  |  make WAVES=1  |  make SIM=verilator
# See common.mk at the repository root for all options.

# Test to run (Python module name)
TEST ?= test_complete_agent

MODULE   = $(TEST)
TOPLEVEL = simple_interface
DUT_DIR  = ../../dut/interfaces
WAVES    = 1
include ../../../common.mk
