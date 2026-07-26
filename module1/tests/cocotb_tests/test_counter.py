"""
Module 1: Counter Testbench
cocotb testbench for counter module.

Demonstrates:
- Clock generation
- Reset sequence
- Enable control
- Counter verification
"""

from collections import Counter
from typing import Any, Dict

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.utils import get_sim_time


class CoverageCollector:
    """
    Coverage data collector.

    Same pattern as module1/examples/data_structures/data_structures_example.py,
    reused here directly against the counter DUT instead of random values.
    """

    def __init__(self) -> None:
        self.covered_bins: Dict[str, set] = {}
        self.hit_counts: Dict[str, Counter] = {}
        self.total_possible: Dict[str, int] = {}

    def define_bin(self, bin_name: str, total_possible_values: int) -> None:
        self.covered_bins.setdefault(bin_name, set())
        self.hit_counts.setdefault(bin_name, Counter())
        self.total_possible[bin_name] = total_possible_values

    def add_coverage(self, bin_name: str, value: Any) -> None:
        self.covered_bins.setdefault(bin_name, set())
        self.hit_counts.setdefault(bin_name, Counter())
        self.covered_bins[bin_name].add(value)
        self.hit_counts[bin_name][value] += 1

    def get_coverage(self, bin_name: str) -> float:
        if bin_name not in self.covered_bins:
            return 0.0
        total = self.total_possible[bin_name]
        if total == 0:
            return 0.0
        return (len(self.covered_bins[bin_name]) / total) * 100.0


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
    assert dut.count.value == 0, (
        f"Counter should be 0 after reset, got {dut.count.value}"
    )


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
        assert actual_count == expected_count, (
            f"Expected count {expected_count}, got {actual_count}"
        )


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

    assert dut.count.value == count_before + 1, (
        "Counter should resume incrementing when re-enabled"
    )


@cocotb.test()
async def test_counter_overflow(dut):
    """
    Test counter overflow behavior.

    Drives a full 256-cycle wrap (0x00 -> 0xFF -> 0x00) and tracks
    functional coverage of the overflow event itself, since checking only
    the final value (0 or 255) can pass without the wrap ever occurring.
    """
    coverage = CoverageCollector()
    coverage.define_bin("overflow_event", total_possible_values=1)

    # Start clock
    cocotb.start_soon(generate_clock(dut, period_ns=10))

    # Reset
    await reset_dut(dut)

    # Enable counter
    dut.enable.value = 1

    MAX_COUNT = 255  # Maximum value for 8-bit counter

    prev_count = int(dut.count.value)  # 0 right after reset

    # A genuine wrap requires 256 increments from 0 (0 -> 1 -> ... -> 255 -> 0).
    for _ in range(MAX_COUNT + 1):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")

        new_count = int(dut.count.value)
        if prev_count == MAX_COUNT and new_count == 0:
            coverage.add_coverage("overflow_event", "wrap_0xFF_to_0x00")
        prev_count = new_count

    final_count = int(dut.count.value)
    assert final_count == 0, (
        f"Counter should wrap to 0 after 256 cycles, got {final_count}"
    )

    cov_pct = coverage.get_coverage("overflow_event")
    dut._log.info(f"Overflow coverage: {cov_pct:.1f}%")
    assert cov_pct == 100.0, "The 0xFF -> 0x00 wrap was never observed"


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
    assert measured_period == period_ns, (
        f"Expected clock period {period_ns}ns, measured {measured_period}ns"
    )


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
    assert count_mid_cycle == count_after_edge, (
        f"Glitch detected: count changed from {count_after_edge} to "
        f"{count_mid_cycle} without a RisingEdge in between"
    )


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

    assert dut.rst_n.value == 0, (
        f"rst_n was released before the required {min_reset_ns}ns minimum"
    )

    elapsed = get_sim_time(units="ns") - t_reset_start
    assert elapsed >= min_reset_ns, (
        f"Reset held for only {elapsed}ns, {min_reset_ns}ns required"
    )

    dut.rst_n.value = 1
