# Módulo 2: Fundamentos de cocotb

**Objetivo**: Dominar cocotb para la verificación de hardware

## Resumen

Este módulo ofrece una cobertura completa de cocotb, el framework de testbench basado en corrutinas que permite testbenches en Python para diseños de hardware. Aprenderás a interactuar con simuladores, generar señales, muestrear valores y crear testbenches robustos.

> **📖 Concepto fundamental**: Antes de profundizar, asegúrate de entender [How Python and Verilog Interact](PYTHON_VERILOG_INTERACTION.md). Este documento explica la arquitectura de dos capas, el flujo de señales, la sincronización temporal y cómo cocotb conecta los testbenches en Python con los diseños en Verilog.

### Ejemplos y estructura de código

Este módulo incluye ejemplos y testbenches en el directorio `module2/`:

```
module2/
├── examples/              # ejemplos de cocotb por tema
│   ├── signal_access/     # lectura y escritura de señales
│   ├── clock_generation/  # patrones de generación de reloj
│   ├── triggers/          # uso de triggers
│   ├── reset_patterns/    # secuencias de reset
│   └── common_patterns/   # patrones comunes de verificación
├── dut/                   # módulos Verilog del DUT
│   ├── registers/         # módulos de registro
│   ├── fifos/             # módulos FIFO
│   └── state_machines/    # máquinas de estado
├── tests/                 # testbenches
│   └── cocotb_tests/      # testbenches de cocotb
└── README.md              # documentación del Módulo 2
```

### Inicio rápido

**Ejecutar todos los tests usando el script orquestador:**
```bash
# Ejecutar todos los tests de cocotb
./scripts/module2.sh --cocotb-tests

# Ejecutar ejemplos específicos (nota: los ejemplos son archivos de test de cocotb)
./scripts/module2.sh --signal-access
./scripts/module2.sh --clock-generation
./scripts/module2.sh --triggers
./scripts/module2.sh --reset-patterns
./scripts/module2.sh --common-patterns
```

**Ejecutar ejemplos individualmente:**
```bash
# Activar entorno virtual (si se usa)
source .venv/bin/activate

# Ejecutar tests de cocotb
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_simple_register
make SIM=verilator TEST=test_shift_register

# Ejecutar ejemplos (son archivos de test de cocotb)
cd module2/examples/signal_access
# Crear un Makefile o ejecutar cocotb directamente
```

## Temas cubiertos

### 1. Arquitectura y conceptos de cocotb

- **¿Qué es cocotb?**
  - Framework de testbench basado en corrutinas
  - Testbenches en Python para Verilog/VHDL
  - Abstracción del simulador
  - Historia y motivación

- **Arquitectura de cocotb**
  - Capa de testbench en Python
  - Capa de interfaz con el simulador
  - Interacción con el DUT
  - Planificación de eventos

- **Conceptos clave**
  - Corrutinas para la simulación
  - Triggers para sincronización
  - Handles para acceso a señales
  - Gestión del tiempo de simulación

### 2. Integración con simuladores

- **Simuladores soportados**
  - Verilator (recomendado)
  - Icarus Verilog
  - ModelSim/QuestaSim
  - GHDL (VHDL)
  - VCS, Xcelium (comerciales)

- **Selección de simulador**
  - Variables de entorno
  - Configuración del Makefile
  - Características específicas de cada simulador

- **Proceso de compilación**
  - Compilación de Verilog
  - Compilación/ligado de la librería cocotb
  - Proceso de linking
  - Estructura del Makefile

### 3. Generación y gestión de relojes

- **Generación de reloj**
  - Uso de la clase `Clock`
  - Parámetros del reloj (periodo, unidades)
  - Inicio de relojes
  - Relojes múltiples

- **Patrones de reloj**
  - Relojes regulares
  - Relojes con gating
  - División de reloj
  - Parada de reloj

- **Gestión de dominios de reloj**
  - Múltiples dominios de reloj
  - Cruce de dominios (CDC)
  - Sincronización entre dominios

### 4. Acceso y conducción de señales

- **Handles de señales**
  - Acceso a señales del DUT
  - Sintaxis `dut.signal_name`
  - Tipos de valor de señal
  - Propiedades de la señal

- **Lectura de valores de señal**
  - Propiedad `.value`
  - Conversión a entero
  - Representación binaria
  - Comprobación del estado de la señal

- **Conducción de señales**
  - Asignación de valores
  - Asignación como entero
  - Asignación por cadena binaria
  - Alto impedancia (Z) y desconocido (X)

