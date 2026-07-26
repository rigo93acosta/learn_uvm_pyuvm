# Notas

## Resumen del contenido de la carpeta `module1`

### Estructura del directorio

- **examples/**: Contiene ejemplos de Python organizados por temas:
  - **python_basics/**: Conceptos básicos de Python como clases, herencia y POO. Archivo destacado: `transaction.py`.
  - **decorators/**: Uso de decoradores y gestores de contexto. Archivo destacado: `decorators_example.py`.
  - **async_await/**: Patrones de programación asíncrona. Archivo destacado: `async_example.py`.
  - **data_structures/**: Estructuras de datos útiles para verificación. Archivo destacado: `data_structures_example.py`.
  - **error_handling/**: Manejo de excepciones y registro de logs. Archivo destacado: `error_handling_example.py`.

- **dut/**: Módulos de diseño en Verilog (Design Under Test):
  - **simple_gates/**: Contiene los módulos `and_gate.v` (compuerta AND de 2 entradas) y `counter.v` (contador ascendente de 8 bits con reset).

- **tests/**: Testbenches para verificar los diseños:
  - **cocotb_tests/**: Testbenches basados en cocotb. Archivos destacados: `test_and_gate.py`, `test_counter.py`.
  - **pyuvm_tests/**: Testbenches basados en pyuvm. Archivo destacado: `test_and_gate_uvm.py`.

### Prerrequisitos

Antes de ejecutar los experimentos, asegúrate de tener:

- **Python 3.8+**: Requerido para cocotb y pyuvm.
- **Verilator 5.036+**: Requerido para simulación (se recomienda la versión 5.044).
- **cocotb 2.0+**: Instalado en un entorno virtual.
- **pyuvm 4.0+**: Instalado en un entorno virtual.

### Explicaciones de los ejemplos

#### 1. **python_basics/transaction.py**
   Este archivo introduce los conceptos básicos de clases en Python, incluyendo:
   - **Definición de clases**: Se utiliza la clase `Transaction` como ejemplo.
   - **Variables de instancia y de clase**: `self.id` y `_id_counter`.
   - **Métodos especiales**: Implementación de `__str__`, `__repr__` y `__eq__` para personalizar el comportamiento de la clase.
   - **Uso de `dataclasses` y `typing`**: Para simplificar la definición de clases y mejorar la legibilidad.

#### 2. **decorators/decorators_example.py**
   Este archivo demuestra el uso de decoradores y gestores de contexto:
   - **Decoradores**:
     - `timing_decorator`: Mide el tiempo de ejecución de una función.
     - `log_calls_decorator`: Registra las llamadas a funciones.
   - **Gestores de contexto**: Uso de `contextlib` para manejar recursos de manera eficiente.
   - **Registro de logs**: Configuración de `logging` para capturar información de depuración.

#### 3. **async_await/async_example.py**
   Este archivo muestra patrones de programación asíncrona:
   - **Simulación de tiempo**: Uso de `asyncio.sleep` para simular retardos en nanosegundos.
   - **Generador de reloj**: Implementación de un generador de señales de reloj con un número específico de ciclos.
   - **Uso de `async/await`**: Para manejar tareas concurrentes de manera eficiente.

#### 4. **data_structures/data_structures_example.py**
   Este archivo explora estructuras de datos útiles para verificación:
   - **`deque`**: Para implementar colas FIFO/LIFO.
   - **`namedtuple`**: Para definir transacciones con campos específicos (`id`, `address`, `data`, `timestamp`).
   - **Operaciones básicas**: Métodos `push` y `pop` para manejar transacciones.

#### 5. **error_handling/error_handling_example.py**
   Este archivo aborda el manejo de errores y registro de logs:
   - **Excepciones personalizadas**:
     - `VerificationError`: Clase base para errores de verificación.
     - `MismatchError`: Para discrepancias en datos esperados y reales.
   - **Registro de logs**: Configuración avanzada para capturar errores en un archivo y en la consola.
   - **Uso de `enum`**: Para definir estados o tipos de errores.

### Explicación de lo realizado en `pyuvm_tests/test_and_gate_uvm.py`

Este archivo implementa un testbench basado en `pyuvm` para verificar una compuerta AND:
- **Transacciones (`AndGateTransaction`)**:
  - Define los campos `a`, `b` y `expected_y` para representar entradas y salidas esperadas.
  - Incluye un método `__str__` para mostrar información de la transacción.
  - `set_value_txn()` actúa como método factory para construir la transacción a partir de una lista de valores.
- **Secuencias (`AndGateSequence`)**:
  - Genera vectores de prueba para la compuerta AND.
  - Los vectores incluyen combinaciones de entradas y sus salidas esperadas:
    - `(0, 0, 0)`
    - `(0, 1, 0)`
    - `(1, 0, 0)`
    - `(1, 1, 1)`
  - Usa `start_item()` / `finish_item()` dentro de `body()` para enviar cada transacción al sequencer.
- **Driver (`AndGateDriver`)**:
  - Extiende `uvm_driver`. En `build_phase()` obtiene el handle del DUT vía `cocotb.top`.
  - En `run_phase()` hace `await self.seq_item_port.get_next_item()` en un loop, conduce las señales `a`/`b` del DUT, espera propagación con `await Timer(10, unit="ns")` y notifica finalización con `self.seq_item_port.item_done()`.
- **Monitor (`AndGateMonitor`)**:
  - Extiende `uvm_monitor`. En `build_phase()` crea un `uvm_analysis_port` (`self.ap`).
  - En `run_phase()` muestrea la salida `y` del DUT y publica una transacción observada con `self.ap.write(observed_txn)`.
- **Agente (`AndGateAgent`)**:
  - Extiende `uvm_agent`. En `build_phase()` crea el `driver`, el `monitor` y el `sequencer` (`uvm_sequencer`).
  - En `connect_phase()` conecta `driver.seq_item_port` con `seqr.seq_item_export`.
- **Entorno (`AndGateEnv`)**:
  - Extiende `uvm_env`. Instancia el `AndGateAgent` en `build_phase()`.
- **Test (`AndGateTest`)**, decorado con `@pyuvm.test()`:
  - Extiende `uvm_test`. Construye el `AndGateEnv` en `build_phase()`.
  - En `run_phase()` levanta una objeción (`self.raise_objection()`), crea y arranca la secuencia (`AndGateSequence.create("seq")` + `await seq.start(...)`), espera con `Timer(100, unit="ns")` y baja la objeción (`self.drop_objection()`).
  - `check_phase()` registra un mensaje de verificación de resultados vía `self.logger`.
- **Fases UVM utilizadas**: `build_phase()`, `connect_phase()`, `run_phase()`, `check_phase()`.
- **Objeciones**: `raise_objection()` / `drop_objection()` controlan cuánto dura la ejecución de la prueba antes de terminar.
- **Nota**: Es un ejemplo estructural que muestra los patrones UVM; el driver/monitor no interactúan aún con señales reales de forma completa (esa integración llega en módulos posteriores).

## Ejercicios propuestos (pendientes de resolver)

Según `docs/MODULE1.md` / `docs/MODULE1_es.md`, quedan los siguientes ejercicios del Módulo 1 **sin solución todavía**:

1. **Diseño de Clases** — Crear una clase de transacción base, derivar tipos específicos e implementar métodos de comparación.
   - Ubicación: extender `module1/examples/python_basics/transaction.py`.
   - Pista: agregar una clase `WriteReadTransaction` que combine lectura y escritura.

2. **Patrones Async** — Crear múltiples corrutinas paralelas, manejar timeout y excepciones en código asíncrono.
   - Ubicación: extender `module1/examples/async_await/async_example.py`.
   - Pista: crear un monitor que expire si no llegan datos.

3. **Estructura de Testbench** — Diseñar un testbench simple con reloj, reset y estímulo básico.
   - Ubicación: crear una nueva prueba en `module1/tests/cocotb_tests/`.
   - Pista: probar el contador con diferentes patrones de enable.

4. **Aserciones** — Agregar aserciones a un testbench existente y entender sus mensajes. (Realizado)
   - Ubicación: agregar a las pruebas existentes en `module1/tests/cocotb_tests/`.
   - Pista: agregar aserciones para restricciones de temporización.

5. **Logging** — Implementar logging en un testbench con distintos niveles y formato de mensajes.
   - Ubicación: extender `module1/examples/error_handling/error_handling_example.py`.
   - Pista: crear un formateador de log personalizado para mensajes de verificación.


