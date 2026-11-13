"""
Generador: produce la informacion (4 bits) y la entrega cuando se la piden.

Lo que se entrega se publica tambien por `ap` hacia el scoreboard: solo cuenta
como generado lo que realmente se tomo para enviar.

El 0 (NO_DATA) esta reservado para el relleno, asi que solo produce 1..0xF.
"""

import random
from collections import deque

import cocotb
from cocotb.triggers import RisingEdge
from pyuvm import uvm_analysis_port, uvm_component, uvm_nonblocking_get_export

from config import get_cfg
from items import GeneratedData


class InfoExport(uvm_nonblocking_get_export):
    """Export de get no bloqueante que delega en el generador."""

    def __init__(self, name, parent, generator):
        super().__init__(name, parent)
        self.generator = generator

    def try_get(self):
        return self.generator.take()

    def can_get(self):
        return len(self.generator.queue) > 0


class DataGenerator(uvm_component):
    def build_phase(self):
        self.cfg = get_cfg(self)
        self.queue = deque()
        self.get_export = InfoExport("get_export", self, self)
        self.ap = uvm_analysis_port("ap", self)  # al scoreboard

    def has_new_data(self):
        """Hay un dato nuevo en este ciclo? (punto de extension para overrides)"""
        return random.random() < self.cfg.gen_rate

    async def run_phase(self):
        """A veces hay dato disponible y a veces no."""
        while True:
            await RisingEdge(cocotb.top.clk)
            if self.has_new_data():
                self.queue.append(random.randint(0x1, 0xF))

    def take(self):
        """Entrega el dato mas antiguo y lo publica; (False, None) si no hay."""
        if not self.queue:
            return False, None
        info = self.queue.popleft()
        self.ap.write(GeneratedData("generated", info))
        return True, info


class AlwaysReadyGenerator(DataGenerator):
    """Variante para override de factory: nunca se queda sin dato (no hay rellenos)."""

    def has_new_data(self):
        return False  # no acumula: genera en el momento en que se lo piden

    def take(self):
        if not self.queue:
            self.queue.append(random.randint(0x1, 0xF))
        return super().take()
