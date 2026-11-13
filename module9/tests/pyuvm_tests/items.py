"""
Objetos que viajan por el testbench. Todos son solo datos, sin logica.

Hay dos familias:
  * los que salen por analysis ports (observaciones y decisiones), y
  * los sequence items que la secuencia le manda al driver.
"""

from enum import Enum

from pyuvm import uvm_sequence_item

from defs import unpack


# --------------------------------------------------------------------------
# Analysis ports
# --------------------------------------------------------------------------
class Source(Enum):
    """Que vio el monitor."""

    TX = "TX"  # dato que entra al canal
    RX = "RX"  # dato que sale del canal
    RESET = "RESET"  # el DUT esta en reset


class MonitorEvent(uvm_sequence_item):
    """Observacion cruda del monitor, con el ciclo en que ocurrio."""

    def __init__(self, name, source, data=0, cycle=0):
        super().__init__(name)
        self.source = source
        self.data = data
        self.cycle = cycle  # ciclos desde que se solto el reset
        self.seq, self.info = unpack(data)


class GeneratedData(uvm_sequence_item):
    """Informacion que el generador entrego para enviar (al scoreboard)."""

    def __init__(self, name, info):
        super().__init__(name)
        self.info = info


class Payload(uvm_sequence_item):
    """Informacion liberada en orden por el receptor ARQ."""

    def __init__(self, name, seq, info):
        super().__init__(name)
        self.seq = seq
        self.info = info


class AckInfo(uvm_sequence_item):
    """Lo que el receptor le cuenta al lado TX por cada dato recibido."""

    def __init__(self, name, seq, next_expected):
        super().__init__(name)
        self.seq = seq  # numero que acaba de llegar
        self.next_expected = next_expected  # todo lo anterior ya fue liberado


class RxKind(Enum):
    """Que hizo el receptor ARQ con un dato recibido."""

    IN_ORDER = "en_orden"  # era el esperado: se libera
    BUFFERED = "adelantado"  # dentro de la ventana: se guarda
    DUPLICATE = "duplicado"  # fuera de la ventana: se descarta


class RxDecision(uvm_sequence_item):
    """Decision del receptor ARQ (para cobertura)."""

    def __init__(self, name, kind, seq, depth, released):
        super().__init__(name)
        self.kind = kind
        self.seq = seq
        self.depth = depth  # datos que quedan guardados esperando su turno
        self.released = released  # lista de (seq, info) liberados por este dato


# --------------------------------------------------------------------------
# Sequence items hacia el driver
# --------------------------------------------------------------------------
class NewDataItem(uvm_sequence_item):
    """Primer envio de un dato."""

    def __init__(self, name, seq, info):
        super().__init__(name)
        self.seq = seq
        self.info = info


class RetxItem(uvm_sequence_item):
    """Retransmision de un dato que sigue sin confirmar."""

    def __init__(self, name, seq, info):
        super().__init__(name)
        self.seq = seq
        self.info = info


class IdleItem(uvm_sequence_item):
    """Esperar sin enviar."""

    def __init__(self, name, cycles=1):
        super().__init__(name)
        self.cycles = cycles
