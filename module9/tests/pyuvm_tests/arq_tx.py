"""ARQ lado TX: buffer de retransmision (Python puro, sin UVM)."""

from defs import SEQ_MOD


class ArqTx:
    def __init__(self, window, timeout):
        self.window = window
        self.timeout = timeout
        self.base = 0  # numero mas antiguo sin confirmar
        self.next_seq = 0  # proximo numero para un dato nuevo
        self.tx_buffer = {}  # seq -> info, enviados y sin confirmar
        self.sent_at = {}  # seq -> ciclo en que termino su ultimo envio

    def has_room(self):
        """Hay lugar en la ventana para un dato nuevo?"""
        return (self.next_seq - self.base) % SEQ_MOD < self.window

    def pending(self):
        return len(self.tx_buffer) > 0

    def store(self, info, now):
        """Guarda un dato nuevo recien enviado y avanza la numeracion."""
        seq = self.next_seq
        self.tx_buffer[seq] = info
        self.sent_at[seq] = now
        self.next_seq = (self.next_seq + 1) % SEQ_MOD
        return seq

    def resent(self, seq, now):
        """Anota una retransmision (si no se confirmo mientras se enviaba)."""
        if seq in self.tx_buffer:
            self.sent_at[seq] = now

    def on_ack(self, seq, next_expected):
        """Llego una confirmacion: se libera el buffer de TX."""
        self.tx_buffer.pop(seq, None)
        self.sent_at.pop(seq, None)
        self.base = next_expected

    def expired(self, now):
        """Numero mas antiguo cuyo timeout vencio, o None."""
        for offset in range(self.window):
            seq = (self.base + offset) % SEQ_MOD
            if seq in self.tx_buffer and now - self.sent_at[seq] >= self.timeout:
                return seq
        return None
