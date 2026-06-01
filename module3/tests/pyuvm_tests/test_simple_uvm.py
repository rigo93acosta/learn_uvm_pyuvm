"""
Module 3 Test Case 3.1: Simple UVM Test
Complete UVM testbench for simple adder.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ReadOnly, FallingEdge, ClockCycles

from pyuvm import *
import pyuvm

from collections import deque


class AdderTransaction(uvm_sequence_item):
    """Transaction for adder test."""

    def __init__(self, name="AdderTransaction"):
        super().__init__(name)
        self.a = 0
        self.b = 0
        self.expected_sum = 0
        self.expected_carry = 0

    def __str__(self):
        return (
            f"a=0x{self.a:02X}, b=0x{self.b:02X}, "
            f"expected_sum=0x{self.expected_sum:02X}, "
            f"expected_carry={self.expected_carry}"
        )


class AdderSequence(uvm_sequence):
    """Sequence generating adder test vectors."""

    async def body(self):
        """Generate test vectors."""
        test_vectors = [
            (0x00, 0x00, 0x00, 0),
            (0x01, 0x01, 0x02, 0),
            (0xFF, 0x01, 0x00, 1),  # Overflow
            (0x80, 0x80, 0x00, 1),  # Overflow
            (0x0A, 0x05, 0x0F, 0),
        ]

        for a, b, expected_sum, expected_carry in test_vectors:
            txn = AdderTransaction()
            txn.a = a
            txn.b = b
            txn.expected_sum = expected_sum
            txn.expected_carry = expected_carry
            await self.start_item(txn)
            await self.finish_item(txn)


class AdderDriver(uvm_driver):
    """Driver for adder DUT."""

    def build_phase(self):
        # pyuvm drivers already have seq_item_port by default
        # No need to create it manually
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            txn = await self.seq_item_port.get_next_item()
            self.logger.info(f"Driving: {txn}")
            # In real implementation, drive DUT signals
            await FallingEdge(self.dut.clk)
            self.dut.a.value = txn.a
            self.dut.b.value = txn.b
            await RisingEdge(self.dut.clk)
            # await Timer(10, unit="ns")
            self.seq_item_port.item_done()


class AdderOutputMonitor(uvm_monitor):
    """Monitor for adder DUT."""

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            await RisingEdge(self.dut.clk)
            await ReadOnly()  # Nos aseguramos de estar al final del delta-cycle

            # Verificamos que el DUT ya no esté escupiendo 'X' o 'Z'
            assert self.dut.sum.value.is_resolvable, (
                "¡El DUT generó un valor X o Z indeterminado!"
            )
            txn = AdderTransaction("out_mon_txn")
            txn.expected_sum = self.dut.sum.value.to_unsigned()
            txn.expected_carry = int(self.dut.carry.value)

            self.ap.write(txn)
            self.logger.info(f"Output Monitor captured: sum=0x{txn.expected_sum:02X}, carry={txn.expected_carry}")


class AdderInputMonitor(uvm_monitor):
    """Monitor for adder DUT."""

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            await RisingEdge(self.dut.clk)
            await ReadOnly()  # Nos aseguramos de estar al final del delta-cycle

            # Verificamos que el DUT ya no esté escupiendo 'X' o 'Z'
            assert self.dut.a.value.is_resolvable, (
                "¡El DUT generó en el PORT a un valor X o Z indeterminado!"
            )
            assert self.dut.b.value.is_resolvable, (
                "¡El DUT generó en el PORT b un valor X o Z indeterminado!"
            )
            txn = AdderTransaction("in_mon_txn")
            txn.a = self.dut.a.value.to_unsigned()
            txn.b = self.dut.b.value.to_unsigned()

            self.ap.write(txn)
            self.logger.info(f"Input Monitor captured: a=0x{txn.a:02X}, b=0x{txn.b:02X}")

class AdderScoreboard(uvm_subscriber):
    """Scoreboard for adder verification."""

    def build_phase(self):
        # Use uvm_subscriber which automatically implements write() method
        self.logger.info("Building AdderScoreboard")
        # 1. Creamos los exports genéricos
        self.input_export = uvm_analysis_export("input_export", self)
        self.output_export = uvm_analysis_export("output_export", self)

        # 2. Redirigimos el método write de cada export a nuestras funciones específicas
        self.input_export.write = self.write_input
        self.output_export.write = self.write_out

        self.expected_deque = deque()
        self.failed = 0

    def write_input(self, txn):
        """Recibe transacciones del Input Monitor (Estímulos)."""
        # Calculamos la operación matemática de inmediato y la guardamos en la cola
        full_sum = txn.a + txn.b
        calc_sum = full_sum & 0xFF
        calc_carry = 1 if full_sum > 0xFF else 0

        # Guardamos el resultado "esperado" junto con los operandos para el reporte
        expected_data = {"a": txn.a, "b": txn.b, "sum": calc_sum, "carry": calc_carry}
        self.expected_deque.append(expected_data)
        self.logger.info("[SCO-IN]: Getted result.")

    def write_out(self, txn):
        """Receive transactions from monitor."""

        if not self.expected_deque:
            self.logger.error("SCO: No expected data available for comparison!")
            self.failed += 1
            return

        expected_data = self.expected_deque.popleft()

        if (
            txn.expected_sum != expected_data["sum"]
            or txn.expected_carry != expected_data["carry"]
        ):
            self.logger.error(
                f"[FAIL] Mismatch in expected results: "
                f"Expected sum=0x{expected_data['sum']:02X}, "
                f"Expected carry={expected_data['carry']}, "
                f"Got sum=0x{txn.expected_sum:02X}, "
                f"Got carry={txn.expected_carry}"
            )
            self.failed += 1
        else:
            self.logger.info(
                "[OK] Expected results match the output monitor transaction."
            )
        self.logger.info("[SCO-OUT]: Getted result.")

    def check_phase(self):
        """Check phase - verify results."""
        self.logger.info("=" * 60)
        self.logger.info("Scoreboard Check")
        if self.failed == 0:
            self.logger.info("All transactions passed!")
        else:
            self.logger.error(f"{self.failed} transactions failed!")


class AdderAgent(uvm_agent):
    """Agent for adder."""

    def build_phase(self):
        self.driver = AdderDriver.create("driver", self)
        self.in_monitor = AdderInputMonitor.create("in_monitor", self)
        self.out_monitor = AdderOutputMonitor.create("out_monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)

    def connect_phase(self):
        # In pyuvm, connect the sequencer to the driver
        # The sequencer has the seq_item_export, driver has seq_item_port
        # Connect export -> port (sequencer provides, driver consumes)
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class AdderEnv(uvm_env):
    """Environment for adder test."""

    def build_phase(self):
        self.logger.info("Building AdderEnv")
        self.agent = AdderAgent.create("agent", self)
        self.scoreboard = AdderScoreboard.create("scoreboard", self)

    def connect_phase(self):
        self.logger.info("Connecting AdderEnv")
        self.agent.in_monitor.ap.connect(self.scoreboard.input_export)
        self.agent.out_monitor.ap.connect(self.scoreboard.output_export)
        


@pyuvm.test()
class AdderTest(uvm_test):
    """Test class for adder."""

    def build_phase(self):
        """Build phase - create environment."""
        self.logger.info("=" * 60)
        self.logger.info("Building AdderTest")
        self.logger.info("=" * 60)
        self.env = AdderEnv.create("env", self)

    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running AdderTest")

        cocotb.start_soon(Clock(cocotb.top.clk, 10, unit="ns").start())
        # Reset directo por hardware usando cocotb
        self.logger.info("Applying reset")
        cocotb.top.rst_n.value = 0
        cocotb.top.a.value = 0
        cocotb.top.b.value = 0
        await ClockCycles(cocotb.top.clk, 1)
        cocotb.top.rst_n.value = 1
        
        # Start sequence
        seq = AdderSequence.create("seq")
        await seq.start(self.env.agent.seqr)

        await Timer(10, unit="ns")
        self.drop_objection()

    def check_phase(self):
        self.logger.info("Checking AdderTest results")

    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("AdderTest completed")
        self.logger.info("=" * 60)
