# Módulo 1: Fundamentos de Python y Verificación

**Objetivo**: Comprender Python para verificación y los fundamentos de verificación

## Resumen

Este módulo establece las bases para el trabajo de verificación. Aprenderás conceptos esenciales de Python utilizados en verificación y comprenderás los principios fundamentales de la verificación de hardware.

### Ejemplos y Estructura de Código

Este módulo incluye ejemplos completos y testbenches ubicados en el directorio `module1/`:

```
module1/
├── examples/              # Ejemplos de Python para cada tema
│   ├── python_basics/     # Clases, herencia, POO
│   ├── decorators/        # Decoradores y context managers
│   ├── async_await/       # Patrones async/await
│   ├── data_structures/   # Estructuras de datos para verificación
│   └── error_handling/   # Manejo de excepciones y logging
├── dut/                   # Módulos Verilog Design Under Test
│   └── simple_gates/      # Compuertas básicas (AND, Contador)
├── tests/                 # Testbenches
│   ├── cocotb_tests/     # Testbenches cocotb
│   └── pyuvm_tests/      # Testbenches pyuvm
└── README.md             # Documentación del Módulo 1
```

### Inicio Rápido

**Ejecutar todos los ejemplos usando el script orquestador:**

```bash
# Ejecutar todos los ejemplos de Python
./scripts/module1.sh

# Ejecutar ejemplos específicos
./scripts/module1.sh --python-basics
./scripts/module1.sh --decorators
./scripts/module1.sh --async-await
./scripts/module1.sh --data-structures
./scripts/module1.sh --error-handling

# Ejecutar pruebas
./scripts/module1.sh --cocotb-tests
./scripts/module1.sh --pyuvm-tests

# Ejecutar todo
./scripts/module1.sh --all-python --all-tests
```

**Ejecutar ejemplos individualmente:**

```bash
# Activar entorno virtual (si usas uno)
source .venv/bin/activate

# Ejecutar ejemplos de Python directamente
python3 module1/examples/python_basics/transaction.py
python3 module1/examples/decorators/decorators_example.py
python3 module1/examples/async_await/async_example.py
python3 module1/examples/data_structures/data_structures_example.py
python3 module1/examples/error_handling/error_handling_example.py

# Ejecutar pruebas cocotb
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_and_gate
make SIM=verilator TEST=test_counter
```

## Temas Cubiertos

### 1. Clases y Herencia en Python para Verificación

- **Conceptos Básicos de Programación Orientada a Objetos**
  - Clases y objetos
  - Variables de instancia y métodos
  - Variables y métodos de clase
  - Conceptos de encapsulación

- **Herencia en Python**
  - Herencia simple
  - Herencia múltiple (MRO)
  - Sobrescritura de métodos
  - Uso de la función `super()`

- **Métodos Especiales (Métodos Dunder)**
  - `__init__()` para inicialización
  - `__str__()` y `__repr__()` para representación como cadena
  - `__eq__()` para comparación de igualdad
  - `__hash__()` para objetos hasheables

- **Patrones de Diseño de Clases para Verificación**
  - Conceptos básicos del patrón Factory
  - Patrón Singleton
  - Patrón Builder
  - Patrón Strategy

#### Ejemplo 1.1: Clases de Transacción (`module1/examples/python_basics/transaction.py`)

**Qué demuestra:**

- Clase base `Transaction` con variables de clase (`_id_counter`)
- Variables de instancia (`id`, `data`, `timestamp`)
- Métodos especiales: `__init__()`, `__str__()`, `__repr__()`, `__eq__()`, `__hash__()`
- Herencia: `ReadTransaction` y `WriteTransaction` heredan de `Transaction`
- Sobrescritura de métodos: Las clases hijas sobrescriben el método `__str__()`
- Uso de `super()` para llamar a métodos de la clase padre

**Ejecución:**

```bash
# Usando script orquestador
./scripts/module1.sh --python-basics

# O directamente
python3 module1/examples/python_basics/transaction.py
```

**Salida Esperada:**

