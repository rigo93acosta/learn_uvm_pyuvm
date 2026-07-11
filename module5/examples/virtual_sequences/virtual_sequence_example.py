"""
Module 5 Example 5.1: Virtual Sequences
Demonstrates virtual sequencer and virtual sequence coordination.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer
import pyuvm
# Note: pyuvm uses uvm_seq_item_port, not uvm_seq_item_pull_port


class VirtualTransaction(uvm_sequence_item):
    """Transaction for virtual sequence example."""

    def __init__(self, name="VirtualTransaction"):
        super().__init__(name)
        self.data = 0
        self.channel = 0

    def __str__(self):
        return f"data=0x{self.data:02X}, channel={self.channel}"


class ChannelSequence(uvm_sequence):
    """Sequence for a single channel."""

    def __init__(self, name="ChannelSequence", channel=0, num_items=5):
        super().__init__(name)
        self.channel = channel
        self.num_items = num_items

    async def body(self):
        """Generate transactions for this channel."""
        # Sequences don't have logger by default
        logging.info(f"[{self.get_name()}] Starting channel {self.channel} sequence")

        for i in range(self.num_items):
            txn = VirtualTransaction()
            txn.data = i * 0x10
            txn.channel = self.channel

            await self.start_item(txn)
            await self.finish_item(txn)

            logging.info(
                f"[{self.get_name()}] Generated transaction {i} for channel {self.channel}: {txn}"
            )


class VirtualSequence(uvm_sequence):
    """
    Virtual sequence coordinating multiple sequencers.

    Shows:
    - Virtual sequence structure
    - Multiple sequencer coordination
    - Parallel sequence execution
    - Sequence synchronization
    """

    def __init__(self, name="VirtualSequence"):
        super().__init__(name)

        if not hasattr(self, "logger"):
            import logging
            self.logger = logging.getLogger(f"{self.__class__.__name__}.{self.get_name()}")
            self.logger.setLevel(logging.INFO)

    async def body(self):
        """Body method - coordinate multiple sequences."""
        # The sequencer we were started on IS the virtual sequencer.
        # We get the real sequencer references from it, not from attributes
        # set by hand. This is the whole point of the virtual sequencer:
        # a single place that holds the handles to the real sequencers.
        master_seqr = self.sequencer.master_seqr
        slave_seqr = self.sequencer.slave_seqr

        self.logger.info("=" * 60)
        self.logger.info(f"[{self.get_name()}] Starting virtual sequence")
        self.logger.info("=" * 60)

        # Start sequences on different sequencers in parallel
        if master_seqr and slave_seqr:
            self.logger.info("[VirtualSequence] Starting parallel sequences")

            # Start master sequence
            master_seq = ChannelSequence(name="master_seq")
            master_seq.channel = 0
            master_seq.num_items = 3
            master_task = cocotb.start_soon(master_seq.start(master_seqr))

            # Start slave sequence
            slave_seq = ChannelSequence(name="slave_seq")
            slave_seq.channel = 1
            slave_seq.num_items = 3
            slave_task = cocotb.start_soon(slave_seq.start(slave_seqr))

            # Wait for both to complete
            await master_task
            await slave_task

            self.logger.info("[VirtualSequence] Parallel sequences completed")

        # Sequential execution example
        self.logger.info("=" * 60)
        self.logger.info("[VirtualSequence] Starting sequential sequences")

        if master_seqr:
            seq1 = ChannelSequence(name="seq1")
            seq1.channel = 0
            seq1.num_items = 2
            await seq1.start(master_seqr)

        if slave_seqr:
            seq2 = ChannelSequence(name="seq2")
            seq2.channel = 1
            seq2.num_items = 2
            await seq2.start(slave_seqr)

        self.logger.info("[VirtualSequence] Sequential sequences completed")
        self.logger.info("=" * 60)


class VirtualSequencer(uvm_sequencer):
    """
    Virtual sequencer containing references to multiple sequencers.

    Shows:
    - Virtual sequencer structure
    - Multiple sequencer references
    - Virtual sequencer implementation
    """

    def build_phase(self):
        """Build phase - virtual sequencer doesn't create sub-sequencers."""
        self.logger.info(f"[{self.get_name()}] Building virtual sequencer")
        # References to actual sequencers (set in connect_phase)
        self.master_seqr = None
        self.slave_seqr = None


