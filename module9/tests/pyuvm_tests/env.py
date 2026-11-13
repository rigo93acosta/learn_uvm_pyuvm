"""Env: agente + generador + scoreboard + cobertura, y sus conexiones."""

from pyuvm import uvm_env

from agent import Agent
from arq_coverage import ArqCoverage
from generator import DataGenerator
from scoreboard import Scoreboard


class Env(uvm_env):
    def build_phase(self):
        self.agent = Agent.create("agent", self)
        self.generator = DataGenerator.create("generator", self)
        self.scoreboard = Scoreboard.create("scoreboard", self)
        self.coverage = ArqCoverage.create("coverage", self)

    def connect_phase(self):
        agent = self.agent
        # La secuencia pide la informacion al generador a traves del sequencer
        agent.seqr.info_port.connect(self.generator.get_export)

        # Scoreboard: lo generado, lo que paso en el bus y lo que se libero
        self.generator.ap.connect(self.scoreboard.gen_export)
        agent.monitor.ap.connect(self.scoreboard.bus_export)
        agent.receiver.ap_payload.connect(self.scoreboard.payload_export)

        # Cobertura: decisiones del receptor y trafico de TX
        agent.receiver.ap_decision.connect(self.coverage.rx_export)
        agent.monitor.ap.connect(self.coverage.bus_export)
