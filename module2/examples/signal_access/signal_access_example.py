"""
Module 2 Example 2.1: Basic Signal Access
Demonstrates accessing and reading DUT signals in cocotb.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge


@cocotb.test()
async def test_signal_access_basic(dut):
    """
    Basic signal access example.
    
    Demonstrates:
    - Accessing DUT signals
    - Reading signal values
    - Different signal types
    """
    # Start clock
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    # Initialize signals
    dut.rst_n.value = 0
    dut.enable.value = 0
    dut.d.value = 0
    
    # Wait for initial values
    await Timer(10, unit="ns")
    
    # Read initial values
    cocotb.log.info(f"Initial q value: {dut.q.value.to_unsigned()}")
    cocotb.log.info(f"Initial q value (integer): {dut.q.value.to_unsigned()}")
    cocotb.log.info(f"Initial q value (binary): {dut.q.value}")
    cocotb.log.info(f"Width of q signal: {len(dut.q)} bits") # Accessing signal width
    
    # Deassert reset
    dut.rst_n.value = 1
    await Timer(10, unit="ns")
    
    # Read after reset
    cocotb.log.info(f"After reset q value: {dut.q.value.to_unsigned()}")
    
    # Enable and write data
    dut.enable.value = 1
    dut.d.value = 0xAB
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    # Read output
    cocotb.log.info(f"After write q value: 0x{dut.q.value.to_unsigned():02X}")
    assert dut.q.value.to_unsigned() == 0xAB, f"Expected 0xAB, got 0x{dut.q.value.to_unsigned():02X}"


@cocotb.test()
async def test_signal_types(dut):
    """
    Demonstrates different signal types.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    dut.enable.value = 1
    
    # Test single-bit signal
    cocotb.log.info(f"enable signal type: {type(dut.enable.value)}")
    cocotb.log.info(f"enable value: {int(dut.enable.value)}")
    
    # Test multi-bit signal
    cocotb.log.info(f"d signal width: {len(dut.d)}")
    cocotb.log.info(f"q signal width: {len(dut.q)}")
    
    # Test different value assignments
    dut.d.value = 0x12  # Integer
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    cocotb.log.info(f"Assigned 0x12, got: 0x{dut.q.value.to_unsigned():02X}")
    
    dut.d.value = 0b10101010  # Binary literal
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    cocotb.log.info(f"Assigned 0b10101010, got: 0x{dut.q.value.to_unsigned():02X}")
    assert dut.q.value.to_unsigned() == 0xAA


@cocotb.test()
async def test_signal_properties(dut):
    """
    Demonstrates signal properties and methods.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    dut.enable.value = 1
    
    # Test signal properties
    cocotb.log.info(f"Signal name: {dut.q._name}")
    cocotb.log.info(f"Signal path: {dut.q._path}")
    cocotb.log.info(f"Signal width: {len(dut.q)}")
    
    # Test value representations
    dut.d.value = 0x5A
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    cocotb.log.info(f"Integer: {dut.q.value.to_unsigned()}")
    cocotb.log.info(f"Binary: {dut.q.value}")
    cocotb.log.info(f"Hex: {hex(dut.q.value.to_unsigned())}")
    cocotb.log.info(f"String: {str(dut.q.value.to_unsigned())}")

