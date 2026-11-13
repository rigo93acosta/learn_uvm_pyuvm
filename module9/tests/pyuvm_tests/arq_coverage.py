"""Cobertura funcional: que situaciones del ARQ se llegaron a ejercitar."""

from pyuvm import uvm_analysis_export, uvm_component

from defs import NO_DATA, SEQ_MOD
from items import RxKind, Source


class AnalysisImp(uvm_analysis_export):
    def __init__(self, name, parent, write_fn):
        super().__init__(name, parent)
        self.write_fn = write_fn

    def write(self, item):
        self.write_fn(item)


class ArqCoverage(uvm_component):
    """
    Un test en verde no dice que se probo. Esta clase cuenta, por nombre, las
    situaciones interesantes ("bins") y al final lista las que nunca ocurrieron.

    No hace fallar el test: es informacion para decidir que test falta.
    """

    BINS = [
        "rx_en_orden",  # llego el dato esperado
        "rx_adelantado",  # llego uno posterior y se guardo
        "rx_duplicado",  # llego uno ya liberado y se descarto
        "rx_relleno",  # se libero un relleno (sin informacion)
        "rx_libera_rafaga",  # un dato desbloqueo a otros que esperaban
        "buffer_1",  # profundidad del buffer de recepcion
        "buffer_2",
        "buffer_3",
        "seq_vuelta_a_0",  # la numeracion paso de 15 a 0
        "tx_nuevo",
        "tx_relleno",
        "tx_retx",  # una retransmision
        "tx_retx_repetida",  # el mismo dato retransmitido mas de una vez
    ]

    def build_phase(self):
        self.rx_export = AnalysisImp("rx_export", self, self.write_decision)
        self.bus_export = AnalysisImp("bus_export", self, self.write_bus)
        self.hits = {name: 0 for name in self.BINS}
        self.next_new = 0
        self.retx_count = {}  # seq -> retransmisiones desde su ultimo envio nuevo

    def hit(self, name):
        self.hits[name] += 1

    def write_decision(self, d):
        if d.kind == RxKind.IN_ORDER:
            self.hit("rx_en_orden")
        elif d.kind == RxKind.BUFFERED:
            self.hit("rx_adelantado")
        else:
            self.hit("rx_duplicado")
        if 1 <= d.depth <= 3:
            self.hit(f"buffer_{d.depth}")
        if len(d.released) > 1:
            self.hit("rx_libera_rafaga")
        for seq, info in d.released:
            if info == NO_DATA:
                self.hit("rx_relleno")
            if seq == SEQ_MOD - 1:
                self.hit("seq_vuelta_a_0")

    def write_bus(self, ev):
        if ev.source != Source.TX:
            return
        if ev.seq == self.next_new:
            self.hit("tx_relleno" if ev.info == NO_DATA else "tx_nuevo")
            self.retx_count[ev.seq] = 0
            self.next_new = (self.next_new + 1) % SEQ_MOD
        else:
            self.hit("tx_retx")
            self.retx_count[ev.seq] = self.retx_count.get(ev.seq, 0) + 1
            if self.retx_count[ev.seq] == 2:
                self.hit("tx_retx_repetida")

    def report_phase(self):
        covered = sum(1 for n in self.hits.values() if n > 0)
        self.logger.info(f"Cobertura funcional: {covered}/{len(self.BINS)} bins")
        for name in self.BINS:
            mark = "ok" if self.hits[name] else "--"
            self.logger.info(f"  [{mark}] {name:<18} {self.hits[name]}")
        holes = [name for name in self.BINS if self.hits[name] == 0]
        if holes:
            self.logger.warning(f"Sin cubrir: {', '.join(holes)}")
