"""
Module 2 Example 2.2: Clock Generation and Management
Demonstrates clock generation patterns in cocotb.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge


async def generate_clock_simple(dut, period_ns=10):
    """
    Simple clock generation function.
    """
    while True:
        dut.clk.value = 1
        await Timer(period_ns // 2, unit="ns")
        dut.clk.value = 0
        await Timer(period_ns // 2, unit="ns")


@cocotb.test()
async def test_clock_class(dut):
    """
    Demonstrates using Clock class.
    """
    # Create clock with 10ns period
    clock = Clock(dut.clk, 10, unit="ns")
    
    # Start clock
    cocotb.start_soon(clock.start())
    
    # Wait for a few clock cycles
    for i in range(5):
        await dut.clk.rising_edge
        cocotb.log.info(f"Clock cycle {i+1}")
    
    # Clock continues running in background


@cocotb.test()
async def test_multiple_clocks(dut):
    """
    Demonstrates multiple clock domains.
    Note: This example uses the same clock for demonstration.
    In practice, you'd have multiple clock signals.
    """
    # Create clocks with different periods
    clock_fast = Clock(dut.clk, 5, unit="ns")
    clock_slow = Clock(dut.clk, 20, unit="ns")
    
    # Start fast clock
    cocotb.start_soon(clock_fast.start())
    
    # Count fast clock cycles
    for i in range(10):
        await dut.clk.rising_edge
        if i % 2 == 0:
            cocotb.log.info(f"Fast clock cycle {i//2 + 1}")


@cocotb.test()
async def test_clock_gating(dut):
    """
    Demonstrates clock gating pattern.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    clock_enable = True
    
    # Simulate clock gating
    async def gated_clock():
        while True:
            await dut.clk.rising_edge
            if not clock_enable:
                cocotb.log.info("Clock gated")
                await Timer(50, unit="ns")  # Hold for gated period
                cocotb.log.info("Clock ungated")
    
    cocotb.start_soon(gated_clock())
    
    # Enable/disable clock
    await dut.clk.rising_edge
    clock_enable = False
    await Timer(60, unit="ns")
    clock_enable = True
    await dut.clk.rising_edge


@cocotb.test()
async def test_clock_stopping(dut):
    """
    Demonstrates stopping a clock.
    
    In cocotb, Clock objects run as coroutines. To stop a clock, you can:
    1. Use a flag-based approach with a custom clock generator
    2. Use the coroutine handle's kill() method (if supported)
    3. Let the test complete naturally (clock stops when test ends)
    
    This example demonstrates the pattern for controlled clock stopping.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    clock_handle = cocotb.start_soon(clock.start())
    
    # Run for a few cycles
    for i in range(5):
        await dut.clk.rising_edge
        print(f"Clock cycle {i+1}")
    
    # Note: In cocotb, Clock objects run until the test completes.
    # For explicit clock control, use a custom clock generator with a stop flag:
    # 
    # stop_clock = False
    # async def controlled_clock():
    #     while not stop_clock:
    #         dut.clk.value = 1
    #         await Timer(period_ns // 2, unit="ns")
    #         dut.clk.value = 0
    #         await Timer(period_ns // 2, unit="ns")
    # 
    # Then set stop_clock = True when you want to stop
    
    print("Clock continues running until test completes")


@cocotb.test()
async def test_clock_division(dut):
    """
    Demonstrates clock division pattern.
    """
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    divided_clock = 0
    divide_by = 2
    
    # Create divided clock
    async def clock_divider():
        nonlocal divided_clock
        count = 0
        while True:
            await dut.clk.rising_edge
            count += 1
            if count >= divide_by:
                divided_clock = 1 - divided_clock
                count = 0
                cocotb.log.info(f"Divided clock: {divided_clock}")
    
    cocotb.start_soon(clock_divider())
    
    # Run for several cycles
    for i in range(10):
        await dut.clk.rising_edge

@cocotb.test()
async def test_multiple_clock_domains(dut):
    """Test 1: Creación y manejo de dos frecuencias distintas."""
    # Reloj principal (Fast: 100MHz / 10ns)
    clk_fast = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clk_fast.start())
    
    # Reloj de referencia (Slow: 40MHz / 25ns)
    # Lo usamos como base de tiempo interna para disparar eventos
    period_slow = 25 
    
    dut.rst_n.value = 0
    await Timer(20, unit="ns")
    dut.rst_n.value = 1

    for i in range(3):
        await Timer(period_slow, unit="ns")
        cocotb.log.info(f"Pulso del dominio lento #{i+1} a los {cocotb.utils.get_sim_time(unit='ns')}ns")


@cocotb.test()
async def test_register_gating(dut):
    """Test 2: Control de flujo mediante gating (enable)."""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    
    # Reset inicial
    dut.rst_n.value = 0
    dut.enable.value = 0
    await dut.clk.falling_edge
    dut.rst_n.value = 1

    # Intento de escritura con Gating activo (Enable = 0)
    dut.d.value = 0xA5
    await dut.clk.rising_edge
    await Timer(1, unit="ns")
    assert dut.q.value == 0x00, "Error: El registro capturó datos con enable=0"
    
    # Escritura con Gating inactivo (Enable = 1)
    dut.enable.value = 1
    await dut.clk.rising_edge
    await Timer(1, unit="ns")
    assert dut.q.value == 0xA5, f"Error: Esperado 0xA5, obtenido {hex(dut.q.value)}"


@cocotb.test()
async def test_clock_synchronization(dut):
    """Test 3: Sincronización de señales entre dominios."""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst_n.value = 1
    dut.enable.value = 0

    # Simulamos un trigger que viene de un dominio de 40ns
    for i in range(1, 4):
        # Esperamos el evento en el dominio lento
        await Timer(40, unit="ns") 
        
        # Sincronizamos con el flanco de bajada del reloj del DUT 
        # para cambiar los datos de forma segura (Setup time)
        await dut.clk.falling_edge
        
        dut.d.value = i * 5
        dut.enable.value = 1
        
        await dut.clk.rising_edge  # Sincronización con el flanco de subida para capturar el dato
        # "Cerrar" el gate inmediatamente después del flanco
        dut.enable.value = 0 
        
        # cocotb.log.info(f"Dato {hex(dut.d.value)} sincronizado y capturado correctamente.")
        cocotb.log.info(f"Dato 0x{dut.d.value.to_unsigned():02X} sincronizado y capturado correctamente.")