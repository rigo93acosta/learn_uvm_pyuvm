# Módulo 2: fundamentos de cocotb

**Objetivo**: Dominar cocotb para la verificación de hardware

## Resumen

Este módulo ofrece una cobertura completa de cocotb, el framework de testbench basado en corrutinas que permite testbenches en Python para diseños de hardware. Aprenderás a interactuar con simuladores, impulsar señales, muestrear valores y crear testbenches robustos.

> **📖 Concepto fundamental**: Antes de profundizar, asegúrate de entender [Cómo interactúan Python y Verilog](PYTHON_VERILOG_INTERACTION.md). Este documento explica la arquitectura de dos capas, el flujo de señales, la sincronización temporal y cómo cocotb conecta los testbenches Python con los diseños Verilog.

### Ejemplos y estructura del código

Este módulo incluye ejemplos y testbenches ubicados en el directorio `module2/`:

```
module2/
├── examples/              # ejemplos de cocotb para cada tema
│   ├── signal_access/     # lectura y escritura de señales
│   ├── clock_generation/  # patrones de generación de reloj
│   ├── triggers/          # ejemplos de uso de triggers
│   ├── reset_patterns/    # secuencias de reset
│   └── common_patterns/   # patrones de verificación comunes
├── dut/                   # módulos Verilog del DUT
│   ├── registers/         # módulos de registros
│   ├── fifos/             # módulos FIFO
│   └── state_machines/    # módulos de máquinas de estado
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
# Activar entorno virtual (si usas uno)
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
  - Capa de interfaz del simulador
  - Interacción con el DUT
  - Programación de eventos

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
  - Características específicas del simulador

- **Proceso de compilación**
  - Compilación de Verilog
  - Compilación de la librería cocotb
  - Proceso de enlace
  - Estructura del Makefile

### 3. Generación y gestión de relojes

- **Generación de reloj**
  - Uso de la clase `Clock`
  - Parámetros del reloj (periodo, unidades)
  - Inicio de relojes
  - Múltiples relojes

- **Patrones de reloj**
  - Relojes regulares
  - Relojes con gating
  - División de reloj
  - Parada del reloj

- **Gestión de dominios de reloj**
  - Múltiples dominios de reloj
  - Crossing entre dominios
  - Sincronización entre dominios

### 4. Acceso y conducción de señales

- **Handles de señal**
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
  - Asignación por entero
  - Asignación por cadena binaria
  - Alta impedancia (Z) y desconocido (X)

- **Tipos de señales**
  - Señales de 1 bit
  - Señales multi-bit (vectores)
  - Buses y arreglos
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
  - `First(*triggers)` (el primero en ocurrir)

- **Ejecución de corrutinas**
  - Definición de corrutinas
  - Inicio de corrutinas
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
  - Parámetro DUT
  - Organización de tests

- **Fases del test**
  - Fase de configuración
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
  - Verificación de reset

- **Patrones de inicialización**
  - Inicialización de señales
  - Inicialización de estados
  - Configuración
  - Condiciones iniciales

### 8. Patrones comunes de verificación

- **Generación de estímulos**
  - Patrones secuenciales
  - Patrones aleatorios
  - Aleatoriedad condicionada
  - Estímulos basados en archivos

- **Comprobación de respuestas**
  - Comprobación inmediata
  - Comprobación diferida
  - Comparación con modelo de referencia
  - Patrones de scoreboard

- **Modelado a nivel de transacciones**
  - Clases de transacción
  - Generación de transacciones
  - Ejecución de transacciones
  - Comprobación de transacciones

**Ver Ejemplo 2.6**: Patrones comunes de verificación (`module2/examples/common_patterns/common_patterns_example.py`) para implementación detallada.

### 9. Depuración con cocotb

- **Logging y reporting**
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
  - Puntos de interrupción
  - Inspección de variables
  - Depuración paso a paso

- **Problemas comunes**
  - Errores de acceso a señales
  - Problemas de temporización
  - Bloqueos en la simulación
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
  - Convenciones de nombres de tests
  - Agrupación de tests
  - Ejecución de tests

## Resultados de aprendizaje

Al final de este módulo deberías ser capaz de:

- Entender la arquitectura de cocotb
- Integrar cocotb con simuladores
- Generar y gestionar relojes
- Acceder y conducir señales
- Usar triggers de forma efectiva
- Estructurar tests correctamente
- Implementar secuencias de reset
- Usar patrones comunes de verificación
- Depurar testbenches de cocotb
- Optimizar el rendimiento de los testbenches

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
- **Lectura de valores**: Leer valores de señal con la propiedad `.value`
- **Tipos de valor**: Representaciones entero, binaria y hex
- **Propiedades de la señal**: Ancho, nombre, ruta
- **Asignaciones de valor**: Diferentes formas de asignar valores (entero, BinaryValue)

**Ejecución:**
```bash
# Usando el script orquestador (ejecuta tests)
./scripts/module2.sh --signal-access