- **Tipos de señales**
  - Señales de 1 bit
  - Señales multibit (vectores)
  - Buses y arrays
  - Señales bidireccionales

### 5. Triggers y corrutinas

- **Tipos de trigger**
  - `RisingEdge(signal)`
  - `FallingEdge(signal)`
  - `Edge(signal)` (cualquier flanco)
  - `Timer(time, units)`
  - `ReadOnly()` (fin del paso de tiempo)
  - `ReadWrite()` (durante el paso de tiempo)
  - `Combine(*triggers)` (múltiples triggers)
  - `First(*triggers)` (el primero que ocurra)

- **Ejecución de corrutinas**
  - Definir corrutinas
  - Iniciar corrutinas
  - `cocotb.start_soon()` vs `await`
  - Ejecución en paralelo

- **Sincronización de corrutinas**
  - Esperar triggers
  - Coordinar múltiples corrutinas
  - Manejo de timeouts
  - Propagación de excepciones

### 6. Estructura y organización de tests

- **Estructura de funciones de test**
  - Decorador `@cocotb.test()`
  - Firma de la función de test
  - Parámetro `dut`
  - Organización de tests

- **Fases del test**
  - Fase de setup
  - Ejecución del test
  - Fase de limpieza
  - Manejo de errores

- **Múltiples tests**
  - Descubrimiento de tests
  - Selección de tests
  - Parámetros de test
  - Fixtures de test

### 7. Reset e inicialización

- **Estrategias de reset**
  - Reset síncrono
  - Reset asíncrono
  - Secuencias de reset
  - Verificación del reset

- **Patrones de inicialización**
  - Inicialización de señales
  - Inicialización de estados
  - Configuración
  - Condiciones iniciales

### 8. Patrones comunes de verificación

- **Generación de estímulos**
  - Patrones secuenciales
  - Patrones aleatorios
  - Aleatorio con restricciones
  - Estímulos desde archivos

- **Chequeo de respuestas**
  - Chequeo inmediato
  - Chequeo diferido
  - Comparación con modelo de referencia
  - Patrones de scoreboard

- **Modelado a nivel de transacción**
  - Clases de transacción
  - Generación de transacciones
  - Ejecución de transacciones
  - Chequeo de transacciones

**Ver Ejemplo 2.6**: Patrones de verificación comunes (`module2/examples/common_patterns/common_patterns_example.py`) para implementación detallada.

### 9. Depuración con cocotb

- **Logging e informes**
  - Logging de cocotb
  - Niveles de log
  - Formato de logs
  - Mensajes de depuración

- **Generación de formas de onda**
  - Generación de archivos VCD
  - Generación de archivos FST
  - Visualización de formas de onda
  - Trazado de señales

- **Depuración interactiva**
  - Depurador de Python (`pdb`)
  - Breakpoints
  - Inspección de variables
  - Depuración paso a paso

- **Problemas comunes**
  - Errores de acceso a señales
  - Problemas de temporización
  - Simulaciones colgadas
  - Problemas de conversión de valores

### 10. Características avanzadas de cocotb

- **Acceso a memoria**
  - Modelado de memoria
  - Inicialización de memoria
  - Patrones de acceso a memoria

- **Bus Functional Models (BFM)**
  - Conceptos de BFM
  - Implementación de BFM
  - BFMs reutilizables

- **Optimización de rendimiento**
  - Eficiencia de corrutinas
  - Optimización de triggers
  - Velocidad de simulación
  - Uso de memoria

### 11. Integración con pytest

- **Integración con pytest**
  - Uso de pytest con cocotb
  - Descubrimiento de tests
  - Fixtures
  - Parametrización

- **Organización de tests**
  - Estructura de directorios de tests
  - Convenciones de nombrado
  - Agrupación de tests
  - Ejecución de tests

## Resultados de aprendizaje

Al finalizar este módulo deberías poder:

- Entender la arquitectura de cocotb
- Integrarte con simuladores
- Generar y gestionar relojes
- Acceder y conducir señales
- Usar triggers eficazmente
- Estructurar tests correctamente
- Implementar secuencias de reset
- Usar patrones comunes de verificación
- Depurar testbenches de cocotb
- Optimizar el rendimiento del testbench

## Casos de prueba

### Caso de prueba 2.1: Acceso básico a señales
**Objetivo**: Acceder y leer señales del DUT

