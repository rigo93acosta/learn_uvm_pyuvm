"""
Module 5 Example: pyuvm Callbacks Manual Implementation

pyuvm no trae un mecanismo nativo equivalente a uvm_callback de SystemVerilog UVM.
Este ejemplo replica el patrón usando listas de callbacks y llamadas explícitas.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer
import pyuvm
import logging

class DriverTransaction(uvm_sequence_item):
    """Transaction for callback example."""

    def __init__(self, name="DriverTransaction"):
        super().__init__(name)
        self.data = 0

    def __str__(self):
        return f"data=0x{self.data:02X}"


class SimpleSequence(uvm_sequence):
    """Sequence that generates a few transactions."""

    def __init__(self, name="VirtualSequence"):
        super().__init__(name)

        if not hasattr(self, "logger"):
            import logging
            self.logger = logging.getLogger(f"{self.__class__.__name__}.{self.get_name()}")
            self.logger.setLevel(logging.INFO)


    async def body(self):
        for i in range(2):
            txn = DriverTransaction()
            txn.data = i * 0xFE
            self.logger.info(f"\n\n[{self.get_name()}] Generating data=0x{txn.data:02X}")
            await self.start_item(txn)
            await self.finish_item(txn)


class DriverCallback(uvm_object):
    """
    Base callback class for driver.

    In SystemVerilog UVM this would usually extend uvm_callback.
    In pyuvm we just define a normal uvm_object with hook methods.
    """
    def __init__(self, name="DriverCallback"):
        super().__init__(name)
        self.logger = logging.getLogger(self.get_name())

    def pre_drive(self, driver, txn):
        """Called before the driver drives the transaction."""
        return txn

    def post_drive(self, driver, txn):
        """Called after the driver drives the transaction."""
        pass


class LoggingDriverCallback(DriverCallback):
    """Callback that only logs driver activity."""

    def pre_drive(self, driver, txn):
        driver.logger.info(f"[{self.get_name()}] pre_drive: {txn}")
        return txn

    def post_drive(self, driver, txn):
        driver.logger.info(f"[{self.get_name()}] post_drive: {txn}")


class ModifyDataCallback(DriverCallback):
    """Callback that modifies the transaction before driving."""

    def pre_drive(self, driver, txn):
        old_data = txn.data
        txn.data = txn.data + 0x10
        driver.logger.info(
            f"[{self.get_name()}] modified txn data: 0x{old_data:02X} -> 0x{txn.data:02X}"
        )
        return txn


class DriverWithCallbacks(uvm_driver):
    """Driver that manually supports callbacks."""

    def build_phase(self):
        self.callbacks = []
        self.logger.info(f"[{self.get_name()}] Building driver with callbacks")

    def add_callback(self, callback):
        self.callbacks.append(callback)

    async def run_phase(self):
        self.logger.info(f"[{self.get_name()}] Starting driver")

        while True:
            item = await self.seq_item_port.get_next_item()

            for callback in self.callbacks:
                item = callback.pre_drive(self, item)

            self.logger.info(f"[{self.get_name()}] Driving: {item}")
            await Timer(10, units="ns")

            for callback in self.callbacks:
                callback.post_drive(self, item)

            self.seq_item_port.item_done()


class MonitorCallback(uvm_object):
    """
    Base callback class for monitor.

    Same idea as DriverCallback, but for sampled transactions.
    """
    def __init__(self, name="MonitorCallback"):
        super().__init__(name)
        self.logger = logging.getLogger(self.get_name())

    def pre_sample(self, monitor, txn):
        """Called before publishing the sampled transaction."""
        return txn

    def post_sample(self, monitor, txn):
        """Called after publishing the sampled transaction."""
        pass


class LoggingMonitorCallback(MonitorCallback):
    """Callback that logs monitor activity."""

    def pre_sample(self, monitor, txn):
        monitor.logger.info(f"[{self.get_name()}] pre_sample: {txn}")
        return txn

    def post_sample(self, monitor, txn):
        monitor.logger.info(f"[{self.get_name()}] post_sample: {txn}")


class FilterMonitorCallback(MonitorCallback):
    """
    Example callback that modifies sampled data.

    This is just to demonstrate that callbacks can alter observed transactions too.
    """

    def pre_sample(self, monitor, txn):
        old_data = txn.data
        txn.data = txn.data ^ 0xFF
        monitor.logger.info(
            f"[{self.get_name()}] transformed sampled data: 0x{old_data:02X} -> 0x{txn.data:02X}"
        )
        return txn


class MonitorWithCallbacks(uvm_monitor):
    """Monitor that manually supports callbacks."""

    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building monitor with callbacks")
        self.ap = uvm_analysis_port("ap", self)
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    async def run_phase(self):
        self.logger.info(f"[{self.get_name()}] Starting monitor")

        while True:
            await Timer(10, units="ns")

            txn = DriverTransaction()
            txn.data = 0xAA

            for callback in self.callbacks:
                txn = callback.pre_sample(self, txn)

            self.logger.info(f"[{self.get_name()}] Sampled: {txn}")
            self.ap.write(txn)

            for callback in self.callbacks:
                callback.post_sample(self, txn)


class CallbackScoreboard(uvm_subscriber):
    """Subscriber to show transactions received from the monitor."""

    def build_phase(self):
        self.received = []

    def write(self, txn):
        self.received.append(txn)
        self.logger.info(f"[{self.get_name()}] Received transaction: {txn}")


class CallbackAgent(uvm_agent):
    """Agent with driver, monitor, sequencer and manual callbacks."""

    def build_phase(self):
        self.logger.info("Building CallbackAgent")

        self.driver = DriverWithCallbacks("driver", self)
        self.monitor = MonitorWithCallbacks("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
        ConfigDB().set(None, "*", "seqr", self.seqr)

    def connect_phase(self):
        self.logger.info("Connecting CallbackAgent")
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)

    def end_of_elaboration_phase(self):
        """
        Register callbacks manually.

        SystemVerilog UVM equivalent idea:

            uvm_callbacks#(driver_type, callback_type)::add(driver, cb)

        pyuvm manual equivalent:

            driver.add_callback(cb)
        """

        driver_log_cb = LoggingDriverCallback("driver_log_cb")
        driver_modify_cb = ModifyDataCallback("driver_modify_cb")

        monitor_log_cb = LoggingMonitorCallback("monitor_log_cb")
        monitor_filter_cb = FilterMonitorCallback("monitor_filter_cb")

        self.driver.add_callback(driver_log_cb)
        self.driver.add_callback(driver_modify_cb)

        self.monitor.add_callback(monitor_log_cb)
        self.monitor.add_callback(monitor_filter_cb)

        self.logger.info("Registered manual callbacks")


class CallbackEnv(uvm_env):
    """Environment with callback-capable agent."""

    def build_phase(self):
        self.logger.info("Building CallbackEnv")

        self.agent = CallbackAgent("agent", self)
        self.subscriber = CallbackScoreboard("subscriber", self)

    def connect_phase(self):
        self.logger.info("Connecting CallbackEnv")
        self.agent.monitor.ap.connect(self.subscriber.analysis_export)


@pyuvm.test()
class CallbackTest(uvm_test):
    """Test demonstrating manual callbacks in pyuvm."""

    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Manual Callback Example Test")
        self.logger.info("=" * 60)
        self.env = CallbackEnv("env", self)

    def end_of_elaboration_phase(self):
        self.logger.info("Starting CallbackTest sequence")
        self.seqr = ConfigDB().get(None, "", "seqr")

    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running callback test")

        seq = SimpleSequence("seq")
        await seq.start(self.seqr)
        self.drop_objection()

    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Callback test completed")
        self.logger.info("=" * 60)