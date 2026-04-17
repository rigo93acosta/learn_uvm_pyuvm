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

# Reemplazar cocotb.logging con logging estándar de Python
class FSMMonitor:
    def __init__(self, dut):
        self.dut = dut
        self.log = logging.getLogger("cocotb.monitor")
        logging.basicConfig(level=logging.INFO)

    async def start_monitoring(self):
        """Observa los cambios de estado y las salidas en cada ciclo."""
        while True:
            await self.dut.clk.rising_edge
            # Esperamos un pequeño tiempo para que las señales se estabilicen
            await Timer(1, unit="ns") 
            
            current_state = FsmState(self.dut.state.value)
            is_done = self.dut.done.value
            
            # El monitor solo informa, no hace asserts
            self.log.info(f"[MON] Estado: {current_state.name} | Done: {is_done}")

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
    Verifica que la FSM permanezca en IDLE 
    y 'done' sea 0 sin estímulo.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)
    
    for _ in range(5):
        await dut.clk.rising_edge
        assert dut.state.value == FsmState.IDLE
        assert dut.done.value == 0, "Error: 'done' debe ser 0 en IDLE"

@cocotb.test()
async def test_fsm_sequence_logic(dut):
    """
    Verifica la secuencia IDLE -> START -> WORK -> DONE -> IDLE.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    # Disparar FSM
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
    assert dut.done.value == 1, "Error: 'done' debe ser 1 en el estado DONE"

    await dut.clk.rising_edge
    await Timer(1, "ns")
    assert dut.state.value == FsmState.IDLE

@cocotb.test()
async def test_fsm_reset_recovery(dut):
    """
    Verifica que un reset en medio de la operación regrese la FSM a IDLE.
    """

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)
    state = FsmState
    # Llegar hasta el estado WORK
    dut.start.value = 1
    await dut.clk.rising_edge # A START
    await dut.clk.rising_edge # A WORK
    dut.start.value = 0
    
    # Aplicar reset inesperado
    await reset_dut(dut, duration=5)
    assert dut.state.value == state.IDLE, "La FSM no regresó a IDLE tras reset"
    assert dut.done.value == 0, "La señal 'done' quedó pegada tras reset"


@cocotb.test()
async def test_fsm_monitor(dut):
    """
    Test con monitor para observar la secuencia de estados y salidas.
    Este test no hace asserts, solo muestra la información del monitor.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    monitor = FSMMonitor(dut)
    cocotb.start_soon(monitor.start_monitoring())
    
    await reset_dut(dut)
    
    # Disparar FSM varias veces para ver la secuencia en el monitor
    for _ in range(3):
        dut.start.value = 1
        await dut.clk.rising_edge
        await Timer(1, "ns")
        dut.start.value = 0
        await dut.clk.rising_edge
        await Timer(20, "ns")