```
============================================================
Module 1 Example 1.1: Python Class Basics
============================================================

1. Creating base transaction:
   Transaction(id=1, data=4660, timestamp=0)
   Transaction ID: 1

2. Creating read transaction (inheritance):
   ReadTransaction(id=2, address=0x1000, data=0xDEAD)
   Address: 0x1000

3. Creating write transaction (inheritance):
   WriteTransaction(id=3, address=0x2000, data=0xBEEF)
   Address: 0x2000

4. Testing equality:
   txn1 == txn2: True
   txn1 == read_txn: False

5. Using transactions in a set (requires __hash__):
   Set size: 3
   - Transaction(id=1, data=4660, timestamp=0)
   - ReadTransaction(id=2, address=0x1000, data=0xDEAD)
   - WriteTransaction(id=3, address=0x2000, data=0xBEEF)

============================================================
Example completed successfully!
============================================================
```

**Conceptos Clave:**

- **Variables de Clase**: `_id_counter` se comparte entre todas las instancias
- **Variables de Instancia**: Cada transacción tiene su propio `id`, `data`, `timestamp`
- **Métodos Especiales**: Permiten comportamiento Pythonic (representación como cadena, igualdad, hashing)
- **Herencia**: `ReadTransaction` y `WriteTransaction` extienden la funcionalidad base
- **Sobrescritura de Métodos**: Las clases hijas personalizan la representación como cadena

### 2. Decoradores y Context Managers

- **Decoradores de Python**
  - Decoradores de funciones
  - Decoradores de clases
  - Sintaxis y uso de decoradores
  - Decoradores comunes (`@property`, `@staticmethod`, `@classmethod`)

- **Context Managers**
  - Sentencia `with`
  - Métodos `__enter__()` y `__exit__()`
  - Protocolo de context manager
  - Utilidades de `contextlib`

- **Decoradores Específicos de Verificación**
  - Decoradores de cocotb (`@cocotb.test()`, `@cocotb.coroutine`)
  - Decoradores personalizados para verificación
  - Decoradores de temporización

#### Ejemplo 1.2: Decoradores y Context Managers (`module1/examples/decorators/decorators_example.py`)

**Qué demuestra:**

- **Decoradores de Función**: `@timing_decorator` y `@log_calls_decorator` envuelven funciones
- **Apilamiento de Decoradores**: Múltiples decoradores pueden aplicarse a la misma función
- **Context Manager con Clase**: `VerificationContext` implementa `__enter__()` y `__exit__()`
- **Context Manager basado en Función**: `simulation_phase()` usando `@contextmanager`
- **Context Managers Anidados**: Usando múltiples context managers juntos
- **Integración con Logging**: Decoradores y context managers usan el módulo logging de Python

**Ejecución:**

```bash
# Usando script orquestador
./scripts/module1.sh --decorators

# O directamente
python3 module1/examples/decorators/decorators_example.py
```

**Salida Esperada:**

```
============================================================
Module 1 Example 1.2: Decorators and Context Managers
============================================================

1. Using function decorators:
2024-01-04 10:00:00 - __main__ - INFO - Calling setup with args=(), kwargs={}
2024-01-04 10:00:00 - __main__ - INFO - Setting up test environment
2024-01-04 10:00:00 - __main__ - INFO - setup returned: None
2024-01-04 10:00:00 - __main__ - INFO - setup took 0.1000 seconds
...

2. Using context manager (class-based):
2024-01-04 10:00:01 - __main__ - INFO - Entering verification context: test_context
   Elapsed time: 0.1000s
2024-01-04 10:00:01 - __main__ - INFO - Exiting verification context: test_context (success, 0.1000s)

3. Using context manager (function-based):
2024-01-04 10:00:02 - __main__ - INFO - Starting simulation phase: reset_phase
2024-01-04 10:00:02 - __main__ - INFO -    Performing reset operations
2024-01-04 10:00:02 - __main__ - INFO - Completed simulation phase: reset_phase (0.0500s)
...

============================================================
Example completed successfully!
============================================================
```

**Conceptos Clave:**

- **Decoradores**: Funciones que modifican otras funciones sin cambiar su código
- **`functools.wraps`**: Preserva los metadatos de la función al decorar
- **Context Managers**: Aseguran la limpieza adecuada de recursos usando sentencias `with`
- **Manejo de Excepciones**: Los context managers pueden manejar excepciones en `__exit__()`
- **Logging**: Integración con el módulo logging de Python para flujos de trabajo de verificación

### 3. Async/Await para Simulación

- **Conceptos de Programación Asíncrona**
  - Corrutinas vs funciones
  - Conceptos básicos del event loop
  - Concurrencia vs paralelismo

