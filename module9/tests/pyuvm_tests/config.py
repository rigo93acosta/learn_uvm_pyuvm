"""Objeto de configuracion del testbench, repartido por ConfigDB."""

import random

from pyuvm import ConfigDB, uvm_object

from defs import SEQ_MOD


class ArqConfig(uvm_object):
    """
    Un unico objeto con todo lo que se puede variar entre tests.

    El test lo crea, lo ajusta y lo publica en ConfigDB; cada componente lo
    recoge en su build_phase con get_cfg(self).
    """

    def __init__(self, name="cfg"):
        super().__init__(name)
        self.n_items = 24  # datos nuevos que envia la secuencia (rellenos incluidos)
        self.window = 4  # ventana del ARQ
        self.timeout = 4  # ciclos de espera, desde que termina un envio, antes de retransmitir
        self.gen_rate = 0.7  # probabilidad por ciclo de que el generador tenga un dato
        self.clk_period_ns = 10
        # Semilla del LFSR del canal: decide el patron de perdidas. Sale del
        # `random` que cocotb siembra con RANDOM_SEED, asi que es repetible.
        self.lfsr_seed = random.randint(1, 255)

    def validate(self):
        assert self.n_items > 0, "n_items debe ser mayor que 0"
        assert self.timeout >= 0, "timeout no puede ser negativo"
        assert 0.0 <= self.gen_rate <= 1.0, "gen_rate es una probabilidad"
        assert 0 <= self.lfsr_seed <= 255, "lfsr_seed es de 8 bits"
        # Con una ventana mayor que la mitad de la numeracion, tras la vuelta
        # a 0 no se distingue un dato nuevo de un duplicado.
        assert 1 <= self.window <= SEQ_MOD // 2, (
            f"window debe estar entre 1 y {SEQ_MOD // 2}"
        )

    def __str__(self):
        return (
            f"n_items={self.n_items} window={self.window} timeout={self.timeout} "
            f"gen_rate={self.gen_rate} lfsr_seed=0x{self.lfsr_seed:02X}"
        )


def get_cfg(component):
    """Recoge la configuracion publicada por el test."""
    return ConfigDB().get(component, "", "cfg")
