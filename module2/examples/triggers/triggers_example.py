"""
Module 2 Example 2.4: Trigger Usage
Demonstrates various triggers in cocotb.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import (
    Timer, RisingEdge, FallingEdge, Edge,
    ReadOnly, ReadWrite, Combine, First, Lock,
    SimTimeoutError
)

@cocotb.test()
async def test_edge_triggers(dut):
    """
    Demonstrates edge triggers.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    
    # Rising edge trigger
    cocotb.log.info("Waiting for rising edge...")
    # await RisingEdge(dut.clk) # Obsolete, use value_change instead
    await dut.clk.rising_edge
    cocotb.log.info("Rising edge detected")
    
    # Falling edge trigger
    cocotb.log.info("Waiting for falling edge...")
    # await FallingEdge(dut.clk) # Obsolete, use value_change instead
    await dut.clk.falling_edge
    cocotb.log.info("Falling edge detected")
    
    # Any edge trigger
    cocotb.log.info("Waiting for any edge...")
    # await Edge(dut.clk) # Obsolete, use value_change instead
    await dut.clk.value_change
    cocotb.log.info("Edge detected")


@cocotb.test()
async def test_timer_trigger(dut):
    """
    Demonstrates timer triggers.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    # Wait for specific time
    cocotb.log.info("Waiting 50ns...")
    await Timer(50, unit="ns")
    cocotb.log.info("50ns elapsed")
    
    # Wait for multiple time periods
    for delay in [10, 20, 30]:
        await Timer(delay, unit="ns")
        cocotb.log.info(f"Waited {delay}ns")


@cocotb.test()
async def test_readonly_trigger(dut):
    """
    Demonstrates ReadOnly trigger (end of time step).
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    dut.enable.value = 1
    dut.d.value = 0xAA
    
    # Drive signal
    await dut.clk.rising_edge
    
    # Wait for ReadOnly (end of time step)
    await ReadOnly()
    
    # Now signal should be stable
    cocotb.log.info(f"Signal value after ReadOnly: 0x{dut.q.value.to_unsigned():02X}")


@cocotb.test()
async def test_combine_trigger(dut):
    """
    Demonstrates combining multiple triggers.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    
    # Wait for clock edge AND timer
    cocotb.log.info("Waiting for clock edge and timer...")
    await Combine(dut.clk.rising_edge, Timer(5, unit="ns"))
    cocotb.log.info("Both conditions met")


@cocotb.test()
async def test_first_trigger(dut):
    """
    Demonstrates First trigger (first to occur).
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    
    # Wait for first of multiple triggers
    cocotb.log.info("Waiting for first trigger...")
    try:
        await First(
            dut.clk.rising_edge,
            Timer(100, unit="ns")
        )
        cocotb.log.info("Clock edge occurred first")
    except SimTimeoutError:
        cocotb.log.info("Timer would occur first")


@cocotb.test()
async def test_timeout_handling(dut):
    """
    Demonstrates timeout handling with triggers.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    # Wait with timeout
    try:
        await Timer(1000, unit="ns")
        cocotb.log.info("Operation completed")
    except SimTimeoutError:
        cocotb.log.info("Operation timed out")


@cocotb.test()
async def test_parallel_triggers(dut):
    """
    Demonstrates parallel coroutines with triggers.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    async def monitor_clock():
        for i in range(5):
            await dut.clk.rising_edge
            cocotb.log.info(f"Monitor: Clock cycle {i+1}")
    
    async def monitor_timer():
        for i in range(3):
            await Timer(20, unit="ns")
            cocotb.log.info(f"Monitor: Timer {i+1}")
    
    # Run both in parallel
    await cocotb.start_soon(monitor_clock())
    await cocotb.start_soon(monitor_timer())
    
    # Wait for completion
    await Timer(100, unit="ns")

