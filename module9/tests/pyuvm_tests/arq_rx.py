"""ARQ lado RX: buffer de recepcion y liberacion en orden (Python puro, sin UVM)."""

from defs import SEQ_MOD
from items import RxKind


class ArqRx:
    def __init__(self, window):
        self.window = window
        self.expected = 0  # proximo numero que se puede liberar
        self.rx_buffer = {}  # seq -> info, llegaron adelantados

    def in_window(self, seq):
        return (seq - self.expected) % SEQ_MOD < self.window

    def receive(self, seq, info):
        """
        Procesa un dato recibido.

        Devuelve (kind, released): que se hizo con el dato y la lista de
        (seq, info) que quedan liberados, en orden, gracias a el.
        """
        released = []
        if seq == self.expected:
            kind = RxKind.IN_ORDER
            released.append((seq, info))
            self.expected = (self.expected + 1) % SEQ_MOD
            # Liberar los que estaban esperando su turno
            while self.expected in self.rx_buffer:
                released.append((self.expected, self.rx_buffer.pop(self.expected)))
                self.expected = (self.expected + 1) % SEQ_MOD
        elif self.in_window(seq):
            kind = RxKind.BUFFERED
            self.rx_buffer[seq] = info
        else:
            kind = RxKind.DUPLICATE
        return kind, released
