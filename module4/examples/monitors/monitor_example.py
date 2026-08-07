"""
Module 4 Example 4.2: UVM Monitor Implementation
Demonstrates monitor implementation with signal sampling and analysis ports.
"""

import random

import pyuvm
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb.utils import get_sim_time
from pyuvm import *


class MonitorTransaction(uvm_sequence_item):
    """Transaction created by monitor."""

    def __init__(self, name="MonitorTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.timestamp = 0

    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}, time={self.timestamp}ns"


class SimpleMonitor(uvm_monitor):
    """
    Simple monitor demonstrating basic monitor implementation.

    Shows:
    - Monitor class structure
    - Signal sampling from DUT
    - Transaction creation
    - Analysis port broadcasting
    """

    def build_phase(self):
        """Build phase - create analysis port."""
        self.logger.info(f"[{self.get_name()}] Building monitor")
        self.ap = uvm_analysis_port("ap", self)

    async def run_phase(self):
        """Run phase - main monitor loop."""
        self.logger.info(f"[{self.get_name()}] Starting monitor run_phase")

        while True:
            # Sample DUT signals and create transaction
            txn = await self.sample_signals()
            # txn = await self.sample_protocol_signals()

            if txn is not None:
                self.logger.info(f"[{self.get_name()}] Sampled transaction: {txn}")
                # Broadcast transaction via analysis port
                self.ap.write(txn)
                self.logger.info(
                    f"[{self.get_name()}] Broadcasted transaction via analysis port"
                )

    async def sample_signals(self) -> MonitorTransaction:
        """
        Sample DUT signals and create transaction.

        In real implementation, this would:
        - Wait for valid data on DUT
        - Sample signal values
        - Create and populate transaction
        """
        # Simulate signal sampling
        await Timer(10, units="ns")

        # In real code:
        # await RisingEdge(cocotb.dut.valid)
        # data = cocotb.dut.data.value.integer
        # addr = cocotb.dut.address.value.integer

        # Create transaction
        txn = MonitorTransaction()
        txn.data = random.randint(0, 255)  # Simulated sampled value
        txn.address = random.randint(0, 2**16 - 1)  # Simulated sampled value
        txn.timestamp = get_sim_time(units="ns")

        return txn

    async def sample_protocol_signals(self):
        """Sample signals based on protocol."""
        # In real code:
        # await RisingEdge(cocotb.dut.clk)
        # if cocotb.dut.valid.value:
        #     txn = MonitorTransaction()
        #     txn.data = cocotb.dut.data.value.integer
        #     return txn

        txn: MonitorTransaction = MonitorTransaction()
        txn.data = 0xCD
        txn.address = 0x2000
        return txn


class MonitorAgent(uvm_agent):
    """Agent containing monitor."""

    def build_phase(self):
        self.logger.info("Building MonitorAgent")
        self.monitor = SimpleMonitor("monitor", self)
        # self.monitor = ProtocolMonitor.create("protocol_monitor", self)
        self.dut = cocotb.top  # Reference to DUT signals

    def connect_phase(self):
        self.logger.info("Connecting MonitorAgent")

    def end_of_elaboration_phase(self):
        cocotb.start_soon(Clock(self.dut.clk, 10, units="ns").start())
        return super().end_of_elaboration_phase()


@pyuvm.test()
class MonitorTest(uvm_test):
    """Test demonstrating monitor usage."""

    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Monitor Example Test")
        self.logger.info("=" * 60)
        self.env = MonitorAgent("env", self)

    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running monitor test")
        await Timer(100, units="ns")
        self.drop_objection()

    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Monitor test completed")
        self.logger.info("=" * 60)