# O manualmente con cocotb
cd module2/examples/signal_access
# Nota: estos son archivos de test de cocotb, requieren configuración adecuada del Makefile
# O se usan en tu propio testbench
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
- **`dut.signal_name`**: Acceder señales del DUT
- **`.value`**: Obtener/establecer el valor de la señal
- **`.value.integer`**: Obtener la representación entera
- **`.value.binstr`**: Obtener la representación binaria como cadena
- **`BinaryValue`**: Crear valores desde cadenas binarias
- **Ancho de señal**: Usar `len(dut.signal)` para obtener el ancho

### Caso de prueba 2.2: Generación de reloj
**Objetivo**: Generar y gestionar relojes

**Temas**:
- Clase Clock
- Inicio de relojes
- Múltiples relojes

#### Ejemplo 2.2: Generación de reloj (`module2/examples/clock_generation/clock_generation_example.py`)

**Lo que demuestra:**
- **Clase Clock**: Uso de `Clock(dut.clk, period, units)` para crear relojes
- **Inicio de relojes**: Uso de `cocotb.start_soon(clock.start())` para ejecutar relojes en segundo plano
- **Múltiples relojes**: Crear y gestionar múltiples dominios de reloj
- **Gating de reloj**: Implementar habilitación/deshabilitación de reloj
- **División de reloj**: Crear señales de reloj divididas
- **Parada de reloj**: Detener la generación del reloj

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
- **`Clock(signal, period, units)`**: Crear objeto de reloj
- **`clock.start()`**: Iniciar la generación del reloj (devuelve una corrutina)
- **`cocotb.start_soon()`**: Ejecutar una corrutina en segundo plano
- **Múltiples relojes**: Cada reloj corre independientemente
- **Gating de reloj**: Controlar el reloj con señales de enable
- **División de reloj**: Dividir la frecuencia contando flancos

### Caso de prueba 2.3: Conducción de señales
**Objetivo**: Conducir señales con valores

**Temas**:
- Asignación de valores
- Control temporal
- Actualizaciones de señales

#### Ejemplo 2.3: Conducción de señales

**Lo que demuestra:**
La conducción de señales se demuestra a lo largo de los ejemplos, particularmente en:
- **Signal Access Example**: Muestra lectura y escritura de señales
- **Reset Patterns Example**: Demuestra conducción de señales de reset
- **Common Patterns Example**: Muestra conducción de señales de datos con temporización

**Conceptos clave:**
- **Asignación directa**: `dut.signal.value = value`
- **Asignación por entero**: `dut.signal.value = 0xAB`
- **Asignación binaria**: `dut.signal.value = BinaryValue("10101010")`
- **Asignación en hex**: `dut.signal.value = 0xAB` (igual que entero)
- **Control temporal**: Usar `await Timer()` o `await RisingEdge()` antes de leer valores conducidos
- **Trigger ReadOnly**: Esperar `ReadOnly()` para asegurar que la señal esté estable después de la asignación
- **Actualizaciones de señales**: Las señales se actualizan en el siguiente paso de simulación