- **`async` y `await` en Python**
  - Definición de funciones async
  - Await de corrutinas
  - Context managers asíncronos
  - Iteradores asíncronos

- **Corrutinas de cocotb**
  - Concepto de corrutina en cocotb
  - `await` para tiempo de simulación
  - Objetos Trigger
  - Planificación de corrutinas

- **Patrones Comunes**
  - Corrutinas paralelas
  - Ejecución secuencial
  - Manejo de timeout
  - Manejo de excepciones en código asíncrono

#### Ejemplo 1.3: Patrones Async/Await (`module1/examples/async_await/async_example.py`)

**Qué demuestra:**

- **Funciones Async**: Definición de corrutinas con `async def`
- **Operaciones Await**: Usando `await` para esperar operaciones asíncronas
- **Generación de Reloj**: Simulación de señales de reloj con funciones async
- **Ejecución Paralela**: Ejecutando múltiples corrutinas concurrentemente con `asyncio.gather()`
- **Ejecución Secuencial**: Ejecutando corrutinas una tras otra
- **Manejo de Timeout**: Usando `asyncio.wait_for()` con timeout
- **Manejo de Excepciones**: Capturando excepciones en código asíncrono
- **Colas**: Usando `asyncio.Queue` para comunicación entre corrutinas

**Ejecución:**

```bash
# Usando script orquestador
./scripts/module1.sh --async-await

# O directamente
python3 module1/examples/async_await/async_example.py
```

**Salida Esperada:**

```
============================================================
Module 1 Example 1.3: Async/Await for Simulation
============================================================

1. Sequential execution:
Running sequential execution example...
Final result: Step 1 complete, Step 2 complete, Step 3 complete

2. Parallel tasks:
Running parallel tasks example...
Results collected: [0, 2, 4, 6, 8]

3. Timeout handling:
Running timeout example...
Operation timed out!

4. Exception handling:
Running exception handling example...
Caught exception: Simulated error

============================================================
Example completed successfully!
============================================================
```

**Conceptos Clave:**

- **Corrutinas**: Funciones definidas con `async def` que pueden pausarse y reanudarse
- **Event Loop**: `asyncio.run()` crea y gestiona el event loop
- **Concurrencia**: Múltiples corrutinas pueden ejecutarse concurrentemente (no en paralelo)
- **`asyncio.gather()`**: Ejecuta múltiples corrutinas concurrentemente y espera a todas
- **`asyncio.wait_for()`**: Agrega timeout a la ejecución de corrutinas
- **Colas Async**: `asyncio.Queue` para comunicación segura entre corrutinas
- **Tiempo de Simulación**: En cocotb, `await Timer()` avanza el tiempo de simulación

### 4. Fundamentos de Verificación

- **¿Qué es Verificación?**
  - Diseño vs verificación
  - Objetivos de verificación
  - Métricas de verificación
  - Ciclo de vida de verificación

- **Arquitectura de Testbench**
  - Componentes del testbench
  - Generación de estímulos
  - Verificación de respuestas
  - Recolección de cobertura

- **Niveles de Verificación**
  - Verificación a nivel de unidad
  - Verificación a nivel de bloque
  - Verificación a nivel de sistema
  - Verificación a nivel de SoC

### 5. Conceptos Básicos de Arquitectura de Testbench

- **Estructura del Testbench**
  - Design Under Test (DUT)
  - Componentes del testbench
  - Definición de interfaz
  - Generación de reloj y reset

- **Generación de Estímulos**
  - Estímulo determinista
  - Estímulo aleatorio
  - Aleatorio restringido
  - Pruebas dirigidas

- **Verificación de Respuestas**
  - Testbenches autoverificables
  - Modelos de referencia
  - Scoreboards
  - Aserciones

### 6. Flujo de Simulación

- **Fases de Simulación**
  - Inicialización
  - Fase de reset
  - Ejecución de prueba
  - Fase de limpieza

- **Gestión del Tiempo**
  - Tiempo de simulación vs tiempo real
  - Unidades de tiempo (ns, ps, etc.)
  - Ciclos de reloj
  - Relaciones temporales

- **Simulación Basada en Eventos**
  - Planificación de eventos
  - Ciclos delta
  - Actualizaciones de señales
  - Condiciones de trigger

### 7. Introducción a Aserciones

