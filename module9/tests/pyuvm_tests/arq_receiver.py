"""Receptor ARQ: envuelve ArqRx en un componente UVM con sus puertos."""

from pyuvm import uvm_analysis_port, uvm_subscriber

from arq_rx import ArqRx
from config import get_cfg
from defs import NO_DATA
from items import AckInfo, Payload, RxDecision, RxKind, Source


class ArqReceiver(uvm_subscriber):
    """
    Suscrito al monitor. Por cada dato que sale del canal:
      * ap_payload : la informacion que queda liberada en orden (al scoreboard)
      * ap_ack     : la confirmacion (al sequencer, para la secuencia reactiva)
      * ap_decision: que se hizo con el dato (a la cobertura)

    write() es una funcion normal, no una corrutina: no puede esperar tiempo
    de simulacion. Para clasificar y reenviar alcanza.
    """

    def build_phase(self):
        self.cfg = get_cfg(self)
        self.arq = ArqRx(self.cfg.window)
        self.ap_payload = uvm_analysis_port("ap_payload", self)
        self.ap_ack = uvm_analysis_port("ap_ack", self)
        self.ap_decision = uvm_analysis_port("ap_decision", self)

    def write(self, ev):
        if ev.source != Source.RX:
            return  # los eventos de TX y de reset no son para el receptor
        kind, released = self.arq.receive(ev.seq, ev.info)

        if kind == RxKind.BUFFERED:
            self.logger.info(
                f"RX   guarda   seq={ev.seq:2d} info=0x{ev.info:X} "
                f"(espera seq={self.arq.expected})"
            )
        elif kind == RxKind.DUPLICATE:
            self.logger.info(f"RX   descarta seq={ev.seq:2d} (duplicado)")

        for seq, info in released:
            if info == NO_DATA:
                # Relleno: consume su numero pero no es informacion
                self.logger.info(f"RX   relleno  seq={seq:2d} (descartado)")
            else:
                self.logger.info(f"RX   libera   seq={seq:2d} info=0x{info:X}")
                # Objeto nuevo: el evento recibido lo comparten otros suscriptores
                self.ap_payload.write(Payload("payload", seq, info))

        self.ap_decision.write(
            RxDecision("decision", kind, ev.seq, len(self.arq.rx_buffer), released)
        )
        self.ap_ack.write(AckInfo("ack", ev.seq, self.arq.expected))
