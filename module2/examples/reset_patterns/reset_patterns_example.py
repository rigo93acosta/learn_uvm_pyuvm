"""
Module 2 Example 2.5: Reset Patterns
Demonstrates reset sequence implementation.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge


async def async_reset(dut, duration_ns=100, propagation_delay_ns=10):
    """
    Asynchronous reset sequence.
    
    Args:
        dut: Device under test
        duration_ns: Reset duration in nanoseconds
        propagation_delay_ns: Delay after deasserting reset to allow
                              signal propagation and DUT stabilization
    """
    cocotb.log.info("Asserting async reset...")
    dut.rst_n.value = 0
    await Timer(duration_ns, unit="ns")
    
    cocotb.log.info("Deasserting async reset...")
    dut.rst_n.value = 1
    # Wait for reset signal to propagate through DUT logic
    # This ensures all flip-flops have stabilized before continuing
    await Timer(propagation_delay_ns, unit="ns")
    cocotb.log.info("Reset complete")


async def sync_reset(dut, clock_period_ns=10, reset_cycles=5):
    """
    Synchronous reset sequence.
    
    Args:
        dut: Device under test
        clock_period_ns: Clock period in nanoseconds
        reset_cycles: Number of clock cycles to hold reset
    """
    cocotb.log.info("Asserting sync reset...")
    dut.rst_n.value = 0
    
    # Hold reset for specified cycles
    for i in range(reset_cycles):
        await dut.clk.rising_edge
        cocotb.log.info(f"  Reset cycle {i+1}/{reset_cycles}")
    
    cocotb.log.info("Deasserting sync reset...")
    dut.rst_n.value = 1
    await dut.clk.rising_edge
    await Timer(1, unit="ns")  # Wait for reset to propagate
    cocotb.log.info("Reset complete")


@cocotb.test()
async def test_async_reset(dut):
    """
    Test asynchronous reset.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    # Initialize
    dut.enable.value = 0
    dut.d.value = 0
    
    # Apply async reset with default propagation delay
    await async_reset(dut, duration_ns=50)
    
    # Verify reset state
    assert dut.q.value.to_unsigned() == 0, "Register should be reset to 0"
    cocotb.log.info("[OK]: Async reset verified")


@cocotb.test()
async def test_sync_reset(dut):
    """
    Test synchronous reset pattern.
    
    Note: This DUT has async reset, so this test demonstrates
    the sync reset pattern but verifies async reset behavior.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    # Initialize
    dut.enable.value = 1
    dut.d.value = 0xFF
    
    # Write some data
    await dut.clk.rising_edge
    await Timer(1, unit="ns")
    cocotb.log.info(f"Before reset: q = 0x{dut.q.value.to_unsigned():02X}")
    
    # Apply sync reset pattern (but DUT has async reset, so it resets immediately)
    dut.rst_n.value = 0
    await Timer(1, unit="ns")  # Wait for async reset to take effect
    assert dut.q.value.to_unsigned() == 0, "Register should be reset immediately (async reset)"
    
    # Hold reset for a few cycles (demonstrating sync reset pattern)
    for i in range(3):
        await dut.clk.rising_edge
        cocotb.log.info(f"  Reset cycle {i+1}/3")
        assert dut.q.value.to_unsigned() == 0, "Register should stay reset"
    
    # Disable enable and clear data before deasserting reset
    dut.enable.value = 0
    dut.d.value = 0
    
    cocotb.log.info("Deasserting sync reset...")
    dut.rst_n.value = 1
    await dut.clk.rising_edge
    await Timer(1, unit="ns")
    
    # Verify reset state (should stay 0 since enable is 0)
    assert dut.q.value.to_unsigned() == 0, "Register should stay at 0 after reset"
    cocotb.log.info("[OK] Sync reset pattern verified (with async reset DUT)")


@cocotb.test()
async def test_reset_verification(dut):
    """
    Comprehensive reset verification.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    # Test 1: Reset during operation
    dut.enable.value = 1
    dut.d.value = 0xAA
    await dut.clk.rising_edge
    await Timer(1, unit="ns")
    
    cocotb.log.info("Applying reset during operation...")
    dut.rst_n.value = 0
    await dut.clk.rising_edge
    await Timer(1, unit="ns")
    
    assert dut.q.value.to_unsigned() == 0, "Should reset even during operation"
    cocotb.log.info("[OK] Reset during operation verified")
    
    # Test 2: Reset release timing
    dut.rst_n.value = 1
    await dut.clk.rising_edge
    await Timer(1, unit="ns")
    
    # Write new data after reset
    dut.d.value = 0x55
    await dut.clk.rising_edge
    await Timer(1, unit="ns")
    
    assert dut.q.value.to_unsigned() == 0x55, "Should accept new data after reset"
    cocotb.log.info("[OK] Reset release timing verified")


@cocotb.test()
async def test_reset_initialization(dut):
    """
    Test initialization after reset.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    # Apply reset with default propagation delay
    await async_reset(dut, duration_ns=50)
    
    # Initialize signals
    dut.enable.value = 1
    dut.d.value = 0x12
    
    # Wait for clock edge
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    # Verify initialization
    assert dut.q.value.integer == 0x12, "Should accept data after reset"
    cocotb.log.info("✓ Initialization after reset verified")

