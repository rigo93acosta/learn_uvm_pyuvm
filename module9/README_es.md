# Módulo 9: Estímulo reactivo

Un ARQ de repetición selectiva dentro del testbench, sobre un canal con
pérdidas en VHDL. Lo que el monitor ve salir del DUT decide lo que la secuencia
envía después.

La guía completa, con la explicación de cada decisión y los ejercicios, está en
[docs/MODULE9_es.md](../docs/MODULE9_es.md).

## Ejecutar

```bash
cd module9/tests/pyuvm_tests
uv run make                    # los tres tests, VHDL en GHDL
uv run make WAVES=1            # además genera lossy_channel.vcd
uv run make RANDOM_SEED=1234   # repetir un patrón de pérdidas concreto
uv run make clean
```

Este módulo es solo VHDL: no hay `lossy_channel.v` para `SIM=verilator`.

## Estructura

```
module9/
├── dut/channel/lossy_channel.vhd   # canal con pérdidas (LFSR con semilla)
└── tests/pyuvm_tests/
    ├── test_reactive_arq.py        # TestArqDefault, TestArqImpatient, TestArqNoFiller
    ├── env.py, agent.py            # jerarquía y conexiones
    ├── driver.py, monitor.py
    ├── reactive_sequencer.py       # ack_fifo, info_port, cfg
    ├── arq_sequence.py             # la secuencia reactiva
    ├── arq_tx.py, arq_rx.py        # el ARQ, Python puro
    ├── arq_receiver.py             # ArqRx como uvm_subscriber
    ├── generator.py                # de dónde sale la información
    ├── channel_model.py            # modelo de referencia del DUT
    ├── scoreboard.py               # tres comprobaciones independientes
    ├── arq_coverage.py             # 13 bins de cobertura funcional
    ├── config.py, defs.py, items.py
    └── Makefile
```

## Qué mirar en el log

- `TX   nuevo` / `TX   RETX`: lo que decide la secuencia.
- `CANAL pierde`: lo que el modelo de referencia predice que se pierde.
- `RX   guarda` / `RX   libera` / `RX   descarta`: lo que hace el receptor.
- `Scoreboard: ...`: resumen de datos, rellenos, retransmisiones y pérdidas.
- `Cobertura funcional: n/13 bins` y la lista de bins sin cubrir.

## Origen

Parte de un testbench propio (`pyuvm_reactivo`), adaptado al curso. Cambios
respecto a aquel:

| Antes | Ahora | Motivo |
|---|---|---|
| El scoreboard solo comprobaba que el canal no inventa datos | Modelo de referencia del canal: dato, latencia y pérdidas, ciclo a ciclo | El DUT casi no se verificaba |
| Sin cobertura | `ArqCoverage` y un test que provoca duplicados | La rama de duplicados nunca se ejecutaba |
| El tiempo se contaba en items | Tiempo de simulación, desde que termina cada envío | Un item de más de un ciclo rompía los timeouts |
| Monitor en el flanco de subida | Flanco de bajada | Dependía del orden de las corrutinas |
| El driver pedía la información al generador | La pide la secuencia, por el sequencer | El driver solo hace protocolo |
| Comprobaciones solo en `check_phase` | Sobre la marcha | El error aparece en el ciclo en que ocurre |
| Constantes en `defs.py` | `ArqConfig` por ConfigDB | Cada test cambia lo que necesita |
| Patrón de pérdidas fijo | Semilla del LFSR por puerto | Cada ejecución prueba otro patrón |
