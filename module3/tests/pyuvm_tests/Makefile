# Makefile for Module 3 pyuvm tests
# Usage: make SIM=verilator test_simple_uvm

# Default simulator is chosen based on available sources unless overridden
# If the user sets SIM on the command line (e.g. `make SIM=ghdl`), it is respected.

# Python files
PYTHON_FILES = test_simple_uvm.py

# Verilog files
VERILOG_SOURCES = ../../dut/simple_blocks/adder.v
VERILOG_FILES = $(VERILOG_SOURCES)

# VHDL files
VHDL_SOURCES = ../../dut/simple_blocks/adder.vhd
VHDL_FILES = $(VHDL_SOURCES)

# Choose default SIM if not provided: prefer Verilator when Verilog exists,
# otherwise use GHDL if VHDL exists. User-provided `SIM=` overrides this.
ifeq ($(origin SIM), undefined)
ifneq ($(strip $(VERILOG_SOURCES)),)
	SIM := verilator
else
ifneq ($(strip $(VHDL_SOURCES)),)
	SIM := ghdl
else
	SIM := verilator
endif
endif
endif

# Test to run
TEST ?= test_simple_uvm

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = adder
COCOTB_REDUCED_LOG_FMT = 1
WAVES = 1
# COMPILE_ARGS += --coverage --coverage-line --coverage-toggle

# If using Verilator, enable tracing at runtime and enable FST only when zlib is available
ifeq ($(SIM),verilator)
TOPLEVEL_LANG = verilog
VERILATOR_TRACE = 1
COMPILE_ARGS += --trace-fst
	# When using Verilator, ignore VHDL files
	VHDL_FILES :=
	VHDL_SOURCES :=
endif

# If using GHDL, set top-level language for cocotb
ifeq ($(SIM),ghdl)
TOPLEVEL_LANG = vhdl
	# When using GHDL, ignore Verilog files
	VERILOG_FILES :=
	VERILOG_SOURCES :=
endif

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