**Temas**:
- Handles de señal
- Lectura de valores
- Tipos de señal

#### Ejemplo 2.1: Acceso a señales (`module2/examples/signal_access/signal_access_example.py`)

**Lo que demuestra:**
- **Handles de señal**: Acceso a señales del DUT usando `dut.signal_name`
- **Lectura de valores**: Lectura con la propiedad `.value`
- **Tipos de valor**: Representación entera, binaria y hex
- **Propiedades de la señal**: Ancho, nombre, ruta
- **Asignaciones de valor**: Formas diferentes de asignar valores (entero, BinaryValue)

**Ejecución:**
```bash
# Usando el script orquestador (ejecuta tests)
./scripts/module2.sh --signal-access

# O manualmente con cocotb
cd module2/examples/signal_access
# Nota: son archivos de test de cocotb, requieren Makefile correcto
```

**Salida esperada:**
```
     0.00ns INFO     cocotb.regression                  Running test_signal_access_basic (1/3)
Initial q value: 0
Initial q value (integer): 0
Initial q value (binary): 00000000
After reset q value: 0
After write q value: 0xAB
     0.00ns INFO     cocotb.regression                  test_signal_access_basic passed
```

**Conceptos clave:**
- `dut.signal_name`: Acceder señales del DUT
- `.value`: Obtener/establecer el valor de una señal
- `.value.integer`: Obtener representación entera
- `.value.binstr`: Obtener representación binaria
- `BinaryValue`: Crear valores desde cadenas binarias
- Ancho de señal: usar `len(dut.signal)` para obtener el ancho

### Caso de prueba 2.2: Generación de reloj
**Objetivo**: Generar y gestionar relojes

**Temas**:
- Clase `Clock`
- Inicio de relojes
- Relojes múltiples

#### Ejemplo 2.2: Generación de reloj (`module2/examples/clock_generation/clock_generation_example.py`)

**Lo que demuestra:**
- **Clase Clock**: Uso de `Clock(dut.clk, period, units)` para crear relojes
- **Inicio de relojes**: `cocotb.start_soon(clock.start())` para ejecutar en background
- **Relojes múltiples**: Crear y gestionar múltiples dominios de reloj
- **Gating de reloj**: Implementar enable/disable
- **División de reloj**: Crear relojes divididos
- **Parada de reloj**: Detener generación de reloj

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module2.sh --clock-generation

# O manualmente
cd module2/examples/clock_generation
# Ejecutar como test de cocotb
```

**Salida esperada:**
```
     0.00ns INFO     cocotb.regression                  Running test_clock_class (1/5)
Clock cycle 1
Clock cycle 2
Clock cycle 3
Clock cycle 4
Clock cycle 5
     0.00ns INFO     cocotb.regression                  test_clock_class passed
```

**Conceptos clave:**
- `Clock(signal, period, units)`: Crear objeto de reloj
- `clock.start()`: Iniciar generación de reloj (devuelve corrutina)
- `cocotb.start_soon()`: Ejecutar corrutina en background
- Relojes múltiples: cada reloj corre independientemente
- Gating de reloj: controlar con señales enable
- División de reloj: dividir frecuencia contando flancos

### Caso de prueba 2.3: Conducción de señales
**Objetivo**: Conducir señales con valores

**Temas**:
- Asignación de valores
- Control de temporización
- Actualizaciones de señales

#### Ejemplo 2.3: Conducción de señales

**Lo que demuestra:**
La conducción de señales se muestra en varios ejemplos, especialmente en:
- Ejemplo de acceso a señales: lectura y escritura
- Ejemplo de reset: conducción de señales de reset
- Patrones comunes: conducción de señales de datos con temporización

**Conceptos clave:**
- Asignación directa: `dut.signal.value = value`
- Asignación entera: `dut.signal.value = 0xAB`
- Asignación binaria: `dut.signal.value = BinaryValue("10101010")`
- Asignación en hex: `dut.signal.value = 0xAB`
- Control de temporización: usar `await Timer()` o `await RisingEdge()` antes de leer
- Trigger `ReadOnly`: esperar `ReadOnly()` para asegurar estabilidad
- Actualizaciones de señal: las señales se actualizan en el siguiente paso de simulación

**Patrón de ejemplo:**
```python
# Conducir señal
dut.data.value = 0xAB

# Esperar propagación
await RisingEdge(dut.clk)
await Timer(1, units="ns")  # Pequeño retardo para lógica combinacional

