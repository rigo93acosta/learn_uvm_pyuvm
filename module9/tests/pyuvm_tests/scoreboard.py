"""Scoreboard: pasivo. Comprueba el DUT y el ARQ por separado, sobre la marcha."""

from collections import deque

from pyuvm import uvm_analysis_export, uvm_scoreboard

from channel_model import LossyChannelModel
from config import get_cfg
from defs import NO_DATA, SEQ_MOD
from items import Source


class AnalysisImp(uvm_analysis_export):
    """Export de analisis que entrega cada item a una funcion del scoreboard."""

    def __init__(self, name, parent, write_fn):
        super().__init__(name, parent)
        self.write_fn = write_fn

    def write(self, item):
        self.write_fn(item)


class Scoreboard(uvm_scoreboard):
    """
    Tres comprobaciones independientes:

    A) Canal (el DUT): lo que sale por RX es exactamente lo que predice el
       modelo de referencia: mismo dato, un ciclo despues, mismas perdidas.
    B) Bus TX: los datos nuevos salen numerados de forma consecutiva y con la
       informacion que entrego el generador; una retransmision repite el dato
       original. No usa ArqTx: la referencia se deduce del bus.
    C) Extremo a extremo: la informacion que libera el receptor es la que
       entrego el generador, una sola vez y en orden.
    """

    def build_phase(self):
        self.cfg = get_cfg(self)
        self.bus_export = AnalysisImp("bus_export", self, self.write_bus)
        self.gen_export = AnalysisImp("gen_export", self, self.write_generated)
        self.payload_export = AnalysisImp("payload_export", self, self.write_payload)

        self.errors = 0
        # A) canal
        self.model = LossyChannelModel(self.cfg.lfsr_seed)
        self.model_cycle = 0  # proximo ciclo que el modelo tiene que simular
        self.expected_rx = deque()  # (ciclo, dato) que deben salir por RX
        self.n_tx = self.n_rx = self.n_lost = 0
        # B) bus TX
        self.next_new = 0  # numero que debe llevar el proximo dato nuevo
        self.first_sent = {}  # seq -> info de su primer envio
        self.n_new = self.n_retx = self.n_filler = 0
        # C) extremo a extremo
        self.generated = []  # info entregada por el generador, en orden
        self.idx_tx = 0  # cuantos generados ya se vieron salir por TX
        self.idx_delivered = 0  # cuantos generados ya libero el receptor

    def error(self, msg):
        self.errors += 1
        self.logger.error(msg)

    # ---------------------------------------------------------------- entradas
    def write_generated(self, gen):
        self.generated.append(gen.info)

    def write_bus(self, ev):
        if ev.source == Source.RESET:
            self.model.reset()
            self.model_cycle = 0
            self.expected_rx.clear()
        elif ev.source == Source.TX:
            self.check_tx(ev)
            self.predict(ev)
        else:
            self.check_rx(ev)

    def write_payload(self, payload):
        if self.idx_delivered >= len(self.generated):
            self.error(f"Se libero info=0x{payload.info:X} que nadie genero")
            return
        expected = self.generated[self.idx_delivered]
        if payload.info != expected:
            self.error(
                f"Entrega #{self.idx_delivered}: liberado 0x{payload.info:X}, "
                f"generado 0x{expected:X}"
            )
        self.idx_delivered += 1

    # ----------------------------------------------------------- A) el canal
    def predict(self, tx):
        """Pasa el TX por el modelo del canal y anota que debe salir por RX."""
        while self.model_cycle < tx.cycle:  # ciclos sin trafico: el LFSR avanza igual
            self.model.step()
            self.model_cycle += 1
        out = self.model.step(valid=True, data=tx.data)
        self.model_cycle += 1
        self.n_tx += 1
        if out is None:
            self.n_lost += 1
            kind = "relleno" if tx.info == NO_DATA else f"info=0x{tx.info:X}"
            self.logger.info(f"CANAL pierde seq={tx.seq:2d} {kind} (ciclo {tx.cycle})")
        else:
            self.expected_rx.append((tx.cycle + 1, out))

    def check_rx(self, rx):
        self.n_rx += 1
        # Lo que debia haber salido antes y no salio
        while self.expected_rx and self.expected_rx[0][0] < rx.cycle:
            cycle, data = self.expected_rx.popleft()
            self.error(f"El canal no entrego 0x{data:02X} en el ciclo {cycle}")
        if not self.expected_rx or self.expected_rx[0][0] != rx.cycle:
            self.error(f"RX inesperado 0x{rx.data:02X} en el ciclo {rx.cycle}")
            return
        _, data = self.expected_rx.popleft()
        if rx.data != data:
            self.error(
                f"Ciclo {rx.cycle}: RX 0x{rx.data:02X}, el modelo esperaba 0x{data:02X}"
            )

    # ------------------------------------------------------------ B) bus TX
    def check_tx(self, tx):
        if tx.seq == self.next_new:
            # Dato nuevo: numeracion consecutiva
            self.n_new += 1
            self.first_sent[tx.seq] = tx.info
            self.next_new = (self.next_new + 1) % SEQ_MOD
            if tx.info == NO_DATA:
                self.n_filler += 1
                return
            if self.idx_tx >= len(self.generated):
                self.error(f"TX nuevo seq={tx.seq} info=0x{tx.info:X} que nadie genero")
                return
            expected = self.generated[self.idx_tx]
            if tx.info != expected:
                self.error(
                    f"TX nuevo seq={tx.seq}: info=0x{tx.info:X}, generado 0x{expected:X}"
                )
            self.idx_tx += 1
        else:
            # Cualquier otro numero tiene que ser una retransmision
            self.n_retx += 1
            if tx.seq not in self.first_sent:
                self.error(f"TX seq={tx.seq} fuera de numeracion (esperado {self.next_new})")
            elif tx.info != self.first_sent[tx.seq]:
                self.error(
                    f"RETX seq={tx.seq}: info=0x{tx.info:X}, "
                    f"el original era 0x{self.first_sent[tx.seq]:X}"
                )

    # ------------------------------------------------------------------ final
    def check_phase(self):
        for cycle, data in self.expected_rx:
            self.error(f"El canal no entrego 0x{data:02X} en el ciclo {cycle}")
        if self.idx_delivered != len(self.generated):
            self.error(
                f"Se generaron {len(self.generated)} datos y se liberaron "
                f"{self.idx_delivered}"
            )
        if self.idx_tx != len(self.generated):
            self.error(
                f"Se generaron {len(self.generated)} datos y salieron por TX {self.idx_tx}"
            )
        if self.n_new == 0:
            self.error("No se envio ningun dato")

        self.logger.info(
            f"Scoreboard: {self.idx_delivered} datos entregados | "
            f"TX={self.n_tx} (nuevos={self.n_new}, rellenos={self.n_filler}, "
            f"retransmisiones={self.n_retx}) RX={self.n_rx} perdidos={self.n_lost}"
        )
        assert self.errors == 0, f"Scoreboard: {self.errors} error(es), ver el log"
