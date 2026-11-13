# Makefile for Module 1 pyuvm tests
# Usage: make TEST=test_and_gate_uvm     (VHDL on GHDL)  |  make WAVES=1  |  make SIM=verilator
# See common.mk at the repository root for all options.

# Test to run (Python module name)
TEST ?= test_and_gate_uvm

MODULE   = $(TEST)
TOPLEVEL = and_gate
DUT_DIR  = ../../dut/simple_gates

# HDL code coverage is a Verilator feature: make SIM=verilator HDL_COVERAGE=1
include ../../../common.mk