- **¿Qué son las Aserciones?**
  - Aserciones inmediatas
  - Aserciones concurrentes
  - Tipos de aserciones

- **Aserciones Básicas**
  - Verificaciones de propiedades simples
  - Aserciones de valor de señal
  - Aserciones de temporización

- **Mejores Prácticas de Aserciones**
  - Cuándo usar aserciones
  - Ubicación de aserciones
  - Mensajes de aserción
  - Cobertura de aserciones

### 8. Frameworks de Pruebas Python (Visión General)

- **Conceptos Básicos de pytest**
  - Descubrimiento de pruebas
  - Fixtures
  - Parametrización
  - Markers

- **Conceptos de Pruebas Unitarias**
  - Organización de pruebas
  - Aislamiento de pruebas
  - Mocking y stubbing
  - Cobertura de pruebas

- **Integración con Verificación**
  - Usando pytest con cocotb
  - Patrones de organización de pruebas
  - Reporte y logging

### 9. Estructuras de Datos para Verificación

- **Listas y Diccionarios**
  - Operaciones comunes
  - Comprensión de listas
  - Comprensión de diccionarios
  - Estructuras anidadas

- **Módulo Collections**
  - `deque` para colas
  - `defaultdict` para valores por defecto
  - `Counter` para conteo
  - `namedtuple` para datos estructurados

- **Estructuras Específicas de Verificación**
  - Colas de transacciones
  - Estructuras de datos de scoreboard
  - Estructuras de datos de cobertura

#### Ejemplo 1.4: Estructuras de Datos (`module1/examples/data_structures/data_structures_example.py`)

**Qué demuestra:**

- **`deque`**: Cola doblemente terminada para operaciones FIFO/LIFO en `TransactionQueue`
- **`defaultdict`**: Diccionario con valores por defecto para scoreboard
- **`Counter`**: Conteo de ocurrencias para estadísticas
- **`namedtuple`**: Datos estructurados para transacciones
- **Comprensión de Listas**: Creación de listas a partir de iterables
- **Comprensión de Diccionarios**: Creación de diccionarios a partir de iterables
- **Patrón Scoreboard**: Comparación de resultados esperados vs reales
- **Recolección de Cobertura**: Seguimiento de bins de cobertura y conteos de aciertos

**Ejecución:**

```bash
# Usando script orquestador
./scripts/module1.sh --data-structures

# O directamente
python3 module1/examples/data_structures/data_structures_example.py
```

**Salida Esperada:**

```
============================================================
Module 1: Data Structures for Verification
============================================================

1. Transaction Queue (deque):
   Queue size: 5
   Popped: id=1, addr=0x1000, data=0x0
   Popped: id=2, addr=0x1001, data=0x2
   ...

2. Scoreboard (defaultdict, Counter):
   Matches: 5
   Mismatches: 0
   Unexpected: 2
   Mismatch details: []

3. Coverage Collector (set, Counter):
   address: 80.0% coverage
      Unique values: 8
      Total hits: 8
   data: 70.0% coverage
      Unique values: 7
      Total hits: 7
   ...

4. List Comprehensions:
   Created 10 transactions
   First transaction: Transaction(id=0, addr=4096, data=0, timestamp=0)

5. Dictionary Comprehensions:
   Created address map with 10 entries
   Sample: {4096: 0, 4097: 2, 4098: 4}

============================================================
Example completed successfully!
============================================================
```

**Conceptos Clave:**

- **`deque`**: Operaciones FIFO/LIFO eficientes, seguro para código asíncrono
- **`defaultdict`**: Crea automáticamente valores por defecto para claves faltantes
- **`Counter`**: Diccionario especializado para contar ocurrencias
- **`namedtuple`**: Alternativa ligera a clases para estructuras de datos simples
- **Comprensiones**: Forma Pythonic de crear listas/diccionarios a partir de iterables
- **Scoreboard**: Patrón común de verificación para verificar resultados
- **Cobertura**: Seguimiento de qué valores/condiciones han sido probados

### 10. Manejo de Errores y Logging

- **Manejo de Excepciones**
  - Bloques Try/except
  - Tipos de excepción
  - Excepciones personalizadas
  - Encadenamiento de excepciones

- **Logging en Python**
  - Conceptos básicos del módulo `logging`
  - Niveles de log
  - Formateo de log
  - Handlers de log

