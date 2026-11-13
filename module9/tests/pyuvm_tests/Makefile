# Makefile for Module 9 pyuvm tests (reactive ARQ over a lossy channel)
# Usage: make            (VHDL on GHDL)   |  make WAVES=1
# This module is VHDL only: there is no lossy_channel.v for SIM=verilator.
# See common.mk at the repository root for all options.

# Test to run (Python module name)
TEST ?= test_reactive_arq

MODULE   = $(TEST)
TOPLEVEL = lossy_channel
DUT_DIR  = ../../dut/channel

include ../../../common.mk
