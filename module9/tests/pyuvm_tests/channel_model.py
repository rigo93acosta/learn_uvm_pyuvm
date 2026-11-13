"""Modelo de referencia del DUT (Python puro, sin UVM ni cocotb)."""


class LossyChannelModel:
    """
    Replica ciclo a ciclo de lossy_channel.vhd.

    Cada llamada a step() equivale a un flanco de subida con rst = '0'.
    """

    def __init__(self, seed):
        self.seed = seed & 0xFF
        self.lfsr = self.seed

    def reset(self):
        self.lfsr = self.seed

    def step(self, valid=False, data=0):
        """Avanza un ciclo. Devuelve el dato que sale por RX, o None."""
        drop = (self.lfsr & 0b11) == 0
        out = data if (valid and not drop) else None
        feedback = ((self.lfsr >> 7) ^ (self.lfsr >> 5) ^ (self.lfsr >> 4) ^ (self.lfsr >> 3)) & 1
        self.lfsr = ((self.lfsr << 1) & 0xFF) | feedback
        return out
