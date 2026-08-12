"""
Module 5 Test: Advanced UVM Test
Complete testbench demonstrating advanced UVM concepts.
"""

from dataclasses import dataclass
import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly, ClockCycles
from pyuvm import *
import pyuvm
import logging


class AdvancedTransaction(uvm_sequence_item):
    """Transaction for advanced UVM test."""

    def __init__(self, name="AdvancedTransaction"):
        super().__init__(name)
        self.data = 0
        self.channel = 0

    def __str__(self):
        return f"data=0x{self.data:02X}, channel={self.channel}"


class AdvancedMasterTransaction(AdvancedTransaction):
    """Transaction for master channel."""

    def __init__(self, name="AdvancedMasterTransaction"):
        super().__init__(name)
        self.valid = False

    def __str__(self):
        return f"MasterTransaction: data=0x{self.data:02X}, channel={self.channel}, valid={self.valid}"


class AdvancedSlaveTransaction(AdvancedTransaction):
    """Transaction for slave channel."""

    def __init__(self, name="AdvancedSlaveTransaction"):
        super().__init__(name)
        self.valid = False

    def __str__(self):
        return f"SlaveTransaction: data=0x{self.data:02X}, channel={self.channel}, valid={self.valid}"


class AdvancedSequenceMaster(uvm_sequence):
    """Sequence for advanced test."""

    def __init__(self, name="AdvancedSequenceMaster"):
        super().__init__(name)
        self.logger = logging.getLogger("AdvancedSequenceMaster")
        self.logger.setLevel(logging.INFO)

    async def body(self):
        """Generate transactions."""
        for i in range(5):
            txn = AdvancedMasterTransaction()
            txn.data = i * 0x10
            txn.channel = 0
            txn.valid = True
            await self.start_item(txn)
            await self.finish_item(txn)


class AdvancedSequenceSlave(uvm_sequence):
    """Sequence for advanced test."""

    def __init__(self, name="AdvancedSequenceSlave"):
        super().__init__(name)
        self.logger = logging.getLogger("AdvancedSequenceSlave")
        self.logger.setLevel(logging.INFO)

    async def body(self):
        """Generate transactions."""
        for i in range(5):
            txn = AdvancedSlaveTransaction()
            txn.data = i * 0x20
            txn.channel = 1
            txn.valid = True
            await self.start_item(txn)
            await self.finish_item(txn)


class AdvancedDriver(uvm_driver):
    """Driver for advanced test."""

    def build_phase(self):
        """seq_item_port is already created by uvm_driver.__init__()"""
        self.dut = cocotb.top

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()

            await FallingEdge(self.dut.clk)

            match item.channel:
                case 0:
                    self.dut.master_valid.value = item.valid
                    self.dut.master_data.value = item.data
                    self.logger.info(f"Driving: {item.data} to master_data")
                case 1:
                    self.dut.slave_valid.value = item.valid
                    self.dut.slave_data.value = item.data
                    self.logger.info(f"Driving: {item.data} to slave_data")
                case _:
                    self.logger.error(f"Unknown channel: {item.channel}")

            await FallingEdge(self.dut.clk)

            if item.channel == 0:
                self.dut.master_valid.value = 0
            elif item.channel == 1:
                self.dut.slave_valid.value = 0

            self.seq_item_port.item_done()


class AdvancedDriverMaster(AdvancedDriver):
    """Driver for master channel."""

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()

            await FallingEdge(self.dut.clk)

            self.dut.master_valid.value = item.valid
            self.dut.master_data.value = item.data
            self.logger.info(f"Driving: {item.data} to master_data")

            await FallingEdge(self.dut.clk)

            self.dut.master_valid.value = 0

            self.seq_item_port.item_done()


class AdvancedDriverSlave(AdvancedDriver):
    """Driver for slave channel."""

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()

            await FallingEdge(self.dut.clk)

            self.dut.slave_valid.value = item.valid
            self.dut.slave_data.value = item.data
            self.logger.info(f"Driving: {item.data} to slave_data")

            await FallingEdge(self.dut.clk)

            self.dut.slave_valid.value = 0

            self.seq_item_port.item_done()


@dataclass(kw_only=True)
class AdvancedMonitorTransaction:
    channel: int
    data: int
    valid: bool
    slave_ready: bool
    master_ready: bool


class AdvancedMonitor(uvm_monitor):
    """Monitor for advanced test."""

    def build_phase(self):
        self.dut = cocotb.top
        self.ap = uvm_analysis_port("ap", self)

    async def run_phase(self):
        while True:
            await RisingEdge(self.dut.clk)
            await ReadOnly()

            if not self.dut.rst_n.value:
                continue

            master_valid = int(self.dut.master_valid.value)
            master_ready = int(self.dut.master_ready.value)
            salve_valid = int(self.dut.slave_valid.value)
            slave_ready = int(self.dut.slave_ready.value)

            if master_valid and master_ready:
                txn = AdvancedMonitorTransaction(
                    channel=0,
                    data=int(self.dut.master_data.value),
                    valid=True,
                    slave_ready=slave_ready,
                    master_ready=master_ready,
                )
                self.ap.write(txn)
            elif salve_valid and slave_ready:
                txn = AdvancedMonitorTransaction(
                    channel=1,
                    data=int(self.dut.slave_data.value),
                    valid=True,
                    slave_ready=slave_ready,
                    master_ready=master_ready,
                )
                self.ap.write(txn)