# Leer
assert dut.output.value.integer == expected_value
```

**Ver también:**
- Conducción en `module2/examples/signal_access/signal_access_example.py`
- Reset en `module2/examples/reset_patterns/reset_patterns_example.py`
- Señales de datos en `module2/examples/common_patterns/common_patterns_example.py`

### Caso de prueba 2.4: Uso de triggers
**Objetivo**: Usar varios triggers

**Temas**:
- Triggers en flanco
- Triggers temporales
- Triggers combinados

#### Ejemplo 2.4: Triggers (`module2/examples/triggers/triggers_example.py`)

**Lo que demuestra:**
- Triggers de flanco: `RisingEdge()`, `FallingEdge()`, `Edge()`
- Triggers temporales: `Timer(time, units)` para retardo por tiempo
- `ReadOnly()`: espera al final del paso de tiempo
- `ReadWrite()`: durante el paso de tiempo
- `Combine(*triggers)`: esperar a que ocurran todos
- `First(*triggers)`: esperar al primero que ocurra
- Manejo de timeouts: usar triggers con timeout
- Ejecución en paralelo: múltiples corrutinas con triggers diferentes

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module2.sh --triggers

# O manualmente
cd module2/examples/triggers
# Ejecutar como test de cocotb
```

**Salida esperada:**
```
     0.00ns INFO     cocotb.regression                  Running test_edge_triggers (1/7)
Waiting for rising edge...
Rising edge detected
Waiting for falling edge...
Falling edge detected
Waiting for any edge...
Edge detected
     0.00ns INFO     cocotb.regression                  test_edge_triggers passed
```

**Conceptos clave:**
- `RisingEdge(signal)`: Espera transición 0→1
- `FallingEdge(signal)`: Espera transición 1→0
- `Edge(signal)`: Espera cualquier flanco
- `Timer(time, units)`: Espera tiempo especificado
- `ReadOnly()`: Espera al fin del paso de tiempo (señales estables)
- `Combine(*triggers)`: Espera a que todos ocurran
- `First(*triggers)`: Espera al primer trigger que ocurra
- Ejecución paralela: múltiples corrutinas pueden esperar distintos triggers

### Caso de prueba 2.5: Secuencia de reset
**Objetivo**: Implementar secuencia de reset

**Temas**:
- Patrones de reset
- Verificación de reset
- Inicialización

#### Ejemplo 2.5: Reset (`module2/examples/reset_patterns/reset_patterns_example.py`)

**Lo que demuestra:**
- Reset asíncrono: secuencia asíncrona con temporización
- Reset síncrono: reset sincronizado con reloj
- Verificación del reset: comprobar que el DUT queda en estado conocido
- Temporización del reset: asegurar tiempos correctos de assert/deassert
- Inicialización: configurar señales tras reset
- Reset en operación: probar reset mientras el DUT está operando

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module2.sh --reset-patterns

# O manualmente
cd module2/examples/reset_patterns
# Ejecutar como test de cocotb
```

**Salida esperada:**
```
     0.00ns INFO     cocotb.regression                  Running test_async_reset (1/4)
Asserting async reset...
Deasserting async reset...
Reset complete
✓ Async reset verified
     0.00ns INFO     cocotb.regression                  test_async_reset passed
```

**Conceptos clave:**
- Reset asíncrono: afirmación del reset, esperar duración, desafirmar
- Reset síncrono: afirmar reset, esperar ciclos de reloj, desafirmar en flanco
- Verificación del reset: siempre comprobar estado conocido
- Temporización del reset: asegurar propagación
- Inicialización: configurar señales de control tras reset
- Patrones de reset: crear funciones reutilizables

#### Ejemplo 2.6: Patrones comunes (`module2/examples/common_patterns/common_patterns_example.py`)

**Lo que demuestra:**
- Patrones secuenciales: generación determinista de estímulos
- Patrones aleatorios: estímulos aleatorios con control de semilla
- Patrón de scoreboard: comparación esperado vs real
- Modelo de referencia: golden reference para comprobaciones
- Modelado a nivel de transacción: abstracción de transacciones
- Clase scoreboard: implementación reutilizable

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module2.sh --common-patterns

# O manualmente
cd module2/examples/common_patterns
# Ejecutar como test de cocotb
```

**Salida esperada:**
```
     0.00ns INFO     cocotb.regression                  Running test_sequential_pattern (1/5)
Wrote 0x01, read 0x01
Wrote 0x02, read 0x02
Wrote 0x03, read 0x03
...
     0.00ns INFO     cocotb.regression                  test_sequential_pattern passed
```