- **Logging de Verificación**
  - Reporte UVM (vista previa)
  - Patrones de logging en testbench
  - Logging de depuración
  - Análisis de logs

#### Ejemplo 1.5: Manejo de Errores y Logging (`module1/examples/error_handling/error_handling_example.py`)

**Qué demuestra:**

- **Excepciones Personalizadas**: `VerificationError`, `MismatchError`, `TimeoutError`
- **Manejo de Excepciones**: Bloques Try/except con tipos de excepción específicos
- **Encadenamiento de Excepciones**: Usando `raise ... from ...` para encadenar excepciones
- **Lógica de Reintento**: Implementación de mecanismos de reintento con manejo de errores
- **Niveles de Logging**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Handlers de Log**: Handlers de archivo y consola
- **Formateo de Log**: Formatos de mensaje de log personalizados
- **Estadísticas de Verificación**: Seguimiento de conteos de pass/fail/error

**Ejecución:**

```bash
# Usando script orquestador
./scripts/module1.sh --error-handling

# O directamente
python3 module1/examples/error_handling/error_handling_example.py
```

**Salida Esperada:**

```
============================================================
Module 1: Error Handling and Logging
============================================================

1. Basic Error Handling:
   ✓ Successful check passed
   ✓ Caught expected error: Mismatch at address 0x2000: expected 0x5678, got 0x9ABC
   Statistics: {'total': 2, 'pass': 1, 'fail': 1, 'error': 0, 'errors': 1}

2. Exception Chaining:
2024-01-04 10:00:00 - __main__ - ERROR - Caught chained exception: Verification failed
2024-01-04 10:00:00 - __main__ - ERROR - Original exception: Original error
   ✓ Exception chaining demonstrated

3. Retry Logic:
2024-01-04 10:00:01 - __main__ - WARNING - RetryChecker: Attempt 1 failed: ...
2024-01-04 10:00:01 - __main__ - WARNING - RetryChecker: Attempt 2 failed: ...
2024-01-04 10:00:01 - __main__ - INFO - RetryChecker: Operation succeeded on attempt 3
   ✓ Operation succeeded after 3 attempts

4. Logging Levels:
2024-01-04 10:00:02 - __main__ - DEBUG - This is a DEBUG message...
2024-01-04 10:00:02 - __main__ - INFO - This is an INFO message...
2024-01-04 10:00:02 - __main__ - WARNING - This is a WARNING message...
2024-01-04 10:00:02 - __main__ - ERROR - This is an ERROR message...
2024-01-04 10:00:02 - __main__ - CRITICAL - This is a CRITICAL message...
   ✓ Logging levels demonstrated (check verification.log)

============================================================
Example completed successfully!
============================================================
Check 'verification.log' for detailed logs
```

**Conceptos Clave:**

- **Excepciones Personalizadas**: Crear excepciones específicas del dominio para mejor manejo de errores
- **Encadenamiento de Excepciones**: Preservar el contexto de la excepción original con `raise ... from ...`
- **Lógica de Reintento**: Implementar mecanismos robustos de recuperación de errores
- **Niveles de Logging**: Usar niveles apropiados (DEBUG < INFO < WARNING < ERROR < CRITICAL)
- **Handlers de Log**: Múltiples handlers (archivo, consola) para diferentes salidas
- **Formateo de Log**: Personalizar el formato del mensaje de log con marcas de tiempo, niveles, etc.
- **Estadísticas de Verificación**: Seguimiento de resultados de pruebas y errores para reportes

## Resultados de Aprendizaje

Al final de este módulo, deberías ser capaz de:

- Escribir clases Python con herencia
- Usar decoradores y context managers efectivamente
- Entender y usar async/await para simulación
- Explicar fundamentos de verificación
- Entender la arquitectura de testbench
- Comprender el flujo de simulación
- Escribir aserciones básicas
- Usar frameworks de pruebas Python
- Manejar errores e implementar logging

## Casos de Prueba

### Caso de Prueba 1.1: Conceptos Básicos de Clases Python

**Objetivo**: Crear una clase de transacción simple con herencia

**Temas**:

- Definición de clase
- Variables de instancia
- Métodos
- Herencia

### Caso de Prueba 1.2: Decoradores y Async

**Objetivo**: Usar decoradores y funciones async

**Temas**:

- Decoradores de función
- Definición de función async
- Uso de await

### Caso de Prueba 1.3: Prueba de Verificación Simple

