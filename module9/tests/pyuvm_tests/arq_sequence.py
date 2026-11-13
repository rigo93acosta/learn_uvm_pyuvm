"""Secuencia reactiva: el lado TX del ARQ."""

from cocotb.utils import get_sim_time
from pyuvm import uvm_sequence

from arq_tx import ArqTx
from defs import NO_DATA
from items import IdleItem, NewDataItem, RetxItem


class ArqSeq(uvm_sequence):
    """
    En cada vuelta decide entre retransmitir, enviar un dato nuevo o esperar,
    segun las confirmaciones que hayan llegado desde el lado RX.
    """

    def __init__(self, name="arq_seq"):
        super().__init__(name)

    def cycle(self):
        """Ciclo de reloj actual, sacado del tiempo de simulacion."""
        return int(get_sim_time("ns")) // self.sequencer.cfg.clk_period_ns

    async def send(self, item):
        await self.start_item(item)
        await self.finish_item(item)  # vuelve cuando el driver hizo item_done()

    def drain_acks(self, arq):
        """Procesa las confirmaciones pendientes sin bloquear."""
        # Un get() bloqueante se colgaria justo cuando el canal pierde un
        # dato, que es el caso que el ARQ existe para resolver.
        while True:
            ok, ack = self.sequencer.ack_fifo.try_get()
            if not ok:
                return
            arq.on_ack(ack.seq, ack.next_expected)

    async def body(self):
        seqr = self.sequencer
        cfg = seqr.cfg
        log = seqr.logger
        arq = ArqTx(cfg.window, cfg.timeout)
        sent_new = 0
        start = self.cycle()

        while sent_new < cfg.n_items or arq.pending():
            # 1) Reaccionar: confirmaciones que llegaron desde el lado RX
            self.drain_acks(arq)

            # 2) Decidir que se envia ahora
            seq = arq.expired(self.cycle())
            if seq is not None:
                info = arq.tx_buffer[seq]
                log.info(f"TX   RETX     seq={seq:2d} info=0x{info:X}")
                await self.send(RetxItem("retx", seq=seq, info=info))
                arq.resent(seq, self.cycle())
            elif sent_new < cfg.n_items and arq.has_room():
                ok, info = seqr.info_port.try_get()
                if not ok:
                    info = NO_DATA  # sin dato: se envia un relleno
                seq = arq.next_seq
                log.info(f"TX   nuevo    seq={seq:2d} info=0x{info:X}")
                await self.send(NewDataItem(f"new_{sent_new}", seq=seq, info=info))
                # El timeout se mide desde que el envio termino de verdad
                arq.store(info, self.cycle())
                sent_new += 1
            else:
                await self.send(IdleItem("idle", cycles=1))

            assert self.cycle() - start < 100 * cfg.n_items + 100, (
                "El ARQ no converge: el canal no entrega nada o el timeout no vence"
            )
