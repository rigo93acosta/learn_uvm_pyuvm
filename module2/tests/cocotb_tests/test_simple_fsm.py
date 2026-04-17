import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
from enum import IntEnum
import logging

class FsmState(IntEnum):
    IDLE = 0
    START = 1
    WORK = 2
    DONE = 3

# Replace cocotb.logging with standard Python logging
class FSMMonitor:
    def __init__(self, dut):
        self.dut = dut
        self.log = logging.getLogger("cocotb.monitor")
        logging.basicConfig(level=logging.INFO)

    async def start_monitoring(self):
        """Observes state changes and outputs on each cycle."""
        while True:
            await self.dut.clk.rising_edge
            # Wait a small time for signals to stabilize
            await Timer(1, unit="ns") 
            
            current_state = FsmState(self.dut.state.value)
            is_done = self.dut.done.value
            
            # The monitor only reports, it does not assert
            self.log.info(f"[MON] State: {current_state.name} | Done: {is_done}")

async def reset_dut(dut, duration: int = 10):
    """Reset the DUT."""
    dut.start.value = 0
    dut.rst_n.value = 0
    await Timer(duration, unit="ns")
    dut.rst_n.value = 1
    await Timer(duration, unit="ns")

@cocotb.test()
async def test_fsm_reset(dut):
    """Test FSM reset functionality."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    await reset_dut(dut)
    
    state = FsmState
    # Verify initial state after reset
    assert dut.state.value == state.IDLE, f"FSM should be in IDLE state after reset, got {dut.state.value}"

@cocotb.test()
async def test_fsm_idle_and_outputs(dut):
    """
    Verify that the FSM remains in IDLE 
    and 'done' is 0 without stimulus.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)
    
    for _ in range(5):
        await dut.clk.rising_edge
        assert dut.state.value == FsmState.IDLE
        assert dut.done.value == 0, "Error: 'done' must be 0 in IDLE"

@cocotb.test()
async def test_fsm_sequence_logic(dut):
    """
    Verify the sequence IDLE -> START -> WORK -> DONE -> IDLE.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    # Trigger FSM
    dut.start.value = 1
    await dut.clk.rising_edge
    await Timer(1, "ns")
    assert dut.state.value == FsmState.START
    assert dut.done.value == 0

    dut.start.value = 0
    await dut.clk.rising_edge
    await Timer(1, "ns")
    assert dut.state.value == FsmState.WORK
    assert dut.done.value == 0

    await dut.clk.rising_edge
    await Timer(1, "ns")
    assert dut.state.value == FsmState.DONE
    

    await dut.clk.rising_edge
    await Timer(1, "ns")
    assert dut.state.value == FsmState.IDLE
    assert dut.done.value == 1, "Error: 'done' must be 1 in the DONE state"
    
    await Timer(10, "ns")

@cocotb.test()
async def test_fsm_reset_recovery(dut):
    """
    Verify that a reset during operation returns the FSM to IDLE.
    """

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)
    state = FsmState
    # Reach the WORK state
    dut.start.value = 1
    await dut.clk.rising_edge # To START
    await dut.clk.rising_edge # To WORK
    dut.start.value = 0
    
    # Apply unexpected reset
    await reset_dut(dut, duration=5)
    assert dut.state.value == state.IDLE, "The FSM did not return to IDLE after reset"
    assert dut.done.value == 0, "The 'done' signal remained stuck after reset"


@cocotb.test()
async def test_fsm_monitor(dut):
    """
    Test with monitor to observe the sequence of states and outputs.
    This test does not assert, it only shows the monitor information.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    monitor = FSMMonitor(dut)
    cocotb.start_soon(monitor.start_monitoring())
    
    await reset_dut(dut)
    
    # Trigger FSM multiple times to see the sequence in the monitor
    for _ in range(3):
        dut.start.value = 1
        await dut.clk.rising_edge
        await Timer(1, "ns")
        dut.start.value = 0
        await dut.clk.rising_edge
        await Timer(20, "ns")