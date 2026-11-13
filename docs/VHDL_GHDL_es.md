# VHDL + GHDL: guía de uso

El proyecto nació con DUT en Verilog simulados con Verilator. A partir de ahora
**el DUT de referencia es VHDL y el simulador por defecto es GHDL**. Los `.v`
siguen en el repositorio como referencia y se pueden seguir simulando con
`SIM=verilator`, pero la fuente de verdad es el `.vhd`.

Los testbenches no cambian de lenguaje: siguen siendo Python (cocotb + pyuvm).
Lo que cambia es lo que hay al otro lado de `dut.<señal>`.

## Cómo ejecutar

```bash
cd module3/tests/pyuvm_tests
uv run make                 # VHDL en GHDL (por defecto)
uv run make WAVES=1         # además genera <toplevel>.vcd
uv run make SIM=verilator   # DUT Verilog heredado
uv run make clean           # siempre al cambiar de simulador o de TEST
```

Todos los Makefile incluyen [`common.mk`](../common.mk) (raíz del repositorio).
Un Makefile de ejemplo solo declara qué ejecutar:

```make
MODULE   = configdb_example          # módulo Python con los tests
TOPLEVEL = adder                     # entity del DUT
DUT_DIR  = ../../dut/simple_blocks   # carpeta con adder.vhd / adder.v
include ../../../common.mk
```

| Variable | Efecto |
|---|---|
| `SIM=ghdl` (defecto), `SIM=nvc` | usa `$(DUT_DIR)/$(TOPLEVEL).vhd` |
| `SIM=verilator`, `SIM=icarus` | usa `$(DUT_DIR)/$(TOPLEVEL).v` |
| `WAVES=1` | GHDL: `--vcd=<toplevel>.vcd`. Verilator: `--trace --trace-structs` (`dump.vcd`) |
| `HDL_COVERAGE=1` | cobertura de código HDL, solo con Verilator |
| `TEST=...` | en `tests/`, elige el módulo Python (y en los módulos 1 y 2, también el DUT) |
| `TESTCASE=...` | un solo test de cocotb (ver README, nombres `test_1`, `test_2` con cocotb 1.9.x) |

`HDL_COVERAGE` no se llama `COVERAGE` a propósito: cocotb reserva la variable de
entorno `COVERAGE` para la cobertura de código *Python* y falla si el paquete
`coverage` no está instalado.

## Los DUT

| Módulo | DUT | Relación con el `.v` |
|---|---|---|
| 1 | `and_gate`, `counter` | equivalente |
| 2 | `simple_register`, `shift_register`, `simple_fsm`, `simple_fifo` | equivalente (la FIFO conserva sus defectos, ver [ROADMAP](ROADMAP_es.md)) |
| 3 | `adder` | equivalente |
| 4 | `simple_interface` | equivalente |
| 5 | `multi_channel` | equivalente |
| 6 | `axi4_lite_slave` | **reescrito**, no equivalente (ver abajo) |
| 7 | `simple_dma`, `uart` | equivalente |
| 8 | `simple_dma` | equivalente |
| 9 | `lossy_channel` | solo VHDL, no hay versión Verilog |

"Equivalente" está comprobado, no solo revisado a mano: cada par `.v`/`.vhd` se
comparó con yosys + plugin de GHDL (miter y SAT, saliendo de reset, 40 ciclos
con entradas libres; 12 ciclos en la FIFO porque el solver no terminaba con
más). Es una comprobación acotada, no una prueba por inducción, y un mutante de
control (`count + 2`) sí es detectado. Por eso los tests ya resueltos de los
módulos 1 a 5 deberían ver exactamente el mismo comportamiento ciclo a ciclo.

### `axi4_lite_slave`: por qué se reescribió

El Verilog original asigna `write_state` desde dos bloques `always` (doble
driver, que en VHDL ni siquiera resuelve) y usa `AWADDR`/`ARADDR` cuando el
handshake de dirección ya terminó. La versión VHDL:

- usa puertos en minúsculas (`aclk`, `aresetn`, `awvalid`, ...), que es lo que
  ya escriben los ejemplos Python del módulo 6 (`dut.awvalid`, `dut.rdata`);
