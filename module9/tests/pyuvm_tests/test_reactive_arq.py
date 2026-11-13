"""
Module 9: estimulo reactivo.

Un ARQ de repeticion selectiva dentro del testbench, sobre un canal con
perdidas (lossy_channel.vhd). Lo que el monitor ve salir por RX decide lo que
la secuencia envia por TX.

Tres tests sobre el mismo entorno; solo cambia la configuracion o un override:
    TestArqDefault    -> configuracion por defecto
    TestArqImpatient  -> timeout 0: retransmite sin esperar y provoca duplicados
    TestArqNoFiller   -> override de factory: el generador nunca se queda sin dato
"""

import cocotb
import pyuvm
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from pyuvm import ConfigDB, uvm_factory, uvm_test

from arq_sequence import ArqSeq
from config import ArqConfig
from env import Env
from generator import AlwaysReadyGenerator, DataGenerator


class ArqBaseTest(uvm_test):
    """Base comun: los tests concretos solo redefinen configure() u overrides()."""

    def configure(self, cfg):
        """Ajustes de configuracion de cada test."""

    def overrides(self):
        """Overrides de factory de cada test (antes de crear el entorno)."""

    def build_phase(self):
        self.cfg = ArqConfig("cfg")
        self.configure(self.cfg)
        self.cfg.validate()
        ConfigDB().set(None, "*", "cfg", self.cfg)
        self.overrides()
        self.env = Env.create("env", self)

    def start_of_simulation_phase(self):
        self.logger.info(f"Configuracion: {self.cfg}")

    async def run_phase(self):
        self.raise_objection()
        clk = cocotb.top.clk
        cocotb.start_soon(Clock(clk, self.cfg.clk_period_ns, units="ns").start())
        seq = ArqSeq.create("seq")
        await seq.start(self.env.agent.seqr)
        for _ in range(3):  # margen para que lo ultimo llegue al scoreboard
            await RisingEdge(clk)
        self.drop_objection()


@pyuvm.test()
class TestArqDefault(ArqBaseTest):
    """Configuracion por defecto: ventana 4, timeout 4, generador al 70 %."""


@pyuvm.test()
class TestArqImpatient(ArqBaseTest):
    """
    Timeout 0: la secuencia retransmite antes de que pueda llegar la
    confirmacion (la ida y vuelta tarda un ciclo). El receptor recibe
    duplicados y tiene que descartarlos sin entregar nada dos veces.
    """

    def configure(self, cfg):
        cfg.timeout = 0


@pyuvm.test()
class TestArqNoFiller(ArqBaseTest):
    """El mismo entorno con otro generador, cambiado por factory."""

    def overrides(self):
        uvm_factory().set_type_override_by_type(DataGenerator, AlwaysReadyGenerator)
