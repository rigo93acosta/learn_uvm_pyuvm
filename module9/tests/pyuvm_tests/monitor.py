"""Monitor: pasivo. Publica por un unico puerto lo que ve en TX y en RX."""

import cocotb
from cocotb.triggers import FallingEdge
from pyuvm import uvm_analysis_port, uvm_monitor

from items import MonitorEvent, Source


def to_int(signal):
    """Valor entero de una senal, o None si no esta resuelta ('U', 'X')."""
    try:
        return int(signal.value)
    except ValueError:
        return None


class Monitor(uvm_monitor):
    """
    Muestrea en el flanco de BAJADA. A mitad de ciclo:
      * las entradas del DUT ya tienen lo que el DUT va a capturar en el
        proximo flanco de subida, y
      * las salidas ya tienen el resultado del flanco de subida anterior.
    Asi no hay carreras con el driver (que escribe tras el flanco de subida)
    ni depende del orden en que el simulador despierta las corrutinas.

    `cycle` cuenta los ciclos desde que se solto el reset: el ciclo 0 es el
    primero en que el DUT ve rst = '0'.
    """

    def build_phase(self):
        self.dut = cocotb.top
        self.ap = uvm_analysis_port("ap", self)

    async def run_phase(self):
        cycle = 0
        in_reset = False
        while True:
            await FallingEdge(self.dut.clk)
            if to_int(self.dut.rst) != 0:
                if not in_reset:
                    self.ap.write(MonitorEvent("reset", Source.RESET))
                in_reset = True
                cycle = 0
                continue
            in_reset = False

            # RX primero: es consecuencia del TX del ciclo anterior
            if to_int(self.dut.rx_valid) == 1:
                data = to_int(self.dut.rx_data)
                if data is None:
                    self.logger.error("rx_valid = 1 con rx_data sin resolver")
                else:
                    self.ap.write(MonitorEvent("rx", Source.RX, data, cycle))
            if to_int(self.dut.tx_valid) == 1:
                data = to_int(self.dut.tx_data)
                if data is not None:
                    self.ap.write(MonitorEvent("tx", Source.TX, data, cycle))
            cycle += 1
