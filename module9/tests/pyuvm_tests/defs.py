"""
Formato del dato de 8 bits que viaja por el canal:
    bits 7..4 -> numero de secuencia (seq)
    bits 3..0 -> informacion (info)

El canal (DUT) no interpreta el dato: este formato solo lo conoce el ARQ.
"""

SEQ_BITS = 4
SEQ_MOD = 1 << SEQ_BITS  # la numeracion va de 0 a 15 y vuelve a 0
NO_DATA = 0x0  # info de relleno: no habia dato que enviar; el receptor lo descarta


def pack(seq, info):
    """Arma el dato de 8 bits: seq en el nibble alto, info en el bajo."""
    return ((seq & 0xF) << 4) | (info & 0xF)


def unpack(data):
    """Separa el dato de 8 bits en (seq, info)."""
    return (data >> 4) & 0xF, data & 0xF