@dataclass(kw_only=True)
class AdvancedCoverageData:
    slave_ready: int = 0
    master_ready: int = 0
    slave_data: list[int] = None
    master_data: list[int] = None

    def __str__(self) -> str:
        return (
            f"\n\nSlave Coverage: {self.slave_ready} transactions, Data: {self.slave_data}\n\n"
            f"\n\nMaster Coverage: {self.master_ready} transactions, Data: {self.master_data}\n\n"
        )


class AdvancedCoverage(uvm_subscriber):
    """Coverage for advanced test."""

    def __init__(self, name="AdvancedCoverage", parent=None):
        super().__init__(name, parent)
        self.coverage_data = AdvancedCoverageData(slave_data=[], master_data=[])

    def build_phase(self):
        """Build phase - uvm_subscriber already provides analysis export."""
        pass

    def write(self, txn):
        """Sample coverage."""
        if txn.slave_ready:
            self.coverage_data.slave_data.append(txn.data)
            self.coverage_data.slave_ready += 1
        if txn.master_ready:
            self.coverage_data.master_data.append(txn.data)
            self.coverage_data.master_ready += 1

    def report_phase(self):
        """Report coverage results."""
        self.logger.info("Coverage Report:")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Slave Transactions: {self.coverage_data}")
        # self.logger.info(f"Slave Coverage: {self.coverage_data.slave_ready} transactions, Data: {self.coverage_data.slave_data}")
        # self.logger.info(f"Master Coverage: {self.coverage_data.master_ready} transactions, Data: {self.coverage_data.master_data}")


class AdvancedAgent(uvm_agent):
    """Agent for advanced test."""

    def build_phase(self):
        self.driver = AdvancedDriver("driver", self)
        self.driver_master = AdvancedDriverMaster("driver_master", self)
        self.driver_slave = AdvancedDriverSlave("driver_slave", self)

        self.monitor = AdvancedMonitor("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
        self.seqr_master = uvm_sequencer("sequencer_master", self)
        self.seqr_slave = uvm_sequencer("sequencer_slave", self)

        ConfigDB().set(None, "*", "seqr", self.seqr)
        ConfigDB().set(None, "*", "seqr_master", self.seqr_master)
        ConfigDB().set(None, "*", "seqr_slave", self.seqr_slave)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        self.driver_master.seq_item_port.connect(self.seqr_master.seq_item_export)
        self.driver_slave.seq_item_port.connect(self.seqr_slave.seq_item_export)
        


class AdvancedEnv(uvm_env):
    """Environment for advanced test."""

    def build_phase(self):
        self.logger.info("Building AdvancedEnv")
        self.agent = AdvancedAgent.create("agent", self)
        self.coverage = AdvancedCoverage.create("coverage", self)
        self.dut = cocotb.top

    def connect_phase(self):
        self.logger.info("Connecting AdvancedEnv")
        self.agent.monitor.ap.connect(self.coverage.analysis_export)

    def end_of_elaboration_phase(self):
        self.logger.info("End of elaboration phase for AdvancedEnv")
        cocotb.fork(Clock(self.dut.clk, 10, units="ns").start())


class ResetSeq(uvm_sequence):
    """Reset sequence for advanced test."""

    async def body(self):
        self.dut = cocotb.top
        self.dut.rst_n.value = 0
        await Timer(20, units="ns")
        self.dut.rst_n.value = 1
        await Timer(20, units="ns")


class AdvancedTestSeq(uvm_sequence):
    """Sequence for advanced test."""

    logger = logging.getLogger("AdvancedTestSeq")

    async def body(self):
        self.seqr = ConfigDB().get(None, "", "seqr")
        self.seqr_master = ConfigDB().get(None, "", "seqr_master")
        self.seqr_slave = ConfigDB().get(None, "", "seqr_slave")
        self.dut = cocotb.top

        await ResetSeq().start(self.seqr)

        self.logger.setLevel(logging.INFO)
        dut_ports = [obj._name for obj in self.dut]
        self.logger.info(f"DUT: {dut_ports}")

        # Start master and slave sequences concurrently
        # False Parallel execution of sequences
        # master_seq = AdvancedSequenceMaster()
        # slave_seq = AdvancedSequenceSlave()

        # master_task = cocotb.start_soon(master_seq.start(self.seqr))
        # slave_task = cocotb.start_soon(slave_seq.start(self.seqr))

        # await master_task
        # await slave_task

        # Sequential execution of sequences 
        # await AdvancedSequenceMaster().start(self.seqr)
        # await AdvancedSequenceSlave().start(self.seqr)


        # Parallel execution of sequences 
        master_seq = AdvancedSequenceMaster()
        slave_seq = AdvancedSequenceSlave()

        master_task = cocotb.start_soon(master_seq.start(self.seqr_master))
        slave_task = cocotb.start_soon(slave_seq.start(self.seqr_slave))

        await master_task
        await slave_task

        await Timer(5, units="ns")


@pyuvm.test()
class AdvancedUVMTest(uvm_test):
    """Test class for advanced UVM."""

    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building AdvancedUVMTest")
        self.logger.info("=" * 60)
        self.env = AdvancedEnv("env", self)

    def end_of_elaboration_phase(self):
        super().end_of_elaboration_phase()
        self.sequencer = AdvancedTestSeq("sequencer")

    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running AdvancedUVMTest")

        # Start sequence
        await self.sequencer.start()
        self.drop_objection()

    def check_phase(self):
        self.logger.info("Checking AdvancedUVMTest results")

    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("AdvancedUVMTest completed")
        self.logger.info("=" * 60)
