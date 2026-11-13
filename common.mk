# common.mk - shared cocotb/pyuvm build rules for every example and test.
#
# A per-directory Makefile only declares WHAT to run and includes this file:
#
#     MODULE   = configdb_example          # Python module with the tests
#     TOPLEVEL = adder                     # entity / module name of the DUT
#     DUT_DIR  = ../../dut/simple_blocks   # directory with <TOPLEVEL>.vhd / .v
#     include ../../../common.mk
#
# Usage:
#     make                  # VHDL DUT on GHDL (default)
#     make WAVES=1          # also dump a waveform (<TOPLEVEL>.vcd on GHDL)
#     make SIM=nvc          # VHDL DUT on NVC
#     make SIM=verilator    # legacy Verilog DUT (<TOPLEVEL>.v) on Verilator
#     make SIM=icarus       # legacy Verilog DUT on Icarus Verilog
#     make clean
#
# Optional knobs (set in the Makefile or on the command line):
#     WAVES=1      dump waveforms
#     HDL_COVERAGE=1   HDL code coverage (only wired up for Verilator)
#                      (not called COVERAGE: cocotb uses that for Python coverage)
#     TESTCASE=... run a single cocotb test (see README, cocotb 1.9.x naming)

SIM      ?= ghdl
WAVES    ?= 0
HDL_COVERAGE ?= 0

ifeq ($(strip $(TOPLEVEL)),)
$(error TOPLEVEL is not set: define it before including common.mk)
endif
ifeq ($(strip $(MODULE)),)
$(error MODULE is not set: define it before including common.mk)
endif

# cocotb 2.x renamed MODULE to COCOTB_TEST_MODULES; keep both in sync so the
# same Makefile works with cocotb 1.9.x (pinned in pyproject.toml) and 2.x.
COCOTB_TEST_MODULES ?= $(MODULE)
export COCOTB_REDUCED_LOG_FMT ?= 1

ifneq ($(filter $(SIM),ghdl nvc),)
# ------------------------------------------------------------------ VHDL ---
TOPLEVEL_LANG   := vhdl
VHDL_SOURCES    ?= $(DUT_DIR)/$(TOPLEVEL).vhd
# cocotb's GHDL flow refuses to run if VERILOG_SOURCES is not empty.
VERILOG_SOURCES :=

ifeq ($(SIM),ghdl)
GHDL_ARGS += --std=08
ifeq ($(WAVES),1)
SIM_ARGS += --vcd=$(TOPLEVEL).vcd
endif
endif

ifeq ($(HDL_COVERAGE),1)
$(warning HDL_COVERAGE=1 is only implemented for SIM=verilator; ignored for $(SIM))
endif

else
# --------------------------------------------------- Verilog (legacy) ------
TOPLEVEL_LANG   := verilog
VERILOG_SOURCES ?= $(DUT_DIR)/$(TOPLEVEL).v
VHDL_SOURCES    :=

ifeq ($(SIM),verilator)
ifeq ($(WAVES),1)
EXTRA_ARGS += --trace --trace-structs
endif
ifeq ($(HDL_COVERAGE),1)
COMPILE_ARGS += --coverage --coverage-line --coverage-toggle
endif
endif

endif

include $(shell cocotb-config --makefiles)/Makefile.sim

clean::
	$(RM) -r __pycache__ results.xml *.vcd *.fst *.ghw
# GHDL with the LLVM/GCC backend leaves the elaborated binary next to the test
	$(RM) $(TOPLEVEL) e~$(TOPLEVEL).o