**Objetivo**: Crear un testbench de verificación básico

**Temas**:

- Estructura de testbench
- Generación de reloj
- Manejo de señales
- Verificación básica

#### Prueba cocotb: Compuerta AND (`module1/tests/cocotb_tests/test_and_gate.py`)

**Qué demuestra:**

- **Estructura de Prueba**: Usando el decorador `@cocotb.test()`
- **Acceso a Señales**: Lectura y escritura de señales del DUT (`dut.a`, `dut.b`, `dut.y`)
- **Control de Temporización**: Usando `await Timer()` para tiempo de simulación
- **Aserciones**: Aserciones Python para verificar resultados
- **Casos de Prueba**: Múltiples funciones de prueba para diferentes escenarios
- **Prueba de Tabla de Verdad**: Prueba sistemática de todas las combinaciones de entrada

**Ejecución:**

```bash
# Usando script orquestador
./scripts/module1.sh --cocotb-tests

# O manualmente
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_and_gate
```

**Salida Esperada:**

```
     0.00ns INFO     cocotb.regression                  Running test_and_gate_basic (1/3)
     0.00ns INFO     cocotb.regression                  Running test_and_gate_truth_table (2/3)
     0.00ns INFO     cocotb.regression                  Running test_and_gate_timing (3/3)
     0.00ns INFO     cocotb.regression                  test_and_gate passed
```

**Conceptos Clave:**

- **`@cocotb.test()`**: Decorador que marca la función como prueba
- **Acceso DUT**: `dut.signal_name.value` para leer/escribir señales
- **`Timer()`**: Avanza el tiempo de simulación
- **Aserciones**: Sentencias `assert` de Python para verificar
- **Organización de Pruebas**: Múltiples funciones de prueba en un archivo

#### Prueba cocotb: Contador (`module1/tests/cocotb_tests/test_counter.py`)

**Qué demuestra:**

- **Generación de Reloj**: Creando señal de reloj con la corrutina `generate_clock()`
- **Secuencia de Reset**: Implementando reset con temporización adecuada
- **Prueba de Lógica Secuencial**: Probando circuitos sincrónicos (secuenciales)
- **Control de Enable**: Probando funcionalidad de activación/desactivación
- **Detección de Flancos**: Usando el trigger `RisingEdge()`
- **Múltiples Escenarios de Prueba**: Reset, incremento, enable, desbordamiento

**Ejecución:**

```bash
# Usando script orquestador
./scripts/module1.sh --cocotb-tests

# O manualmente
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_counter
```

**Salida Esperada:**

```
     0.00ns INFO     cocotb.regression                  Running test_counter_reset (1/4)
     0.00ns INFO     cocotb.regression                  Running test_counter_increment (2/4)
     0.00ns INFO     cocotb.regression                  Running test_counter_enable (3/4)
     0.00ns INFO     cocotb.regression                  Running test_counter_overflow (4/4)
     0.00ns INFO     cocotb.regression                  test_counter passed
```

**Conceptos Clave:**

- **Generación de Reloj**: Corrutina en segundo plano para la señal de reloj
- **`cocotb.start_soon()`**: Iniciar corrutinas en segundo plano
- **`RisingEdge()`**: Esperar al flanco de subida del reloj
- **Temporización de Reset**: Secuencia de reset adecuada con temporización
- **Prueba Secuencial**: Probando máquinas de estado y contadores

#### Prueba pyuvm: Compuerta AND (`module1/tests/pyuvm_tests/test_and_gate_uvm.py`)

**Qué demuestra:**

- **Estructura de Prueba UVM**: Decorador `@uvm_test()`
- **Fases UVM**: `build_phase()`, `run_phase()`, `check_phase()`
- **Componentes UVM**: `uvm_test`, `uvm_env`, `uvm_agent`, `uvm_driver`, `uvm_monitor`
- **Secuencias UVM**: `uvm_sequence` y `uvm_sequence_item`
- **Reporte UVM**: Usando `self.logger` para mensajes
- **Objeciones**: Usando `raise_objection()` y `drop_objection()` para control de prueba

**Ejecución:**

```bash
# Usando script orquestador
./scripts/module1.sh --pyuvm-tests

# O manualmente
cd module1/tests/pyuvm_tests
make SIM=verilator TEST=test_and_gate_uvm
```

