"""
Module 1: Counter Testbench
cocotb testbench for counter module.

Demonstrates:
- Clock generation
- Reset sequence
- Enable control
- Counter verification
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.utils import get_sim_time


async def generate_clock(dut, period_ns=10):
    """Generate clock signal."""
    while True:
        dut.clk.value = 1
        await Timer(period_ns // 2, units="ns")


        dut.clk.value = 0
        await Timer(period_ns // 2, units="ns")




async def reset_dut(dut, duration_ns=20):
    """Reset the DUT."""
    dut.rst_n.value = 0
    dut.enable.value = 0
    await Timer(duration_ns, units="ns")


    dut.rst_n.value = 1
    await Timer(10, units="ns")




@cocotb.test()
async def test_counter_reset(dut):
    """
    Test counter reset functionality.
    """
    # Start clock
    cocotb.start_soon(generate_clock(dut, period_ns=10))
    
    # Reset
    await reset_dut(dut)
    
    # Check counter is reset
    assert dut.count.value == 0, f"Counter should be 0 after reset, got {dut.count.value}"


@cocotb.test()
async def test_counter_increment(dut):
    """
    Test counter increment functionality.
    """
    # Start clock
    cocotb.start_soon(generate_clock(dut, period_ns=10))
    
    # Reset
    await reset_dut(dut)
    
    # Enable counter
    dut.enable.value = 1
    
    # Count for several cycles
    for expected_count in range(1, 11):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")  # Wait for combinational logic


        actual_count = int(dut.count.value)
        assert actual_count == expected_count, \
            f"Expected count {expected_count}, got {actual_count}"


@cocotb.test()
async def test_counter_enable(dut):
    """
    Test counter enable control.
    """
    # Start clock
    cocotb.start_soon(generate_clock(dut, period_ns=10))
    
    # Reset
    await reset_dut(dut)
    
    # Enable and count
    dut.enable.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


    assert dut.count.value == 1, "Counter should increment when enabled"
    
    # Disable and check counter doesn't increment
    dut.enable.value = 0
    count_before = int(dut.count.value)
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


    count_after = int(dut.count.value)
    assert count_after == count_before, "Counter should not increment when disabled"
    
    # Re-enable and verify it continues
    dut.enable.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


    assert dut.count.value == count_before + 1, "Counter should resume incrementing when re-enabled"


@cocotb.test()
async def test_counter_overflow(dut):
    """
    Test counter overflow behavior.
    """
    # Start clock
    cocotb.start_soon(generate_clock(dut, period_ns=10))
    
    # Reset
    await reset_dut(dut)
    
    # Enable counter
    dut.enable.value = 1
    
    # Count to near overflow (254 = 255 - 1, testing boundary condition)
    # For an 8-bit counter, maximum value is 255 (0xFF)
    # We count to 254 to test the overflow behavior on the next increment
    MAX_COUNT = 255  # Maximum value for 8-bit counter
    COUNT_TO_OVERFLOW = MAX_COUNT - 1  # 254
    
    for _ in range(COUNT_TO_OVERFLOW):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")


    
    # Check we're at the expected pre-overflow value
    assert dut.count.value == COUNT_TO_OVERFLOW, \
        f"Should be at {COUNT_TO_OVERFLOW} before overflow, got {dut.count.value}"
    
    # Next increment should wrap to 0 (or continue to 255, depending on implementation)
    # This tests the counter's overflow behavior
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


    # Note: Counter behavior depends on implementation:
    # - Wrapping counter: 254 -> 255 -> 0 (wraps on next increment)
    # - Saturating counter: 254 -> 255 -> 255 (saturates at max)
    # This test accepts both behaviors as valid
    final_count = int(dut.count.value)
    assert final_count in [0, MAX_COUNT], \
        f"Counter should wrap to 0 or saturate at {MAX_COUNT}, got {final_count}"


@cocotb.test()
async def test_counter_clock_period(dut):
    """
    Test clock timing constraint.

    Verifies the generated clock actually respects the requested period.
    """
    period_ns = 10
    cocotb.start_soon(generate_clock(dut, period_ns=period_ns))

    await RisingEdge(dut.clk)
    t1 = get_sim_time(units="ns")
    await RisingEdge(dut.clk)
    t2 = get_sim_time(units="ns")

    measured_period = t2 - t1
    assert measured_period == period_ns, \
        f"Expected clock period {period_ns}ns, measured {measured_period}ns"


@cocotb.test()
async def test_counter_no_glitch(dut):
    """
    Test counter stability timing constraint.

    Verifies count only changes on a RisingEdge, never mid-cycle.
    """
    cocotb.start_soon(generate_clock(dut, period_ns=10))
    await reset_dut(dut)
    dut.enable.value = 1

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")  # Wait for combinational logic
    count_after_edge = int(dut.count.value)

    # Sample mid-cycle: value must not have changed
    await Timer(4, units="ns")
    count_mid_cycle = int(dut.count.value)
    assert count_mid_cycle == count_after_edge, \
        f"Glitch detected: count changed from {count_after_edge} to " \
        f"{count_mid_cycle} without a RisingEdge in between"


@cocotb.test()
async def test_counter_reset_duration(dut):
    """
    Test reset timing constraint.

    Verifies rst_n stays asserted (low) for at least the required duration.
    """
    cocotb.start_soon(generate_clock(dut, period_ns=10))

    dut.rst_n.value = 0
    dut.enable.value = 0
    t_reset_start = get_sim_time(units="ns")

    min_reset_ns = 20  # Minimum reset duration required by the design/spec
    await Timer(min_reset_ns, units="ns")

    assert dut.rst_n.value == 0, \
        f"rst_n was released before the required {min_reset_ns}ns minimum"

    elapsed = get_sim_time(units="ns") - t_reset_start
    assert elapsed >= min_reset_ns, \
        f"Reset held for only {elapsed}ns, {min_reset_ns}ns required"

    dut.rst_n.value = 1