**Patrón de ejemplo:**
```python
# Conducir señal
dut.data.value = 0xAB

# Esperar a que la señal se propague
await RisingEdge(dut.clk)
await Timer(1, units="ns")  # Pequeño retraso para lógica combinacional

# Leer de vuelta
assert dut.output.value.integer == expected_value
```

**Ver también:**
- Conducción de señales en `module2/examples/signal_access/signal_access_example.py`
- Conducción de reset en `module2/examples/reset_patterns/reset_patterns_example.py`
- Conducción de datos en `module2/examples/common_patterns/common_patterns_example.py`

### Caso de prueba 2.4: Uso de triggers
**Objetivo**: Usar diversos triggers

**Temas**:
- Triggers por flanco
- Triggers temporales
- Triggers combinados

#### Ejemplo 2.4: Triggers (`module2/examples/triggers/triggers_example.py`)

**Lo que demuestra:**
- **Triggers por flanco**: `RisingEdge()`, `FallingEdge()`, `Edge()`
- **Triggers temporales**: `Timer(time, units)` para retrasos basados en tiempo
- **Trigger ReadOnly**: `ReadOnly()` espera el fin del paso de tiempo
- **Trigger ReadWrite**: `ReadWrite()` para durante el paso de tiempo
- **Trigger Combine**: `Combine(*triggers)` espera que ocurran todos los triggers
- **Trigger First**: `First(*triggers)` espera el primero que ocurra
- **Manejo de timeouts**: Uso de triggers con timeout
- **Corrutinas en paralelo**: Múltiples corrutinas con diferentes triggers

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
- **`RisingEdge(signal)`**: Esperar transición 0→1
- **`FallingEdge(signal)`**: Esperar transición 1→0
- **`Edge(signal)`**: Esperar cualquier flanco
- **`Timer(time, units)`**: Esperar tiempo especificado
- **`ReadOnly()`**: Esperar fin del paso de tiempo (señales estables)
- **`Combine(*triggers)`**: Esperar a que todos los triggers ocurran
- **`First(*triggers)`**: Esperar al primer trigger que ocurra
- **Ejecución en paralelo**: Varias corrutinas pueden esperar triggers distintos

### Caso de prueba 2.5: Secuencia de reset
**Objetivo**: Implementar secuencia de reset

**Temas**:
- Patrones de reset
- Verificación de reset
- Inicialización

#### Ejemplo 2.5: Patrones de reset (`module2/examples/reset_patterns/reset_patterns_example.py`)

**Lo que demuestra:**
- **Reset asíncrono**: Secuencia de reset asíncrona con temporización
- **Reset síncrono**: Reset síncrono sincronizado con el reloj
- **Verificación de reset**: Comprobar que el reset coloca el DUT en un estado conocido
- **Temporización de reset**: Asserción y deassertión del reset con tiempos adecuados
- **Inicialización**: Configurar señales tras el reset
- **Reset en operación**: Probar reset mientras el DUT está en operación

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
- **Reset asíncrono**: Aserta reset, esperar duración, desasertar reset
- **Reset síncrono**: Aserta reset, esperar ciclos de reloj, desasertar en flanco de reloj
- **Verificación de reset**: Siempre comprobar que el reset pone el DUT en estado conocido
- **Temporización de reset**: La temporización adecuada asegura propagación del reset
- **Inicialización**: Configurar señales de control tras completar el reset
- **Patrones de reset**: Crear funciones reutilizables de reset para diferentes tipos

#### Ejemplo 2.6: Patrones comunes de verificación (`module2/examples/common_patterns/common_patterns_example.py`)

