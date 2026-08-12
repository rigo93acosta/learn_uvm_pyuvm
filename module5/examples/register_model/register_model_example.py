"""
Module 5 Example 5.5: Conceptual Register Model

Demonstrates a small teaching register model with mirror storage, frontdoor-style
read/write, backdoor-style peek/poke, and sequence/driver integration.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer
import pyuvm
import logging

class RegisterTransaction(uvm_sequence_item):
    """Single register access request sent from the sequence to the driver."""

    def __init__(self, name="RegisterTransaction"):
        super().__init__(name)
        self.address = 0
        self.data = 0
        self.is_write = True

    def __str__(self):
        op = "WRITE" if self.is_write else "READ"
        return f"{op}: addr=0x{self.address:04X}, data=0x{self.data:02X}"


class RegisterModel(uvm_object):
    """
    Simple conceptual register model implementation.

    Shows:
    - Register model structure
    - Mirror storage using a Python dictionary
    - Frontdoor-style register operations
    - Backdoor-style register operations

    For production verification, prefer a structured RegMap generated from a
    register description source when the design has many registers or fields.
    """

    def __init__(self, name="RegisterModel"):
        super().__init__(name)

        # Mirror storage for this demo. A production model would also track
        # reset values, access permissions, masks, desired values, and fields.
        self.registers = {}

        # Minimal address map used only for readable log messages.
        self.reg_defs = {
            0x0000: "CONTROL",
            0x0004: "STATUS",
            0x0008: "DATA",
            0x000C: "CONFIG",
        }
        self.logger = logging.getLogger(self.get_name())
        self.logger.setLevel(logging.INFO)

    def write(self, address, data):
        """Frontdoor-style write: update the mirror as if a bus write happened."""
        self.logger.info(
            f"[{self.get_name()}] Writing register 0x{address:04X} ({self.reg_defs.get(address, 'UNKNOWN')}): 0x{data:02X}"
        )
        self.registers[address] = data
        return True

    def read(self, address):
        """Frontdoor-style read: return the current mirrored value."""
        value = self.registers.get(address, 0)
        self.logger.info(
            f"[{self.get_name()}] Reading register 0x{address:04X} ({self.reg_defs.get(address, 'UNKNOWN')}): 0x{value:02X}"
        )
        return value

    def peek(self, address):
        """Backdoor-style read: inspect the mirror without bus activity."""
        value = self.registers.get(address, 0)
        self.logger.info(f"[{self.get_name()}] Peeking register 0x{address:04X}: 0x{value:02X}")
        return value

    def poke(self, address, data):
        """Backdoor-style write: force the mirror without bus activity."""
        self.logger.info(f"[{self.get_name()}] Poking register 0x{address:04X}: 0x{data:02X}")
        self.registers[address] = data
        return True

    def update(self):
        """Placeholder for writing desired mirrored values back to hardware."""
        self.logger.info(f"[{self.get_name()}] Updating registers")
        for addr, value in self.registers.items():
            print(f"  Register 0x{addr:04X}: 0x{value:02X}")
        return True


class RegisterSequence(uvm_sequence):
    """Sequence for register access."""

    def __init__(self, name="RegisterSequence"):
        super().__init__(name)
        self.logger = logging.getLogger(self.get_name())
        self.logger.setLevel(logging.INFO)

    async def body(self):
        """Body method - perform register operations."""
        self.logger.info(f"[{self.get_name()}] Starting register sequence")

        # In a fuller model, the sequence could access a generated RegMap via
        # the sequencer, or call a higher-level API such as reg_model.status.read().
        # reg_model = self.sequencer.reg_model

        # Fixed operations keep the example focused on sequence/driver flow.
        operations = [
            (0x0000, 0x01, True),  # Write CONTROL
            (0x0004, 0x00, False),  # Read STATUS
            (0x0008, 0xAB, True),  # Write DATA
            (0x000C, 0x00, False),  # Read CONFIG
        ]

        for addr, data, is_write in operations:
            txn = RegisterTransaction()
            txn.address = addr
            txn.data = data
            txn.is_write = is_write

            await self.start_item(txn)
            await self.finish_item(txn)

            self.logger.info(f"[{self.get_name()}] Register operation: {txn}")


class RegisterDriver(uvm_driver):
    """Driver for register access."""

    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building register driver")

        # seq_item_port is created by uvm_driver. This optional model reference
        # shows where a bus adapter or RegMap-facing API could be connected.
        self.reg_model = None

    async def run_phase(self):
        """Run phase - execute register operations."""
        self.logger.info(f"[{self.get_name()}] Starting register driver")

        while True:
            item = await self.seq_item_port.get_next_item()

            # This demo only logs the request. A real driver would translate the
            # register access into pin/bus activity, and a monitor/predictor would
            # update the mirror from the observed transaction.
            if item.is_write:
                self.logger.info(f"[{self.get_name()}] Writing register: {item}")
            else:
                self.logger.info(f"[{self.get_name()}] Reading register: {item}")

            await Timer(10, units="ns")
            self.seq_item_port.item_done()


class RegisterAgent(uvm_agent):
    """Agent for register access."""

    def build_phase(self):
        self.logger.info("Building RegisterAgent")
        self.driver = RegisterDriver("driver", self)
        self.seqr = uvm_sequencer("sequencer", self)

        # The demo keeps the model inside the agent. Larger environments often
        # place a generated RegMap at env level and share it with sequences,
        # adapters, scoreboards, and predictors.
        self.reg_model = RegisterModel("reg_model")
        self.driver.reg_model = self.reg_model

    def connect_phase(self):
        self.logger.info("Connecting RegisterAgent")
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class RegisterEnv(uvm_env):
    """Environment with register model."""

    def build_phase(self):
        self.logger.info("Building RegisterEnv")
        self.agent = RegisterAgent("agent", self)

    def connect_phase(self):
        self.logger.info("Connecting RegisterEnv")


@pyuvm.test()
class RegisterModelTest(uvm_test):
    """Test demonstrating register model."""

    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Register Model Example Test")
        self.logger.info("=" * 60)
        self.env = RegisterEnv("env", self)

    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running register model test")

        # Direct model accesses demonstrate the API without going through the
        # sequence/driver path.
        self.logger.info("=" * 60)
        self.logger.info("Register Operations:")

        self.env.agent.reg_model.write(0x0000, 0x01)
        value = self.env.agent.reg_model.read(0x0000)
        self.logger.info(f"Read back value: 0x{value:02X}")

        self.env.agent.reg_model.poke(0x0004, 0x80)
        value = self.env.agent.reg_model.peek(0x0004)
        self.logger.info(f"Peeked value: 0x{value:02X}")

        # The sequence path demonstrates normal pyuvm sequencer/driver traffic.
        seq = RegisterSequence("seq")
        await seq.start(self.env.agent.seqr)

        await Timer(10, units="ns")
        self.drop_objection()

    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Register model test completed")
        self.logger.info("=" * 60)
