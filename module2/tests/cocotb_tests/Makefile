# Makefile for Module 2 cocotb tests
# Usage: make TEST=test_simple_register | test_shift_register | test_simple_fsm
#        make test_all
#        (VHDL on GHDL by default; add SIM=verilator for the legacy Verilog DUT)
# See common.mk at the repository root for all options.

# Test to run (Python module name). The DUT is the test name without "test_".
TEST ?= test_simple_register

MODULE   = $(TEST)
TOPLEVEL = $(patsubst test_%,%,$(TEST))
WAVES    = 1

# DUT directory - selected by test
ifeq ($(TEST),test_simple_fsm)
DUT_DIR = ../../dut/state_machines
else ifeq ($(TEST),test_simple_fifo)
DUT_DIR = ../../dut/fifos
else
DUT_DIR = ../../dut/registers
endif

# HDL code coverage is a Verilator feature: make SIM=verilator HDL_COVERAGE=1

include ../../../common.mk

# Helper targets
.PHONY: test_all
test_all:
	$(MAKE) clean
	$(MAKE) TEST=test_simple_register
	$(MAKE) clean
	$(MAKE) TEST=test_shift_register
	$(MAKE) clean
	$(MAKE) TEST=test_simple_fsm
