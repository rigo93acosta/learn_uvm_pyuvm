"""
Module 1 Test Case 1.3: Simple Verification Test
cocotb testbench for AND gate.

Demonstrates:
- Testbench structure
- Clock generation
- Signal driving
- Basic checking
"""

from collections import Counter
from typing import Any, Dict

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge


class CoverageCollector:
    """
    Coverage data collector.

    Same pattern as module1/examples/data_structures/data_structures_example.py,
    reused here directly against the AND gate DUT instead of random values.
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


@cocotb.test()
async def test_and_gate_basic(dut):
    """
    Basic AND gate test.
    
    Tests all input combinations.
    """
    # Initialize inputs
    dut.a.value = 0
    dut.b.value = 0
    
    # Wait for initial values to settle
    await Timer(10, unitss="ns")
    
    # Test case 1: 0 & 0 = 0
    dut.a.value = 0
    dut.b.value = 0
    await Timer(10, unitss="ns")
    assert dut.y.value == 0, f"Expected 0, got {dut.y.value}"
    
    # Test case 2: 0 & 1 = 0
    dut.a.value = 0
    dut.b.value = 1
    await Timer(10, unitss="ns")
    assert dut.y.value == 0, f"Expected 0, got {dut.y.value}"
    
    # Test case 3: 1 & 0 = 0
    dut.a.value = 1
    dut.b.value = 0
    await Timer(10, unitss="ns")
    assert dut.y.value == 0, f"Expected 0, got {dut.y.value}"
    
    # Test case 4: 1 & 1 = 1
    dut.a.value = 1
    dut.b.value = 1
    await Timer(10, unitss="ns")
    assert dut.y.value == 1, f"Expected 1, got {dut.y.value}"


@cocotb.test()
async def test_and_gate_truth_table(dut):
    """
    AND gate truth table test.

    Tests all combinations systematically and tracks functional coverage
    of the input space to guarantee the truth table is fully exercised.
    """
    coverage = CoverageCollector()
    coverage.define_bin("input_combo", total_possible_values=4)  # (a,b): 00,01,10,11

    test_cases = [
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0),
        (1, 1, 1),
    ]

    for a_val, b_val, expected_y in test_cases:
        dut.a.value = a_val
        dut.b.value = b_val
        await Timer(10, unitss="ns")

        actual_y = int(dut.y.value)
        assert actual_y == expected_y, \
            f"Input (a={a_val}, b={b_val}): Expected {expected_y}, got {actual_y}"

        coverage.add_coverage("input_combo", (a_val, b_val))

    cov_pct = coverage.get_coverage("input_combo")
    dut._log.info(f"Truth table coverage: {cov_pct:.1f}%")
    assert cov_pct == 100.0, f"Truth table not fully covered: {cov_pct:.1f}%"


@cocotb.test()
async def test_and_gate_timing(dut):
    """
    AND gate timing test.
    
    Tests signal propagation timing.
    """
    # Set initial values
    dut.a.value = 0
    dut.b.value = 0
    await Timer(5, unitss="ns")
    
    # Change both inputs simultaneously
    dut.a.value = 1
    dut.b.value = 1
    await Timer(5, unitss="ns")
    
    # Output should be stable
    assert dut.y.value == 1, "Output should be 1 after both inputs are 1"
    
    # Change one input
    dut.a.value = 0
    await Timer(5, unitss="ns")
    assert dut.y.value == 0, "Output should be 0 when one input is 0"

