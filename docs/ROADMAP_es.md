# Estado del proyecto y rumbo

Revisión del repositorio tal como está: qué hay resuelto, qué huecos tiene la
guía y en qué orden conviene cerrarlos. Complementa a las guías `MODULE*_es.md`
(que describen el temario) diciendo qué falta para que ese temario se pueda
*comprobar*.

## El hueco principal: el DUT desaparece a mitad de curso

Los módulos 1 a 3 verifican hardware de verdad: el test escribe señales, el DUT
responde y un scoreboard compara. A partir del módulo 4 los ejemplos pasan a
simular el bus con comentarios `# In real code: cocotb.dut.x.value = ...`, y en
los módulos 6 a 8 ni los ejemplos ni los tests tocan una sola señal:

| Módulo | Ejemplos que tocan el DUT | Test del módulo toca el DUT | Notas propias |
|---|---|---|---|
| 1 | — (Python puro) | sí (`and_gate`, `counter`) | `Note_M1` |
| 2 | 5 de 5 | sí (registro, shift, FSM) | `Note_M2` |
| 3 | 0 de 6 | sí (`adder`) | `Note_M3` |
| 4 | 2 de 7 (`drivers`, `monitors`) | sí (`simple_interface`) | `Note_M4` |
| 5 | 0 de 5 | sí (`multi_channel`) | `Note_M5` |
| 6 | 0 de 5 | **no** | `Note_M6` (solo el título) |
| 7 | 0 de 6 | **no** | — |
| 8 | 0 de 9 | **no** | — |
| 9 | — (todo está en el test) | sí (`lossy_channel`) | — |

Consecuencia: en 6–8 un test "pasa" aunque el DUT esté roto. De hecho lo estaba:
el `axi4_lite_slave.v` original tiene una señal con doble driver y nadie lo
notó porque ningún test lo ejercita.

**Rumbo propuesto:** cada módulo que queda se da por resuelto cuando su test
conduce y observa el DUT real, no cuando el ejemplo imprime logs. Los ejemplos
actuales sirven como esqueleto de la arquitectura; el trabajo es sustituir cada
`# In real code:` por código real.

## Huecos concretos

### DUT

- **M2 `simple_fifo`**: no tiene ningún test (el Makefile ya acepta
  `TEST=test_simple_fifo`). Tiene dos defectos reales, conservados en el VHDL:
  `full`/`empty` van un ciclo por detrás de la ocupación, y con lectura y
  escritura simultáneas el contador de ocupación se descuadra.
- **M4 `driver_example`**: el driver con handshake usa `dut.req` / `dut.gnt`,
  que `simple_interface` no tiene (solo aparecen en comentarios, por eso no falla).
- **M5 `multi_channel`**: `master_data` y `slave_data` no se usan y no hay
  salida de datos. Un scoreboard solo puede comprobar que `ready` es `valid`
  retrasado un ciclo.
- **M6 `axi4_lite_slave`**: reescrito en VHDL (ver [VHDL_GHDL_es.md](VHDL_GHDL_es.md)).
  El `.v` sigue roto; úsalo solo como curiosidad.
- **M7 `simple_dma`**: no mueve datos (no tiene interfaz de memoria) y, tras
  reset, `dma_done` pulsa cada dos ciclos aunque nadie haya dado `dma_start`.
- **M7 `uart`**: sin divisor de baudios (1 bit = 1 ciclo) y el receptor pierde
  el bit 0: no puede recibir lo que envía su propio transmisor.
- **M7 SPI e I2C**: no existe DUT; los ejemplos corren sobre `simple_dma`.
- **M8**: copia de `simple_dma`; ningún ejemplo lo usa.

### Guía y repositorio

- El README enlazaba documentos que no existen (`STUDY.md`,
  `COVERAGE_CHECKLIST.md`, `IEEE_1800_2_COVERAGE.md`) y una carpeta `module0/`
  que tampoco. Corregido en esta revisión.
- Las guías `MODULE*.md` y `PYTHON_VERILOG_INTERACTION.md` siguen hablando de
  Verilog/Verilator en sus comandos y fragmentos. Los comandos `make` funcionan
  igual (el simulador por defecto cambió en `common.mk`); los fragmentos HDL no
  se han traducido.
- `module1/README.md` no tiene versión `_es`; el resto sí.
- Hay 99 artefactos versionados que `.gitignore` ya excluye (`__pycache__`,
  `coverage.dat`, `dump.vcd`). Para sacarlos del índice sin borrarlos del disco:
  `git rm -r --cached $(git ls-files | grep -E '__pycache__|\.dat$|\.vcd$')`.
- `pyproject.toml` pide Python ≥ 3.13 y cocotb 1.9.2; el README anunciaba
  "3.10+" y "Latest".
- No hay forma de lanzar todo de una vez y saber qué está roto. Un
  `make regress` (o un `pytest` que recorra los Makefile) daría esa foto.
- Faltan criterios de "hecho". Los ejercicios de las guías son enunciados
  abiertos ("crea un checker de protocolo") sin nada que diga cuándo están bien.

## Plan por módulo

Cada punto es comprobable: o el test falla cuando debe, o no está hecho.

### Módulo 2 — cerrar la FIFO (deuda pequeña)