**Lo que demuestra:**
- **Patrones secuenciales**: Generación de estímulos determinística y reproducible
- **Patrones aleatorios**: Estímulos aleatorios con control de semilla
- **Scoreboard**: Comparación esperado vs real
- **Modelo de referencia**: Golden reference para comprobaciones
- **Modelado a nivel de transacciones**: Abstracción de transacciones a alto nivel
- **Clase Scoreboard**: Implementación reutilizable de scoreboard

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
- **Patrones secuenciales**: Predecibles y repetibles
- **Patrones aleatorios**: Usar `random.seed()` para reproducibilidad
- **Scoreboard**: Rastrear esperado vs real para verificación
- **Modelo de referencia**: Modelo software del comportamiento esperado
- **Transacciones**: Abstracción de alto nivel para operaciones
- **Reutilización de patrones**: Crear componentes de verificación reutilizables

### Testbenches

#### Test: Registro simple (`module2/tests/cocotb_tests/test_simple_register.py`)

**Qué prueba:**
- Funcionalidad de reset del registro
- Operaciones de escritura en el registro
- Comportamiento del control enable
- Todos los límites de valores de 8 bits

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
- `test_register_write`: Testea la operación básica de escritura
- `test_register_enable`: Testea el control enable
- `test_register_all_values`: Testea valores límite (0x00, 0x01, 0x7F, 0x80, 0xFE, 0xFF)

#### Test: Registro de corrimiento (`module2/tests/cocotb_tests/test_shift_register.py`)

**Qué prueba:**
- Reset del registro de corrimiento
- Operación de desplazamiento serial
- Comportamiento de salida serial

**Ejecución:**
```bash
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_shift_register
```

**Funciones de test:**
- `test_shift_register_reset`: Verifica que el reset borra el registro
- `test_shift_register_operation`: Testea la entrada serial y el desplazamiento
- `test_shift_register_serial_out`: Testea la salida serial del registro

### Módulos Design Under Test (DUT)

#### Registro simple (`module2/dut/registers/simple_register.v`)
- **Propósito**: Registro básico de 8 bits con reloj, reset y enable
- **Usado en**: Ejemplos de acceso a señales, generación de reloj, ejemplos de reset
- **Características**: Reset síncrono, control enable, camino de datos de 8 bits

#### Registro de corrimiento (`module2/dut/registers/shift_register.v`)
- **Propósito**: Registro de corrimiento serial-in, serial-out de 8 bits
- **Usado en**: Testbench de registro de corrimiento
- **Características**: Entrada/salida serial, salida/paralela, enable de desplazamiento

#### FIFO simple (`module2/dut/fifos/simple_fifo.v`)
- **Propósito**: FIFO de 16 entradas con punteros de lectura/escritura
- **Características**: Flags full/empty, ancho de datos 8 bits, operación síncrona
- **Nota**: Disponible para desarrollo de testbenches futuros

#### FSM simple (`module2/dut/state_machines/simple_fsm.v`)
- **Propósito**: Máquina de estados de 4 estados
- **Características**: IDLE, START, WORK, DONE, señales start/done
- **Nota**: Disponible para desarrollo de testbenches futuros

## Ejercicios

1. **Gestión de relojes**
   - Crear múltiples relojes
   - Implementar gating de reloj
   - Sincronizar operaciones
   - **Ubicación**: Extender `module2/examples/clock_generation/clock_generation_example.py`
   - **Pista**: Crear dos relojes con periodos distintos y sincronizar operaciones entre ellos

2. **Operaciones de señal**
   - Leer y escribir señales
   - Manejar señales multi-bit
   - Trabajar con buses
   - **Ubicación**: Extender `module2/examples/signal_access/signal_access_example.py`
   - **Pista**: Probar con distintos anchos de señal (1-bit, 8-bit, 16-bit, 32-bit)

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
   - **Pista**: Crear una fixture que prepare reloj y reset para todos los tests

5. **Depuración**
   - Añadir logging
   - Generar formas de onda
   - Usar el depurador
   - **Ubicación**: Añadir a tests existentes
   - **Pista**: Usar `cocotb.log` para logging y activar generación VCD en el Makefile

## Evaluación

