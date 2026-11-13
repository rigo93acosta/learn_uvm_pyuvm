"""Sequencer reactivo: lo que la secuencia necesita ademas de enviar items."""

from pyuvm import uvm_nonblocking_get_port, uvm_sequencer, uvm_tlm_analysis_fifo

from config import get_cfg


class ReactiveSequencer(uvm_sequencer):
    """
    Una secuencia no es un componente: no tiene puertos ni build_phase. Todo
    lo que necesita del entorno lo alcanza a traves de `self.sequencer`:

      * ack_fifo : confirmaciones que publica el receptor ARQ (lo observado)
      * info_port: de donde sale la informacion a enviar (el generador)
      * cfg      : la configuracion del test
    """

    def build_phase(self):
        self.cfg = get_cfg(self)
        self.ack_fifo = uvm_tlm_analysis_fifo("ack_fifo", self)
        self.info_port = uvm_nonblocking_get_port("info_port", self)