class VirtualDriver(uvm_driver):
    """Simple driver for virtual sequence test."""

    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building driver")
        # seq_item_port is already created by uvm_driver.__init__()

    def connect_phase(self):
        """Connect phase - connection is done by parent agent."""
        self.logger.info(f"[{self.get_name()}] Connecting driver")
        # Connection to sequencer is done by parent agent in its connect_phase

    async def run_phase(self):
        """Driver run phase - consume transactions."""
        self.logger.info(f"[{self.get_name()}] Starting driver run_phase")
        try:
            while True:
                txn = await self.seq_item_port.get_next_item()
                self.logger.info(f"[{self.get_name()}] Received transaction: {txn}")
                # Simulate some processing
                await Timer(1, units="ns")
                self.seq_item_port.item_done()
        except Exception as e:
            self.logger.warning(f"[{self.get_name()}] Driver run_phase ended: {e}")


class MasterAgent(uvm_agent):
    """Master agent."""

    def build_phase(self):
        self.logger.info("Building MasterAgent")
        self.seqr = uvm_sequencer("sequencer", self)
        self.driver = VirtualDriver.create("driver", self)

    def connect_phase(self):
        self.logger.info("Connecting MasterAgent")
        if hasattr(self.driver, "seq_item_port") and self.driver.seq_item_port:
            self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class SlaveAgent(uvm_agent):
    """Slave agent."""

    def build_phase(self):
        self.logger.info("Building SlaveAgent")
        self.seqr = uvm_sequencer("sequencer", self)
        self.driver = VirtualDriver.create("driver", self)

    def connect_phase(self):
        self.logger.info("Connecting SlaveAgent")
        if hasattr(self.driver, "seq_item_port") and self.driver.seq_item_port:
            self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class VirtualEnv(uvm_env):
    """Environment with multiple agents and virtual sequencer."""

    def build_phase(self):
        self.logger.info("Building VirtualEnv")
        self.master_agent = MasterAgent.create("master_agent", self)
        self.slave_agent = SlaveAgent.create("slave_agent", self)
        self.virtual_seqr = VirtualSequencer.create("virtual_seqr", self)

    def connect_phase(self):
        self.logger.info("Connecting VirtualEnv")
        # Connect virtual sequencer to actual sequencers
        self.virtual_seqr.master_seqr = self.master_agent.seqr
        self.virtual_seqr.slave_seqr = self.slave_agent.seqr


@pyuvm.test()
class VirtualSequenceTest(uvm_test):
    """Test demonstrating virtual sequences."""

    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Virtual Sequence Example Test")
        self.logger.info("=" * 60)
        self.env = VirtualEnv.create("env", self)

    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running virtual sequence test")

        try:
            # Create and start virtual sequence.
            # No need to pass sequencer handles by hand: the sequence gets
            # them from the virtual sequencer it is started on (self.sequencer).
            # virtual_seq = VirtualSequence.create("virtual_seq")
            virtual_seq = VirtualSequence(name="virtual_seq")
            await virtual_seq.start(self.env.virtual_seqr)

            # Give some time for sequences to complete
            await Timer(50, units="ns")

            self.logger.info("Virtual sequence test completed successfully")
        except Exception as e:
            self.logger.error(f"Virtual sequence test failed: {e}")
            import traceback

            self.logger.error(traceback.format_exc())
        finally:
            self.drop_objection()

    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Virtual sequence test completed")
        self.logger.info("=" * 60)