- acepta AW y W en cualquier orden y registra dirección y dato en su handshake;
- da `xREADY` como pulso de un ciclo, un ciclo después de ver `xVALID`;
- respeta `WSTRB` byte a byte;
- responde `SLVERR` (`"10"`) si la dirección tiene algún bit 31..12 a 1: la
  escritura se descarta y la lectura devuelve 0. Rango válido: `0x000`–`0xFFC`.

## Qué cambia para el testbench Python

### 1. Valores no resueltos (`U`, `X`)

Verilator es de 2 estados: todo arranca en 0. VHDL usa `std_logic` de 9 valores
y una señal sin valor inicial vale `'U'`. Con `'U'` o `'X'`:

```python
int(dut.q.value)            # ValueError
dut.q.value.integer         # ValueError
dut.q.value.is_resolvable   # False  -> compruébalo antes de convertir
dut.q.value.binstr          # 'UUUUUUUU'
```

Para que los tests escritos contra Verilator no cambien de comportamiento, los
`.vhd` nuevos dan valor inicial a todos los registros y `:= '0'` por defecto a
los puertos de entrada (el `rx` de la UART arranca en `'1'`, línea en reposo).
Es una decisión para facilitar la migración, no una regla de diseño: en un DUT
real no puedes contar con ello, y un buen monitor comprueba `is_resolvable`,
como ya hace `module3/tests/pyuvm_tests/test_simple_uvm.py`.

`module3/dut/simple_blocks/adder.vhd` (el que ya existía) no tiene valores por
defecto en `a` y `b`: valen `'U'` hasta que el driver los escribe, y si llega un
flanco de reloj antes, `numeric_std` avisa de *metavalue detected*.

### 2. VHDL no distingue mayúsculas

`start` y `START` son el mismo identificador. Consecuencias:

- en `simple_fsm.vhd` los estados se llaman `ST_IDLE`, `ST_START`... porque
  `START` y `DONE` chocarían con los puertos `start` y `done`;
- GHDL expone los nombres en minúsculas: desde Python usa siempre minúsculas
  (`dut.awvalid`, no `dut.AWVALID`).

### 3. Qué se puede ver desde Python

Por la interfaz VPI de GHDL se accede bien a puertos y señales `std_logic` /
`std_logic_vector` / `unsigned`. No cuentes con leer arrays de memoria
(`mem` en la FIFO o en el esclavo AXI), records ni genéricos. Si un scoreboard
necesita el contenido de la memoria, que lo lea por el bus, que además es lo
correcto en verificación de caja negra.

### 4. Ondas y cobertura

- `make WAVES=1` genera `<toplevel>.vcd` (GTKWave o Surfer lo abren). Para
  formato GHW, más compacto y con tipos VHDL: `make SIM_ARGS=--wave=dut.ghw`.
- No hay equivalente directo a `--coverage` de Verilator. La cobertura que
  importa en este curso es la **funcional**, que vive en Python y no depende
  del simulador.

### 5. Binarios junto al Makefile

El GHDL instalado (oss-cad-suite, backend LLVM) deja el ejecutable elaborado y
un `e~<toplevel>.o` en la carpeta desde la que se lanza `make`. `make clean` los
borra y `.gitignore` ya los excluye.

## Leer VHDL viniendo de Verilog

| Verilog | VHDL |
|---|---|
| `module` | `entity` (puertos) + `architecture` (implementación) |
| `input wire [7:0] d` | `d : in std_logic_vector(7 downto 0)` |
| `always @(posedge clk or negedge rst_n)` | `process(clk, rst_n)` con `if rst_n = '0' ... elsif rising_edge(clk)` |
| `<=` (no bloqueante) | `<=` (asignación de señal, se aplica al terminar el proceso) |
| `=` (bloqueante) | `:=` sobre una `variable` |
| `q + 1` sobre `reg` | hay que elegir tipo: `unsigned(q) + 1` con `ieee.numeric_std` |
| `{a, b}` | `a & b` |
| `localparam` | `constant` |
| `output reg q` | señal interna `q_reg` + `q <= q_reg;` (en VHDL-93 no se lee un puerto `out`) |

Lo último explica el patrón que se repite en todos los `.vhd`: registro interno
con sufijo `_reg` y una asignación concurrente al puerto al final.
