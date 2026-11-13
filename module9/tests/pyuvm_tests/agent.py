"""Agente: el ARQ queda en el medio, entre el monitor y el driver."""

from pyuvm import uvm_agent

from arq_receiver import ArqReceiver
from driver import Driver
from monitor import Monitor
from reactive_sequencer import ReactiveSequencer


class Agent(uvm_agent):
    def build_phase(self):
        self.seqr = ReactiveSequencer.create("seqr", self)
        self.driver = Driver.create("driver", self)
        self.monitor = Monitor.create("monitor", self)
        self.receiver = ArqReceiver.create("receiver", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        # Lo observado -> receptor ARQ (ignora lo que no es RX)
        self.monitor.ap.connect(self.receiver.analysis_export)
        # Confirmaciones -> sequencer: aqui se cierra el lazo reactivo
        self.receiver.ap_ack.connect(self.seqr.ack_fifo.analysis_export)
