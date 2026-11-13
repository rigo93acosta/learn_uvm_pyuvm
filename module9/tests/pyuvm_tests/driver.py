"""Driver: solo protocolo. Convierte cada tipo de item en actividad en el bus."""

import cocotb
from cocotb.triggers import RisingEdge
from pyuvm import uvm_driver

from config import get_cfg
from defs import pack
from items import IdleItem, NewDataItem, RetxItem


class Driver(uvm_driver):
    def build_phase(self):
        self.cfg = get_cfg(self)
        self.dut = cocotb.top

    async def reset(self):
        self.dut.rst.value = 1
        self.dut.lfsr_seed.value = self.cfg.lfsr_seed
        self.dut.tx_valid.value = 0
        self.dut.tx_data.value = 0
        for _ in range(3):
            await RisingEdge(self.dut.clk)
        self.dut.rst.value = 0
        await RisingEdge(self.dut.clk)

    async def drive(self, data):
        """Envia un dato de 8 bits por TX: ocupa exactamente un ciclo."""
        self.dut.tx_valid.value = 1
        self.dut.tx_data.value = data
        await RisingEdge(self.dut.clk)
        self.dut.tx_valid.value = 0

    async def idle(self, cycles):
        """Deja pasar ciclos sin enviar nada."""
        for _ in range(cycles):
            await RisingEdge(self.dut.clk)

    async def handle(self, item):
        """Despacho por tipo: el seq_item_port de pyuvm no esta tipado."""
        match item:
            case NewDataItem() | RetxItem():
                await self.drive(pack(item.seq, item.info))
            case IdleItem():
                await self.idle(item.cycles)
            case _:
                # Un tipo nuevo de item obliga a venir aqui a anadir un `case`
                raise TypeError(f"Item desconocido: {type(item).__name__}")

    async def run_phase(self):
        await self.reset()
        while True:
            item = await self.seq_item_port.get_next_item()
            await self.handle(item)
            self.seq_item_port.item_done()
