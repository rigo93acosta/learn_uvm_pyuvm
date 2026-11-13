# Makefile for the protocol examples (i2c, spi, uart)
# Usage: make MODULE=uart_example | make MODULE=spi_example | make MODULE=i2c_example
#        (VHDL on GHDL by default; add SIM=verilator for the legacy Verilog DUT)
# See common.mk at the repository root for all options.

# Example to run
MODULE ?= i2c_example

# Only the UART has a real DUT. The SPI and I2C examples do not drive any
# signal yet, so they run on top of simple_dma just to have a simulator
# (see docs/ROADMAP_es.md, Module 7).
ifeq ($(MODULE),uart_example)
TOPLEVEL = uart
DUT_DIR  = ../../dut/protocols
else
TOPLEVEL = simple_dma
DUT_DIR  = ../../dut/dma
endif

include ../../../common.mk
