"""
Module 3 Test Case 3.1: Simple UVM Test
Complete UVM testbench for simple adder.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ReadOnly, FallingEdge
from pyuvm import *
import pyuvm


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
            # In real implementation, drive DUT signals
            
            await FallingEdge(self.dut.clk)
            self.dut.a.value = txn.a
            self.dut.b.value = txn.b
            await RisingEdge(self.dut.clk)
            self.logger.info(f"Driving: {txn}")
            # await Timer(10, unit="ns")
            self.seq_item_port.item_done()


class AdderMonitor(uvm_monitor):
    """Monitor for adder DUT."""

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            await RisingEdge(self.dut.clk)
            await ReadOnly()  # Nos aseguramos de estar al final del delta-cycle

            # Verificamos que el DUT ya no esté escupiendo 'X' o 'Z'
            if self.dut.sum.value.is_resolvable:
                txn = AdderTransaction("mon_txn")
                txn.a = self.dut.a.value.to_unsigned()
                txn.b = self.dut.b.value.to_unsigned()
                txn.expected_sum = self.dut.sum.value.to_unsigned()
                txn.expected_carry = int(self.dut.carry.value)

                self.ap.write(txn)
            else:
                self.logger.warning(
                    "Ignorando ciclo: El DUT todavía está inicializándose (valores en X/Z)"
                )


class AdderScoreboard(uvm_subscriber):
    """Scoreboard for adder verification."""

    def build_phase(self):
        # Use uvm_subscriber which automatically implements write() method
        self.expected = []
        self.actual = []

    def write(self, txn):
        """Receive transactions from monitor."""
        self.actual.append(txn)
        self.logger.info(f"Scoreboard received: {txn}")

    def check_phase(self):
        """Check phase - verify results."""
        self.logger.info("=" * 60)
        self.logger.info("Scoreboard Check")
        self.logger.info(f"Total transactions: {len(self.actual)}")
        if len(self.expected) == len(self.actual):
            self.logger.info("✓ Transaction count matches")
        else:
            self.logger.error(
                f"✗ Transaction count mismatch: "
                f"expected={len(self.expected)}, actual={len(self.actual)}"
            )


class AdderAgent(uvm_agent):
    """Agent for adder."""

    def build_phase(self):
        self.driver = AdderDriver.create("driver", self)
        self.monitor = AdderMonitor.create("monitor", self)
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
        self.agent.monitor.ap.connect(self.scoreboard.analysis_export)


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