- [ ] Entiende la arquitectura de cocotb
- [ ] Puede integrar con simuladores
- [ ] Puede generar y gestionar relojes
- [ ] Puede acceder y conducir señales
- [ ] Puede usar triggers de forma efectiva
- [ ] Puede estructurar tests correctamente
- [ ] Puede implementar secuencias de reset
- [ ] Puede usar patrones comunes de verificación
- [ ] Puede depurar testbenches de cocotb
- [ ] Entiende la optimización de rendimiento

## Próximos pasos

Tras completar este módulo, procede a [Módulo 3: Fundamentos de UVM](MODULE3.md) para aprender la metodología UVM y la jerarquía de clases.

## Recursos adicionales

- **Documentación de cocotb**: https://docs.cocotb.org/
- **Ejemplos de cocotb**: https://github.com/cocotb/cocotb/tree/master/examples
- **Cookbook de cocotb**: https://docs.cocotb.org/en/stable/cookbook.html
- **Documentación de Verilator**: https://verilator.org/

## Solución de problemas

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
# Solución: Revisar rutas del Makefile y la instalación de cocotb
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_simple_register
# Asegurarse de que la ruta VERILOG_FILES sea correcta
```

**Problema: errores de acceso a señales**
```bash
# Solución: Verificar que los nombres de señales coincidan con el módulo Verilog
# Usar: dut._discover_all() para ver todas las señales disponibles
# O revisar: print(dut._name, dut._path)
```

**Problema: simulación colgada**
```bash
# Solución: Revisar bucles infinitos en corrutinas
# Asegurarse de que todas las corrutinas tengan condiciones de salida
# Usar timeouts: await First(trigger, Timer(timeout))
```

### Obtener ayuda

- Revisar los comentarios en el código de ejemplo para explicaciones detalladas
- Revisar `module2/README.md` para la estructura del directorio
- Ejecutar tests individualmente para aislar problemas: `make SIM=verilator TEST=test_name`
- Revisar logs de cocotb para mensajes de error detallados
- Usar `cocotb.log.set_level(cocotb.log.DEBUG)` para logging detallado
- Revisar todos los ejemplos en `module2/examples/` para patrones
- Revisar testbenches en `module2/tests/cocotb_tests/` para ejemplos completos

### Resumen de ejemplos y tests

**Ejemplos (archivos de test de cocotb en `module2/examples/`):**
1. **Ejemplo 2.1: Acceso a señales** (`signal_access/`) - Lectura/escritura de señales, tipos de valor
2. **Ejemplo 2.2: Generación de reloj** (`clock_generation/`) - Patrones de reloj, gating, división
3. **Ejemplo 2.3: Conducción de señales** - Demostrado en signal_access y reset_patterns
4. **Ejemplo 2.4: Triggers** (`triggers/`) - Triggers por flanco, timers, triggers combinados
5. **Ejemplo 2.5: Patrones de reset** (`reset_patterns/`) - Reset asíncrono/síncrono
6. **Ejemplo 2.6: Patrones comunes** (`common_patterns/`) - Scoreboard, modelo de referencia, transacciones

**Testbenches (tests ejecutables en `module2/tests/cocotb_tests/`):**
1. **Test registro simple** (`test_simple_register.py`) - 4 funciones de test: reset, escritura, enable, límites
2. **Test registro de corrimiento** (`test_shift_register.py`) - 3 funciones de test: reset, operación de desplazamiento, salida serial

**Módulos DUT (en `module2/dut/`):**
1. **Registro simple** (`registers/simple_register.v`) - Usado en ejemplos y tests
2. **Registro de corrimiento** (`registers/shift_register.v`) - Usado en test de shift register
3. **FIFO simple** (`fifos/simple_fifo.v`) - Disponible para tests futuros
4. **FSM simple** (`state_machines/simple_fsm.v`) - Disponible para tests futuros

**Cobertura:**
- ✅ Acceso y conducción de señales
- ✅ Generación y gestión de relojes
- ✅ Uso de triggers
- ✅ Patrones de reset
- ✅ Patrones comunes de verificación
- ✅ Estructura y organización de tests
- ✅ Testbenches completos con aserciones
