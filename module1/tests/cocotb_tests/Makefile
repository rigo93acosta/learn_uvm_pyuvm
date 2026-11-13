# Makefile for Module 1 cocotb tests
# Usage: make TEST=test_and_gate | make TEST=test_counter | make test_all
#        (VHDL on GHDL by default; add SIM=verilator for the legacy Verilog DUT)
# See common.mk at the repository root for all options.

# Test to run (Python module name). The DUT is the test name without "test_".
TEST ?= test_and_gate

MODULE   = $(TEST)
TOPLEVEL = $(patsubst test_%,%,$(TEST))
DUT_DIR  = ../../dut/simple_gates

include ../../../common.mk

# Helper targets
.PHONY: test_all
test_all:
	$(MAKE) clean
	$(MAKE) TEST=test_and_gate
	$(MAKE) clean
	$(MAKE) TEST=test_counter