**Nota**: Este es un ejemplo estructural que muestra patrones UVM. La integración completa con cocotb requiere configuración adicional.

**Conceptos Clave:**

- **Fases UVM**: Fases de build, connect, run, check
- **Jerarquía de Componentes**: Test → Environment → Agent → Driver/Monitor
- **Secuencias**: Generan y envían transacciones
- **Objeciones**: Controlan la duración de la ejecución de la prueba
- **Patrón Factory**: UVM usa factory para la creación de componentes

## Ejercicios

1. **Diseño de Clases**
   - Crear una clase de transacción base
   - Derivar tipos de transacción específicos
   - Implementar métodos de comparación
   - **Ubicación**: Extiende `module1/examples/python_basics/transaction.py`
   - **Pista**: Agrega una clase `WriteReadTransaction` que combine ambas operaciones

2. **Patrones Async**
   - Crear múltiples corrutinas paralelas
   - Implementar manejo de timeout
   - Manejar excepciones en código asíncrono
   - **Ubicación**: Extiende `module1/examples/async_await/async_example.py`
   - **Pista**: Crea un monitor que expire si no llegan datos

3. **Estructura de Testbench**
   - Diseñar un testbench simple
   - Implementar reloj y reset
   - Crear estímulo básico
   - **Ubicación**: Crear nueva prueba en `module1/tests/cocotb_tests/`
   - **Pista**: Prueba el contador con diferentes patrones de enable

4. **Aserciones**
   - Agregar aserciones al testbench
   - Probar el comportamiento de las aserciones
   - Entender los mensajes de aserción
   - **Ubicación**: Agregar a pruebas existentes en `module1/tests/cocotb_tests/`
   - **Pista**: Agrega aserciones para restricciones de temporización

5. **Logging**
   - Implementar logging en testbench
   - Usar diferentes niveles de log
   - Formatear mensajes de log
   - **Ubicación**: Extiende `module1/examples/error_handling/error_handling_example.py`
   - **Pista**: Crea un formateador de log personalizado para mensajes de verificación

## Evaluación

- [ ] Puedo escribir clases Python con herencia
- [ ] Entiendo decoradores y context managers
- [ ] Puedo usar async/await efectivamente
- [ ] Entiendo los fundamentos de verificación
- [ ] Puedo explicar la arquitectura de testbench
- [ ] Entiendo el flujo de simulación
- [ ] Puedo escribir aserciones básicas
- [ ] Puedo usar frameworks de pruebas Python
- [ ] Puedo manejar errores e implementar logging

## Próximos Pasos

Después de completar este módulo, continúa con [Módulo 2: Fundamentos de cocotb](MODULE2.md) para aprender a usar cocotb para verificación de hardware.

## Recursos Adicionales

- **Tutorial Oficial de Python**: https://docs.python.org/3/tutorial/
- **Guía Async de Real Python**: https://realpython.com/async-io-python/
- **Documentación de pytest**: https://docs.pytest.org/
- **Guía de Logging de Python**: https://docs.python.org/3/howto/logging.html

## Solución de Problemas

### Problemas Comunes

**Problema: Entorno virtual no encontrado**

```bash
# Solución: Crear entorno virtual primero
python3 -m venv .venv
source .venv/bin/activate
./scripts/module0.sh  # Instalar dependencias
```

**Problema: Las pruebas cocotb fallan con "simulador no encontrado"**

```bash
# Solución: Verificar que Verilator esté instalado
verilator --version
# Si no está instalado, ejecutar:
./scripts/install_verilator.sh --from-submodule
```

**Problema: Errores de importación en ejemplos Python**

```bash
# Solución: Asegurarse de usar el entorno Python correcto
source .venv/bin/activate  # Si usas venv
python3 --version  # Debe ser 3.8+
```

**Problema: Errores de Makefile al ejecutar pruebas**

```bash
# Solución: Asegurarse de que cocotb esté instalado correctamente
python3 -c "import cocotb; print(cocotb.__version__)"
# Verificar que las rutas del Makefile sean correctas
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_and_gate
```

### Obteniendo Ayuda

- Revisa los comentarios del código de ejemplo para explicaciones detalladas
- Consulta el `module1/README.md` para la estructura del directorio
- Ejecuta ejemplos individualmente para aislar problemas
- Revisa los archivos de log (ej. `verification.log` para el ejemplo de manejo de errores)