1. `test_simple_fifo.py`: llenar, vaciar, comprobar orden con una `deque` como
   modelo de referencia.
2. El test debe **fallar** al escribir 17 datos seguidos o al leer y escribir
   en el mismo ciclo. Documenta en `Note_M2` qué defecto encontró cada caso.
3. Opcional: arreglar `simple_fifo.vhd` y ver el test en verde.

### Módulo 6 — AXI4-Lite de verdad (siguiente paso)

Objetivo: un agente AXI4-Lite que hable con `axi4_lite_slave.vhd`.

1. **Driver**: escritura (AW + W, esperar B) y lectura (AR, esperar R). Mantén
   `xVALID` hasta ver `xREADY` en un flanco de subida. Reutiliza la estructura
   de `protocol_example.py` rellenando los `# In real code:`.
2. **Monitor**: reconstruye transacciones a partir de los handshakes, sin
   mirar lo que hizo el driver.
3. **Scoreboard**: memoria de referencia en un `dict`. Debe modelar `WSTRB`
   (escritura parcial) y `SLVERR` fuera de `0x000`–`0xFFC`.
4. **Checker de protocolo**: `VALID` no baja sin handshake; `BRESP`/`RRESP`
   estables mientras `VALID` está alto; ninguna salida sin resolver tras reset.
5. **Cobertura funcional**: cruce de tipo de acceso × `WSTRB` × respuesta, y
   orden de llegada AW antes / después / a la vez que W.
6. **Secuencia virtual**: escritura y lectura concurrentes a la misma dirección.

Hecho cuando: una escritura con `WSTRB=0b0101` seguida de lectura devuelve solo
los bytes 0 y 2 modificados; una lectura en `0x1000` da `RRESP=2`; y si rompes
el DUT a propósito (por ejemplo, ignorando `wstrb`) el scoreboard lo detecta.
Ese último paso, la mutación, es la mejor prueba de que el testbench sirve.

### Módulo 7 — elegir un protocolo y terminarlo

Tres protocolos a medias enseñan menos que uno completo.

1. **UART (recomendado)**: monitor que decodifica `tx` bit a bit y compara con
   `tx_data`; driver sobre `rx`. El scoreboard debe destapar el bit perdido del
   receptor. Después, corregir el receptor y añadir divisor de baudios como
   genérico es un buen primer ejercicio de VHDL.
2. **DMA**: comprobar que `dma_done` llega `dma_length + 1` flancos después de
   registrar la petición y que no hay `dma_done` sin `dma_start` (falla hoy).
3. **SPI / I2C**: o se escribe un esclavo SPI pequeño en VHDL (unas 60 líneas),
   o se dejan explícitamente como ejemplos de arquitectura sin DUT. I2C con
   open-drain y ACK es bastante más trabajo; no lo empezaría antes de cerrar UART.
4. **VIP**: empaquetar el agente UART o el AXI4-Lite del módulo 6 como paquete
   reutilizable (configuración, modo activo/pasivo) en vez de un VIP genérico.

### Módulo 8 — utilidades aplicadas, no sueltas

CLP, comparadores, pools y recorders se entienden mejor integrados que en nueve
ejemplos aislados. Propuesta: aplicarlos al testbench del módulo 6.

- CLP: `+num_txn=` y `+seed=` desde `PLUSARGS`.
- Comparador: sustituir la comparación manual del scoreboard.
- Recorder: volcar las transacciones a JSON y compararlas entre dos semillas.
- `uvm_pool` / colas: transacciones pendientes por dirección.

### Módulo 9 — estímulo reactivo (nuevo)

Es el único módulo avanzado que nace con el lazo cerrado sobre el DUT: modelo
de referencia del canal, tres comprobaciones independientes y cobertura
funcional. Sirve de plantilla para lo que se pide en los módulos 6 y 7.
Sus ejercicios están en [MODULE9_es.md](MODULE9_es.md), agrupados por capacidad
de UVM (factory, ConfigDB, capas de secuencias, secuencia virtual, fases,
mutaciones) y terminan en un proyecto que mueve el ARQ al DUT con modelo de
registros.

Pendiente: no tiene script `scripts/module9.sh` ni versión en inglés de la guía.

### Transversal

- Rellenar `Note_M6` a medida que avance el AXI (es la única nota vacía).
- Un objetivo de regresión que ejecute todos los tests y resuma verde/rojo.
- Traducir a VHDL los fragmentos de `PYTHON_VERILOG_INTERACTION.md` cuando
  toque repasar el módulo 2; hasta entonces basta con `VHDL_GHDL_es.md`.

## Orden sugerido

1. Volver a ejecutar los tests ya resueltos (módulos 1–5) con GHDL. Deberían
   pasar sin cambios; si alguno falla, la causa más probable es un valor `U`.
2. FIFO del módulo 2: es corto y entrena justo lo que hace falta después
   (modelo de referencia, encontrar un bug real).
3. Módulo 6 completo contra el esclavo AXI.
4. Módulo 8 aplicado sobre el testbench del 6.
5. Módulo 7 con UART.
6. Módulo 9: primero ejecutar los tres tests y leer la cobertura; después los
   ejercicios, que reutilizan lo aprendido en 4, 5 y 6.