**Conceptos clave:**
- Patrones secuenciales: predecibles y reproducibles
- Patrones aleatorios: usar `random.seed()` para reproducibilidad
- Scoreboard: rastrear esperado vs real
- Modelo de referencia: modelo software del comportamiento esperado
- Transacciones: abstracción de alto nivel
- Reutilización: crear componentes reutilizables de verificación

### Testbenches

#### Test: Registro simple (`module2/tests/cocotb_tests/test_simple_register.py`)

**Qué prueba:**
- Funcionalidad de reset del registro
- Operaciones de escritura en el registro
- Comportamiento del control `enable`
- Límites en 8 bits

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module2.sh --cocotb-tests

# O manualmente
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_simple_register
```

**Funciones de test:**
- `test_register_reset`: Verifica que el reset pone el registro a 0
- `test_register_write`: Prueba la operación básica de escritura
- `test_register_enable`: Prueba el control `enable`
- `test_register_all_values`: Prueba valores de límite (0x00, 0x01, 0x7F, 0x80, 0xFE, 0xFF)

#### Test: Registro desplazador (`module2/tests/cocotb_tests/test_shift_register.py`)

**Qué prueba:**
- Reset del registro desplazador
- Operación de shift serial
- Comportamiento del output serial

**Ejecución:**
```bash
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_shift_register
```

**Funciones de test:**
- `test_shift_register_reset`: Verifica que el reset limpia el registro
- `test_shift_register_operation`: Prueba el desplazamiento serial de entrada
- `test_shift_register_serial_out`: Prueba la salida serial

### Módulos Design Under Test (DUT)

#### Registro simple (`module2/dut/registers/simple_register.v`)
- **Propósito**: Registro básico de 8 bits con reloj, reset y enable
- **Usos**: Ejemplos de acceso a señales, generación de reloj, patrones de reset
- **Características**: Reset síncrono, control enable, datapath de 8 bits

#### Registro desplazador (`module2/dut/registers/shift_register.v`)
- **Propósito**: Registro de 8 bits serial-in, serial-out
- **Usos**: Testbench de registro desplazador
- **Características**: Entrada/salida serial, salida paralela, enable de shift

#### FIFO simple (`module2/dut/fifos/simple_fifo.v`)
- **Propósito**: FIFO de 16 entradas con punteros de lectura/escritura
- **Características**: Flags full/empty, ancho de datos 8 bits, operación síncrona
- **Nota**: Disponible para desarrollo futuro de testbenches

#### FSM simple (`module2/dut/state_machines/simple_fsm.v`)
- **Propósito**: Máquina de estados de 4 estados
- **Características**: Estados IDLE, START, WORK, DONE; señales start/done
- **Nota**: Disponible para desarrollo futuro de testbenches

## Ejercicios

1. **Gestión de relojes**
   - Crear relojes múltiples
   - Implementar gating de reloj
   - Sincronizar operaciones
   - **Ubicación**: Extender `module2/examples/clock_generation/clock_generation_example.py`
   - **Pista**: Crear dos relojes con periodos distintos y sincronizar operaciones entre ellos

2. **Operaciones con señales**
   - Leer y escribir señales
   - Manejar señales multibit
   - Trabajar con buses
   - **Ubicación**: Extender `module2/examples/signal_access/signal_access_example.py`
   - **Pista**: Probar con anchos de señal diferentes (1-bit, 8-bit, 16-bit, 32-bit)

3. **Patrones de triggers**
   - Usar varios triggers
   - Combinar triggers
   - Manejar timeouts
   - **Ubicación**: Extender `module2/examples/triggers/triggers_example.py`
   - **Pista**: Crear un mecanismo de timeout que cancele una operación si tarda demasiado

4. **Estructura de tests**
   - Organizar tests
   - Implementar fixtures
   - Manejar errores
   - **Ubicación**: Crear nuevo test en `module2/tests/cocotb_tests/`
   - **Pista**: Crear un fixture que configure reloj y reset para todos los tests

5. **Depuración**
   - Añadir logging
   - Generar formas de onda
   - Usar el depurador
   - **Ubicación**: Añadir a tests existentes
   - **Pista**: Usar `cocotb.log` para logging y habilitar generación de VCD en el Makefile

## Evaluación

- [ ] Entiende la arquitectura de cocotb
- [ ] Puede integrarse con simuladores
- [ ] Puede generar y gestionar relojes
- [ ] Puede acceder y conducir señales
- [ ] Puede usar triggers eficazmente
- [ ] Puede estructurar tests correctamente
- [ ] Puede implementar secuencias de reset
- [ ] Puede usar patrones comunes de verificación
- [ ] Puede depurar testbenches de cocotb
- [ ] Entiende la optimización de rendimiento

## Próximos pasos

Después de completar este módulo, procede a [Module 3: UVM Basics](MODULE3.md) para aprender la metodología UVM y la jerarquía de clases.

## Recursos adicionales

- **Documentación de cocotb**: https://docs.cocotb.org/
- **Ejemplos de cocotb**: https://github.com/cocotb/cocotb/tree/master/examples
- **cocotb Cookbook**: https://docs.cocotb.org/en/stable/cookbook.html
- **Documentación de Verilator**: https://verilator.org/

## Resolución de problemas

### Problemas comunes

**Problema: error "cocotb not found"**
```bash
# Solución: Instalar cocotb
./scripts/install_cocotb.sh --pip --venv .venv
# O
./scripts/module0.sh
```

**Problema: error "verilator not found"**
```bash
# Solución: Instalar Verilator
./scripts/install_verilator.sh --from-submodule
# O
./scripts/module0.sh
```

**Problema: errores en Makefile al ejecutar tests**
```bash
# Solución: Revisar rutas en Makefile e instalación de cocotb
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_simple_register
# Asegurar que la variable VERILOG_FILES es correcta
```

**Problema: errores de acceso a señales**
```bash
# Solución: Verificar que los nombres de señales coincidan con el módulo Verilog
# Usar: dut._discover_all() para listar señales disponibles
# O revisar: print(dut._name, dut._path)
```

**Problema: simulación colgada**
```bash
# Solución: Revisar bucles infinitos en corrutinas
# Asegurar que todas las corrutinas tienen condición de salida
# Usar timeouts: await First(trigger, Timer(timeout))
```

### Obtener ayuda

- Revisar comentarios en el código de ejemplo para explicaciones detalladas
- Revisar `module2/README.md` para estructura de directorios
- Ejecutar tests individualmente para aislar problemas: `make SIM=verilator TEST=test_name`
- Revisar logs de cocotb para mensajes detallados
- Usar `cocotb.log.set_level(cocotb.log.DEBUG)` para logging verboso
- Revisar todos los ejemplos en `module2/examples/` para patrones
- Revisar testbenches en `module2/tests/cocotb_tests/` para ejemplos completos

### Resumen de ejemplos y tests

**Ejemplos (archivos de test de cocotb en `module2/examples/`):**
1. **Ejemplo 2.1: Acceso a señales** (`signal_access/`) - Lectura/escritura de señales, tipos de valor
2. **Ejemplo 2.2: Generación de reloj** (`clock_generation/`) - Patrones de reloj, gating, división
3. **Ejemplo 2.3: Conducción de señales** - Demostrado en signal_access y reset_patterns
4. **Ejemplo 2.4: Triggers** (`triggers/`) - Triggers de flanco, timers, triggers combinados
5. **Ejemplo 2.5: Patrones de reset** (`reset_patterns/`) - Resets asíncronos/síncronos
6. **Ejemplo 2.6: Patrones comunes** (`common_patterns/`) - Scoreboard, modelos de referencia, transacciones

**Testbenches (tests ejecutables en `module2/tests/cocotb_tests/`):**
1. **Test de registro simple** (`test_simple_register.py`) - 4 funciones de test cubriendo reset, escritura, enable, límites
2. **Test de registro desplazador** (`test_shift_register.py`) - 3 funciones de test cubriendo reset, operación de shift, salida serial

**DUTs (en `module2/dut/`):**
1. **Registro simple** (`registers/simple_register.v`) - Usado en ejemplos y tests
2. **Registro desplazador** (`registers/shift_register.v`) - Usado en tests de shift register
3. **FIFO simple** (`fifos/simple_fifo.v`) - Disponible para pruebas futuras
4. **FSM simple** (`state_machines/simple_fsm.v`) - Disponible para pruebas futuras

**Cobertura:**
- ✅ Acceso y conducción de señales
- ✅ Generación y gestión de relojes
- ✅ Uso de triggers
- ✅ Patrones de reset
- ✅ Patrones comunes de verificación
- ✅ Estructura de tests y organización
- ✅ Testbenches completos con aserciones
