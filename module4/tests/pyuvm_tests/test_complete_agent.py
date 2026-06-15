"""
Module 4 Test: Complete Agent Test
Complete UVM testbench with driver, monitor, sequencer, and scoreboard.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles, ReadOnly
from pyuvm import *
import pyuvm


class InterfaceTransaction(uvm_sequence_item):
    """Transaction for interface test."""

    def __init__(self, name="InterfaceTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.expected_result = 0

    def __str__(self):
        return (
            f"data=0x{self.data:02X}, addr=0x{self.address:04X}, "
            f"expected=0x{self.expected_result:02X}"
        )


class InterfaceSequence(uvm_sequence):
    """Sequence generating test vectors."""

    async def body(self):
        """Generate test vectors."""
        test_vectors = [
            (0x01, 0x1000, 0x02),
            (0x02, 0x1001, 0x03),
            (0xFF, 0x1FFF, 0x00),  # Overflow
            (0x7F, 0x2000, 0x80),
            (0x0A, 0x3000, 0x0B),
        ]

        for data, addr, expected in test_vectors:
            txn = InterfaceTransaction()
            txn.data = data
            txn.address = addr
            txn.expected_result = expected
            await self.start_item(txn)
            await self.finish_item(txn)


class InterfaceDriver(uvm_driver):
    """Driver for interface."""

    def build_phase(self):
        self.seq_item_port = uvm_seq_item_port("driver_seq_item_port", self)
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            # In real implementation, drive DUT signals
            await FallingEdge(self.dut.clk)
            self.dut.data.value = item.data
            self.dut.address.value = item.address
            self.dut.valid.value = 1
            # await Timer(10, units="ns")
            await RisingEdge(self.dut.clk)
            self.logger.info(f"Driving: {item}")
            self.dut.valid.value = 0
            self.seq_item_port.item_done()


class InterfaceMonitor(uvm_monitor):
    """Monitor for interface."""

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            # In real implementation, sample DUT outputs
            await RisingEdge(self.dut.clk)
            await ReadOnly()
            if self.dut.ready.value.integer == 1:
                result = self.dut.result.value.integer
                # await Timer(10, units="ns")
                # Create transaction from sampled values
                txn = InterfaceTransaction()
                txn.data = self.dut.data.value.integer
                # txn.expected_result = self.dut.data.value.integer + 1 & 0xFF  # Example expected result
                self.logger.info(
                    f"Monitor sampled: data=0x{txn.data:02X}, result=0x{result:02X}"
                )
                self.ap.write((txn, result))


class InterfaceScoreboard(uvm_subscriber):
    """Scoreboard for interface."""

    def build_phase(self):
        self.actual = []
        self.mismatches = []

    def write(self, data_recv: tuple[InterfaceTransaction, int]):
        """Receive transactions."""
        txn, actual_result = data_recv
        txn.expected_result = self.model_predict(txn.data)

        self.actual.append(txn)
        if txn.expected_result != actual_result:
            self.mismatches.append((actual_result, txn))
            self.logger.error(
                f"Mismatch: actual=0x{actual_result:02X}, expected=0x{txn.expected_result:02X}"
            )

    def model_predict(self, data: int) -> int:
        """Model prediction for expected result."""
        return (data + 1) & 0xFF  # Example model: expected result is data + 1

    def check_phase(self):
        """Check phase."""
        self.logger.info(f"Scoreboard: Mismatches={len(self.mismatches)}")


class InterfaceAgent(uvm_agent):
    """Agent for interface."""

    def build_phase(self):
        self.driver = InterfaceDriver.create("driver", self)
        self.monitor = InterfaceMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class InterfaceEnv(uvm_env):
    """Environment for interface test."""

    def build_phase(self):
        self.logger.info("Building InterfaceEnv")
        self.agent = InterfaceAgent.create("agent", self)
        self.scoreboard = InterfaceScoreboard.create("scoreboard", self)

    def connect_phase(self):
        self.logger.info("Connecting InterfaceEnv")
        self.agent.monitor.ap.connect(self.scoreboard.analysis_export)


@pyuvm.test()
class CompleteAgentTest(uvm_test):
    """Test class for complete agent."""

    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building CompleteAgentTest")
        self.logger.info("=" * 60)
        self.env = InterfaceEnv.create("env", self)
        self.dut = cocotb.top

    async def run_phase(self):
        self.raise_objection()
        cocotb.start_soon(Clock(self.dut.clk, 10, units="ns").start())

        self.logger.info("Running CompleteAgentTest")
        await FallingEdge(self.dut.clk)
        self.dut.rst_n.value = 0
        await ClockCycles(self.dut.clk, 1)
        self.dut.rst_n.value = 1
        await ClockCycles(self.dut.clk, 1)
        # Note: Sequence starting has issues in current pyuvm implementation
        seq = InterfaceSequence.create("seq")
        await seq.start(self.env.agent.seqr)

        await Timer(100, units="ns")
        self.drop_objection()

    def check_phase(self):
        self.logger.info("Checking CompleteAgentTest results")

    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("CompleteAgentTest completed")
        self.logger.info("=" * 60)
