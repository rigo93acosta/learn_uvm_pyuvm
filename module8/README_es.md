# Módulo 8: Utilidades Avanzadas de UVM

Este directorio contiene todos los ejemplos, ejercicios y casos de prueba para el Módulo 8, enfocado en utilidades avanzadas de UVM incluyendo procesamiento de línea de comandos, comparadores, grabadores, pools, colas y funciones utilitarias para cadenas, matemáticas y generación de números aleatorios.

## Estructura del Directorio

```
module8/
├── examples/              # Ejemplos de pyuvm para cada tema
│   ├── clp/              # Ejemplos de procesador de línea de comandos
│   │   └── clp_example.py
│   ├── comparators/      # Ejemplos de comparadores
│   │   └── comparator_example.py
│   ├── recorders/        # Ejemplos de grabadores
│   │   └── recorder_example.py
│   ├── pools/            # Ejemplos de pools
│   │   └── pool_example.py
│   ├── queues/           # Ejemplos de colas
│   │   └── queue_example.py
│   ├── string_utils/     # Ejemplos de utilidades de cadenas
│   │   └── string_utils_example.py
│   ├── math_utils/       # Ejemplos de utilidades matemáticas
│   │   └── math_utils_example.py
│   ├── random_utils/     # Ejemplos de utilidades aleatorias
│   │   └── random_utils_example.py
│   └── integration/      # Ejemplos de integración de utilidades
│       └── integration_example.py
├── dut/                   # Módulos Verilog Design Under Test
│   └── dma/              # Controlador DMA
│       └── simple_dma.v
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # Testbenches pyuvm
│       └── test_utilities.py
└── exercises/            # Soluciones de ejercicios (si las hay)
```

## Prerrequisitos

Antes de ejecutar los experimentos, asegúrate de tener:

- **Python 3.8+** - Requerido para cocotb y pyuvm
- **Verilator 5.036+** - Requerido para simulación (5.044 recomendado)
- **cocotb 2.0+** - Instalado en el entorno virtual
- **pyuvm 4.0+** - Instalado en el entorno virtual
- **Make** - Para compilar y ejecutar pruebas

Para verificar tu entorno:

```bash
python3 --version        # Debe ser 3.8+
verilator --version      # Debe ser 5.036+
python3 -c "import cocotb; print(cocotb.__version__)"
python3 -c "import pyuvm; print(pyuvm.__version__)"
```

## Ejemplos de Utilidades Avanzadas de UVM

### 1. Procesador de Línea de Comandos (CLP) (`examples/clp/clp_example.py`)

Demuestra el uso de argumentos de línea de comandos para configuración de pruebas:

**Conceptos Clave:**
- Análisis de argumentos de línea de comandos
- Configuración de pruebas mediante línea de comandos
- Paso de parámetros desde la línea de comandos
- Selección de modo de prueba
- Configuración de semilla y nivel de depuración

**Componentes CLP:**

1. **CLPEnv**
   - Entorno que demuestra el uso de CLP
   - Analiza argumentos de línea de comandos usando `get_clp_arg()`
   - Configura la prueba según parámetros de línea de comandos
   - Soporta modo de prueba, nivel de depuración, conteo de transacciones y semilla

2. **Método get_clp_arg()**
   - Obtiene valores de argumentos de línea de comandos
   - Soporta el formato `+arg_name=value`
   - Soporta banderas booleanas `+arg_name`
   - Devuelve valor por defecto si el argumento no se encuentra
   - Simula el comportamiento de UVM CLP en Python

**Uso de CLP:**

**Argumentos de Línea de Comandos:**
```bash
# Ejecutar con argumentos de línea de comandos
make SIM=verilator TEST=clp_example EXTRA_ARGS="+test_mode=stress +debug_level=3 +num_transactions=100 +seed=42"
```

**Formato de Argumentos:**
- `+test_mode=normal` - Parámetro de modo de prueba
- `+debug_level=2` - Parámetro de nivel de depuración
- `+num_transactions=50` - Parámetro de número de transacciones
- `+seed=123` - Parámetro de semilla aleatoria

**Configuración CLP:**
```python
# Obtener argumentos de línea de comandos
self.test_mode = self.get_clp_arg("+test_mode", "normal")
self.debug_level = int(self.get_clp_arg("+debug_level", "0"))
self.num_transactions = int(self.get_clp_arg("+num_transactions", "10"))
self.seed = int(self.get_clp_arg("+seed", "0"))
```

**Ejecutar el ejemplo:**

```bash
# Mediante el script del módulo
./scripts/module8.sh --clp

# O directamente desde el directorio del ejemplo
cd module8/examples/clp
make SIM=verilator TEST=clp_example EXTRA_ARGS="+test_mode=stress +num_transactions=20"
```

**Salida Esperada:**
- Análisis de argumentos de línea de comandos
- Configuración de prueba desde línea de comandos
- Uso de parámetros en la ejecución de pruebas
- Selección de modo de prueba

### 2. Comparadores (`examples/comparators/comparator_example.py`)

Demuestra el uso de comparadores para la comparación de transacciones en scoreboards:

**Conceptos Clave:**
- Comparación de transacciones en orden
- Comparación de transacciones fuera de orden
- Algoritmos de coincidencia de transacciones
- Estadísticas y reporte de comparadores

**Componentes del Comparador:**

1. **InOrderComparator**
   - Compara transacciones en orden de llegada
   - Coincide transacciones esperadas y reales secuencialmente
   - Reporta coincidencias y discrepancias
   - Rastrea estadísticas de comparación

2. **OutOfOrderComparator**
   - Compara transacciones sin requerir orden
   - Usa algoritmos de coincidencia (ej. por dirección, por datos)
   - Maneja llegada de transacciones fuera de orden
   - Reporta coincidencias y discrepancias

3. **ComparatorTransaction**
   - Transacción para el ejemplo de comparador
   - Soporta comparación de igualdad mediante `__eq__()`
   - Soporta hash para uso en conjuntos/diccionarios mediante `__hash__()`
   - Contiene campos de datos, dirección y marca de tiempo

**Tipos de Comparador:**

**Comparación en Orden:**
- Esperado y real deben llegar en el mismo orden
- El primero esperado coincide con el primero real
- Algoritmo de coincidencia FIFO simple

**Comparación Fuera de Orden:**
- Esperado y real pueden llegar en cualquier orden
- Coincidencia por campos clave (ej. dirección, datos)
- Algoritmo de coincidencia más complejo

**Uso del Comparador:**
```python
# Crear comparador
comparator = InOrderComparator.create("comparator", self)

# Conectar suscriptores de esperado y real
monitor_expected.ap.connect(comparator.expected_subscriber.analysis_export)
monitor_actual.ap.connect(comparator.actual_subscriber.analysis_export)

# El comparador compara transacciones automáticamente
```

**Ejecutar el ejemplo:**

```bash
./scripts/module8.sh --comparators
# o
cd module8/examples/comparators
make SIM=verilator TEST=comparator_example
```

**Salida Esperada:**
- Demostración de comparación de transacciones
- Detección de coincidencias y discrepancias
- Reporte de estadísticas del comparador
- Comparación en orden y fuera de orden

### 3. Grabadores (`examples/recorders/recorder_example.py`)

Demuestra la grabación de transacciones para análisis:

**Conceptos Clave:**
- Grabación en archivo de texto
- Grabación en archivo JSON
- Almacenamiento en base de datos de transacciones
- Formato y estructura de grabación
- Análisis post-simulación

**Componentes del Grabador:**

1. **TextRecorder**
   - Graba transacciones en archivo de texto
   - Formato legible para humanos
   - Marca de tiempo para cada transacción
   - Almacenamiento simple basado en archivos

2. **JSONRecorder**
   - Graba transacciones en archivo JSON
   - Formato legible por máquina
   - Almacenamiento estructurado de datos
   - Análisis y análisis sencillo

3. **TransactionDatabase**
   - Base de datos de transacciones en memoria
   - Almacena transacciones para consultas
   - Soporta filtrado y búsqueda
   - Análisis post-simulación

**Formatos de Grabación:**

**Formato de Texto:**
```
Transaction Recording Started: 2024-01-01 10:00:00
============================================================
[2024-01-01 10:00:01.123456] id=1, data=0xAA, addr=0x1000, ts=100
[2024-01-01 10:00:02.234567] id=2, data=0xBB, addr=0x2000, ts=200
============================================================
Transaction Recording Ended: 2024-01-01 10:00:05
Total transactions recorded: 2
```

**Formato JSON:**
```json
{
  "start_time": "2024-01-01T10:00:00",
  "end_time": "2024-01-01T10:00:05",
  "total_transactions": 2,
  "transactions": [
    {
      "transaction_id": 1,
      "data": "0xaa",
      "address": "0x1000",
      "timestamp": 100,
      "record_time": "2024-01-01T10:00:01.123456"
    }
  ]
}
```

**Ejecutar el ejemplo:**

```bash
./scripts/module8.sh --recorders
# o
cd module8/examples/recorders
make SIM=verilator TEST=recorder_example
```

**Salida Esperada:**
- Grabación de transacciones en archivos
- Grabación en formato texto y JSON
- Almacenamiento y consulta en base de datos
- Estadísticas de grabación

### 4. Pools (`examples/pools/pool_example.py`)

Demuestra pooling de objetos para optimización de rendimiento:

**Conceptos Clave:**
- Patrones de reutilización de objetos
- Optimización de asignación de memoria
- Configuración de tamaño del pool
- Seguimiento de asignación y desasignación
- Beneficios de rendimiento

**Componentes del Pool:**

1. **TransactionPool**
   - Pool de objetos para reutilización de transacciones
   - Pre-asigna un pool de objetos
   - Reduce la sobrecarga de asignación de memoria
   - Rastrea estadísticas de asignación y reutilización

2. **PoolTransaction**
   - Transacción con método `reset()`
   - Soporta reutilización después del reseteo
   - Resetea todos los campos al estado inicial

**Operaciones del Pool:**

**Asignación:**
```python
# Obtener transacción del pool
txn = pool.get()  # Reutiliza existente o crea nueva
```

**Desasignación:**
```python
# Devolver transacción al pool
pool.put(txn)  # Resetea y devuelve al pool
```

**Beneficios del Pool:**
- Reduce la sobrecarga de asignación de memoria
- Mejora el rendimiento reutilizando objetos
- Tamaño del pool configurable
- Rastrea estadísticas de reutilización

**Ejecutar el ejemplo:**

```bash
./scripts/module8.sh --pools
# o
cd module8/examples/pools
make SIM=verilator TEST=pool_example
```

**Salida Esperada:**
- Creación y gestión del pool de objetos
- Demostración de asignación y desasignación
- Reporte de estadísticas de reutilización
- Beneficios de optimización de rendimiento

### 5. Colas (`examples/queues/queue_example.py`)

Demuestra estructuras de datos de colas para la gestión de transacciones:

**Conceptos Clave:**
- Operaciones de cola FIFO
- Soporte de cola de prioridad
- Gestión de tamaño de cola
- Manejo de desbordamiento
- Estadísticas de cola

**Componentes de Cola:**

1. **TransactionQueue**
   - Cola FIFO para transacciones
   - Usa `deque` de Python para eficiencia
   - Soporta configuración de tamaño máximo
   - Rastrea estadísticas de cola

2. **QueueTransaction**
   - Transacción con campo de prioridad
   - Soporta ordenamiento basado en prioridad
   - Contiene datos, dirección y prioridad

**Operaciones de Cola:**

**Push:**
```python
# Agregar elemento a la cola
queue.push(item)  # Devuelve True si se agregó, False si hay desbordamiento
```

**Pop:**
```python
# Eliminar y devolver elemento de la cola
item = queue.pop()  # Devuelve None si está vacía
```

**Tipos de Cola:**

**Cola FIFO:**
- Primero en entrar, primero en salir
- Comportamiento estándar de cola
- Procesamiento secuencial

**Cola de Prioridad:**
- Elementos ordenados por prioridad
- Mayor prioridad se procesa primero
- Ordenamiento más complejo

**Ejecutar el ejemplo:**

```bash
./scripts/module8.sh --queues
# o
cd module8/examples/queues
make SIM=verilator TEST=queue_example
```

**Salida Esperada:**
- Creación y gestión de cola
- Operaciones push y pop
- Seguimiento de tamaño de cola
- Demostración de manejo de desbordamiento

### 6. Utilidades de Cadenas (`examples/string_utils/string_utils_example.py`)

Demuestra utilidades de manipulación de cadenas para UVM:

**Conceptos Clave:**
- Formateo y conversión de cadenas
- Conversión hexadecimal y binaria
- Manipulación de rutas
- Comparación de cadenas
- Representación de transacciones como cadena

**Utilidades de Cadenas:**

1. **Formateo de Cadenas:**
   - Formateo hexadecimal: `f"0x{data:04X}"`
   - Formateo binario: `bin(data)`
   - Cadenas de formato personalizado

2. **Conversión de Cadenas:**
   - `hex()` - Convertir a cadena hexadecimal
   - `bin()` - Convertir a cadena binaria
   - `str()` - Convertir a cadena

3. **Manipulación de Rutas:**
   - `split('/')` - Dividir componentes de ruta
   - `join()` - Unir componentes de ruta
   - Extracción de nombre base y directorio

4. **Comparación de Cadenas:**
   - Comparación sensible a mayúsculas
   - Comparación insensible a mayúsculas
   - Coincidencia de patrones

**Uso de Utilidades de Cadenas:**
```python
# Formateo
formatted = f"data=0x{data:04X}, addr=0x{addr:04X}"

# Conversión
hex_str = hex(data)
bin_str = bin(data)

# Manipulación de rutas
basename = path.split('/')[-1]
dirname = '/'.join(path.split('/')[:-1])

# Representación de transacción como cadena
txn_str = ", ".join([f"{k}=0x{v:04X}" if isinstance(v, int) else f"{k}={v}" 
                     for k, v in txn_data.items()])
```

**Ejecutar el ejemplo:**

```bash
./scripts/module8.sh --string-utils
# o
cd module8/examples/string_utils
make SIM=verilator TEST=string_utils_example
```

**Salida Esperada:**
- Formateo y conversión de cadenas
- Demostración de manipulación de rutas
- Ejemplos de comparación de cadenas
- Representación de transacciones como cadena

### 7. Utilidades Matemáticas (`examples/math_utils/math_utils_example.py`)

Demuestra utilidades matemáticas para UVM:

**Conceptos Clave:**
- Generación de números aleatorios
- Funciones estadísticas
- Operaciones matemáticas
- Manipulación de bits
- Operaciones de rango

**Utilidades Matemáticas:**

1. **Generación de Números Aleatorios:**
   - `random.randint()` - Entero aleatorio
   - `random.random()` - Flotante aleatorio
   - Configuración de semilla

2. **Funciones Estadísticas:**
   - `statistics.mean()` - Valor medio
   - `statistics.median()` - Valor mediano
   - `statistics.stdev()` - Desviación estándar

3. **Manipulación de Bits:**
   - Extracción de bits: `(value >> bit) & 1`
   - Establecer bit: `value | (1 << bit)`
   - Limpiar bit: `value & ~(1 << bit)`

4. **Operaciones de Rango:**
   - `min()` - Valor mínimo
   - `max()` - Valor máximo
   - Cálculo de rango

**Uso de Utilidades Matemáticas:**
```python
# Generación de números aleatorios
random.seed(42)
rand_int = random.randint(0, 100)
rand_float = random.random()

# Funciones estadísticas
mean_val = statistics.mean(data)
median_val = statistics.median(data)
stdev_val = statistics.stdev(data)

# Manipulación de bits
bit_value = (value >> 8) & 1
set_bit = value | (1 << 4)
clear_bit = value & ~(1 << 4)
```

**Ejecutar el ejemplo:**

```bash
./scripts/module8.sh --math-utils
# o
cd module8/examples/math_utils
make SIM=verilator TEST=math_utils_example
```

**Salida Esperada:**
- Demostración de generación de números aleatorios
- Uso de funciones estadísticas
- Ejemplos de manipulación de bits
- Demostración de operaciones de rango

### 8. Utilidades Aleatorias (`examples/random_utils/random_utils_example.py`)

Demuestra generación de números aleatorios y aleatorización restringida:

**Conceptos Clave:**
- Aleatorización de transacciones
- Aleatorización restringida
- Gestión de semillas
- Generación de secuencias aleatorias
- Aleatoriedad reproducible

**Utilidades Aleatorias:**

1. **RandomTransaction**
   - Transacción con campos aleatorios
   - Método `randomize()` para aleatorización
   - `randomize_constrained()` para aleatorización restringida
   - Soporta configuración de semilla

2. **RandomSequence**
   - Secuencia que genera transacciones aleatorias
   - Semilla configurable
   - Genera múltiples transacciones aleatorias

3. **ConstrainedRandomSequence**
   - Secuencia con aleatorización restringida
   - Restricciones configurables (valores mín/máx)
   - Aleatoriedad controlada

**Métodos de Aleatorización:**

**Aleatorización Básica:**
```python
txn = RandomTransaction()
txn.randomize()  # Aleatorizar todos los campos
```

**Aleatorización Restringida:**
```python
txn = RandomTransaction()
txn.randomize_constrained(
    data_min=0x00, data_max=0xFF,
    addr_min=0x0000, addr_max=0xFFFF,
    length_min=1, length_max=256
)
```

**Configuración de Semilla:**
```python
# Establecer semilla para reproducibilidad
random.seed(42)

# O pasar semilla a randomize
txn.randomize(seed=42)
```

**Ejecutar el ejemplo:**

```bash
./scripts/module8.sh --random-utils
# o
cd module8/examples/random_utils
make SIM=verilator TEST=random_utils_example
```

**Salida Esperada:**
- Demostración de aleatorización de transacciones
- Ejemplos de aleatorización restringida
- Gestión de semillas y reproducibilidad
- Generación de secuencias aleatorias

### 9. Integración de Utilidades (`examples/integration/integration_example.py`)

Demuestra la integración de múltiples utilidades en un testbench:

**Conceptos Clave:**
- Combinación de múltiples utilidades
- Patrones de interacción de utilidades
- Diseño de testbench integrado
- Coordinación de utilidades

**Componentes de Integración:**

1. **Utilidades Combinadas:**
   - CLP para configuración
   - Pools para reutilización de objetos
   - Colas para gestión de transacciones
   - Comparadores para verificación
   - Grabadores para análisis

2. **Patrones de Integración:**
   - Inicialización de utilidades
   - Coordinación de utilidades
   - Flujo de datos entre utilidades
   - Reporte de utilidades

**Ejemplo de Integración:**
```python
# Inicializar utilidades
pool = TransactionPool.create("pool", self, pool_size=10)
queue = TransactionQueue.create("queue", self, max_size=100)
comparator = InOrderComparator.create("comparator", self)
recorder = TextRecorder.create("recorder", self, filename="transactions.txt")

# Usar utilidades juntas
txn = pool.get()  # Obtener del pool
queue.push(txn)   # Agregar a la cola
txn_processed = queue.pop()  # Procesar desde la cola
recorder.write(txn_processed)  # Grabar transacción
```

**Ejecutar el ejemplo:**

```bash
./scripts/module8.sh --integration
# o
cd module8/examples/integration
make SIM=verilator TEST=integration_example
```

**Salida Esperada:**
- Integración de múltiples utilidades
- Demostración de interacción de utilidades
- Uso coordinado de utilidades
- Operación de testbench integrado

## Design Under Test (DUT)

### Controlador DMA Simple (`dut/dma/simple_dma.v`)

Un controlador DMA simple para ejemplos de utilidades de verificación. Este es el mismo DUT utilizado en el Módulo 7.

**Interfaz del Módulo:**
```verilog
module simple_dma (
    input  wire        clk,            // Señal de reloj
    input  wire        rst_n,          // Reset activo en bajo
    input  wire        dma_start,      // Iniciar transferencia DMA
    output reg         dma_done,       // Transferencia DMA completada
    input  wire [31:0] dma_src_addr,   // Dirección de origen (32-bit)
    input  wire [31:0] dma_dst_addr,   // Dirección de destino (32-bit)
    input  wire [15:0] dma_length,     // Longitud de transferencia (16-bit)
    input  wire [2:0]  dma_channel     // Selección de canal DMA (3-bit)
);
```

**Funcionalidad:**
- Direcciones de origen y destino configurables
- Longitud de transferencia variable
- Soporte de múltiples canales
- Indicación de inicio y finalización de transferencia
- Contador de transferencia para seguimiento de progreso

**Nota:** Este DUT se utiliza principalmente con fines de demostración de utilidades. Las utilidades se pueden aplicar a cualquier DUT o testbench.

## Testbenches

### Pruebas pyuvm (`tests/pyuvm_tests/`)

#### Prueba de Utilidades (`test_utilities.py`)

Testbench UVM completo que demuestra el uso de utilidades:

**Componentes UVM:**

1. **Transaction (`UtilitiesTransaction`)**
   - Contiene campos `data` y `address`
   - Utilizado para demostración de utilidades

2. **Sequence (`UtilitiesSequence`)**
   - Genera transacciones de prueba
   - Crea vectores de prueba exhaustivos

3. **Driver (`UtilitiesDriver`)**
   - Recibe transacciones del secuenciador
   - Maneja las entradas del DUT

4. **Monitor (`UtilitiesMonitor`)**
   - Muestrea las salidas del DUT
   - Crea transacciones a partir de los datos muestreados
   - Transmite a través del puerto de análisis

5. **Scoreboard (`UtilitiesScoreboard`)**
   - Extiende `uvm_subscriber`
   - Recibe transacciones del monitor
   - Rastrea transacciones recibidas

6. **Agent (`UtilitiesAgent`)**
   - Contiene driver, monitor y secuenciador
   - Conecta componentes

7. **Environment (`UtilitiesEnv`)**
   - Contiene agente y scoreboard
   - Conecta el monitor con el scoreboard

8. **Test (`UtilitiesTest`)**
   - Clase de prueba de nivel superior
   - Crea el entorno y ejecuta la prueba
   - Inicia la secuencia y verifica los resultados

**Flujo de Prueba:**
1. `build_phase()` - Crear todos los componentes
2. `connect_phase()` - Conectar componentes
3. `run_phase()` - Iniciar secuencia, generar transacciones
4. `check_phase()` - Verificar resultados
5. `report_phase()` - Generar reporte de prueba

**Ejecutar la prueba:**

```bash
# Mediante el script del módulo
./scripts/module8.sh --pyuvm-tests

# Directamente desde el directorio de pruebas
cd module8/tests/pyuvm_tests
make SIM=verilator TEST=test_utilities
```

**Resultados Esperados:**
- 1 caso de prueba exitoso
- Todos los componentes creados y conectados
- Ejecución de secuencia demostrada
- Seguimiento de scoreboard demostrado
- Conceptos de utilidades integrados

## Ejecutar Ejemplos y Pruebas

### Usando el Script del Módulo

El script `module8.sh` proporciona una forma conveniente de ejecutar todos los ejemplos y pruebas:

```bash
# Ejecutar todo (todos los ejemplos + todas las pruebas)
./scripts/module8.sh

# Ejecutar solo ejemplos
./scripts/module8.sh --all-examples

# Ejecutar solo pruebas
./scripts/module8.sh --pyuvm-tests

# Ejecutar ejemplos específicos
./scripts/module8.sh --clp
./scripts/module8.sh --comparators
./scripts/module8.sh --recorders
./scripts/module8.sh --pools
./scripts/module8.sh --queues
./scripts/module8.sh --string-utils
./scripts/module8.sh --math-utils
./scripts/module8.sh --random-utils
./scripts/module8.sh --integration

# Combinar opciones
./scripts/module8.sh --clp --comparators --pyuvm-tests
```

### Ejecutar Ejemplos Individuales

#### Ejecución Directa desde el Directorio del Ejemplo

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio del ejemplo
cd module8/examples/clp

# Ejecutar ejemplo
make SIM=verilator TEST=clp_example

# Limpiar artefactos de compilación
make clean
```

#### Ejecutar Todos los Ejemplos Secuencialmente

```bash
cd module8/examples

# CLP
cd clp && make SIM=verilator TEST=clp_example && cd ..

# Comparators
cd comparators && make SIM=verilator TEST=comparator_example && cd ..

# Recorders
cd recorders && make SIM=verilator TEST=recorder_example && cd ..

# Pools
cd pools && make SIM=verilator TEST=pool_example && cd ..

# Queues
cd queues && make SIM=verilator TEST=queue_example && cd ..

# String utils
cd string_utils && make SIM=verilator TEST=string_utils_example && cd ..

# Math utils
cd math_utils && make SIM=verilator TEST=math_utils_example && cd ..

# Random utils
cd random_utils && make SIM=verilator TEST=random_utils_example && cd ..

# Integration
cd integration && make SIM=verilator TEST=integration_example && cd ..
```

### Ejecutar Pruebas pyuvm

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio de pruebas
cd module8/tests/pyuvm_tests

# Ejecutar prueba
make SIM=verilator TEST=test_utilities

# Limpiar artefactos de compilación
make clean
```

## Resultados de las Pruebas

Cuando las pruebas se completen exitosamente, deberías ver una salida similar a:

### Salida de Ejemplo de Prueba

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** clp_example.test_clp                           PASS         200.00           0.00     123456.78  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 200.00           0.00      12345.67  **
```

### Conteo Esperado de Pruebas

- **Ejemplo CLP**: 1 prueba
- **Ejemplo de comparadores**: 1 prueba
- **Ejemplo de grabadores**: 1 prueba
- **Ejemplo de pools**: 1 prueba
- **Ejemplo de colas**: 1 prueba
- **Ejemplo de utilidades de cadenas**: 1 prueba
- **Ejemplo de utilidades matemáticas**: 1 prueba
- **Ejemplo de utilidades aleatorias**: 1 prueba
- **Ejemplo de integración**: 1 prueba
- **Prueba de utilidades**: 1 prueba
- **Total**: 10 pruebas en todos los ejemplos y testbenches

## Solución de Problemas

### Problemas Comunes

#### 1. Error de Versión de Verilator

**Error:** `cocotb requires Verilator 5.036 or later, but using 5.020`

**Solución:** Actualiza Verilator a 5.036 o posterior:

```bash
./scripts/install_verilator.sh --from-submodule --force
```

#### 2. Errores de Módulo No Encontrado

**Error:** `ModuleNotFoundError: No module named 'pyuvm'` o `ModuleNotFoundError: No module named 'cocotb'`

**Solución:** Activa el entorno virtual:

```bash
source .venv/bin/activate
```

#### 3. Problemas de Análisis de Argumentos CLP

**Error:** Los argumentos de línea de comandos no se reconocen

**Solución:**
- Verifica el formato del argumento: `+arg_name=value` o `+arg_name`
- Comprueba que los nombres de argumento coincidan exactamente
- Asegúrate de que `EXTRA_ARGS` se pase al Makefile
- Verifica la implementación de `get_clp_arg()`

#### 4. Problemas de Discrepancia del Comparador

**Error:** Los comparadores reportan discrepancias inesperadas

**Solución:**
- Verifica la implementación del método `__eq__()` de la transacción
- Comprueba la lógica de comparación en el comparador
- Asegúrate de que las transacciones esperadas y reales tengan el mismo tipo
- Verifica los criterios de coincidencia de campos de transacción

#### 5. Problemas de Archivos del Grabador

**Error:** Los archivos grabados no se crean o están corruptos

**Solución:**
- Verifica los permisos de la ruta del archivo
- Comprueba las operaciones de apertura/cierre de archivos
- Asegúrate de que el formateo JSON sea correcto
- Verifica el método `to_dict()` de la transacción

#### 6. Problemas de Asignación del Pool

**Error:** La asignación del pool falla o tiene fugas

**Solución:**
- Verifica que el tamaño del pool sea suficiente
- Comprueba que `get()` y `put()` estén correctamente emparejados
- Asegúrate de que el método `reset()` limpie todos los campos
- Monitorea las estadísticas de asignación del pool

#### 7. Problemas de Desbordamiento de Cola

**Error:** Advertencias de desbordamiento de cola

**Solución:**
- Aumenta el tamaño máximo de la cola
- Verifica que los elementos se eliminen de la cola
- Comprueba la tasa de procesamiento de la cola
- Monitorea las estadísticas de la cola

### Consejos de Depuración

1. **Verificar Argumentos CLP:**
   ```python
   # Verify argument parsing
   self.logger.info(f"CLP args: test_mode={self.test_mode}, num_txns={self.num_transactions}")
   ```

2. **Monitorear Operaciones del Comparador:**
   ```python
   # Add logging in comparator
   self.logger.info(f"Comparing: expected={exp_txn}, actual={act_txn}")
   ```

3. **Verificar Estado del Grabador:**
   ```python
   # Verify recording
   self.logger.info(f"Recorded {self.recorded_count} transactions")
   ```

4. **Inspeccionar Estadísticas del Pool:**
   ```python
   # Check pool usage
   self.logger.info(f"Pool: allocated={self.allocated_count}, reused={self.reused_count}")
   ```

5. **Monitorear Estado de la Cola:**
   ```python
   # Check queue size
   self.logger.info(f"Queue: size={queue.size()}, added={queue.added_count}, removed={queue.removed_count}")
   ```

## Temas Cubiertos

1. **Procesador de Línea de Comandos** - Análisis de argumentos CLP, configuración de pruebas
2. **Comparadores** - Comparación de transacciones en orden y fuera de orden
3. **Grabadores** - Grabación de transacciones en texto, JSON y base de datos
4. **Pools** - Pooling de objetos para optimización de rendimiento
5. **Colas** - Estructuras de datos FIFO y cola de prioridad
6. **Utilidades de Cadenas** - Formateo, conversión y manipulación de cadenas
7. **Utilidades Matemáticas** - Números aleatorios, estadísticas, manipulación de bits
8. **Utilidades Aleatorias** - Aleatorización restringida, gestión de semillas
9. **Integración de Utilidades** - Combinación de múltiples utilidades en testbenches
10. **Optimización de Rendimiento** - Optimización de testbench basada en utilidades

## Próximos Pasos

Después de completar el Módulo 8, has completado la ruta de aprendizaje completa de UVM/PyUVM.

**Próximos Pasos Recomendados:**
- Revisa todos los módulos y consolida el aprendizaje
- Construye un proyecto de verificación completo usando todos los conceptos
- Explora temas avanzados en la documentación de pyuvm
- Contribuye a proyectos open-source de UVM/PyUVM

## Recursos Adicionales

- [Documentación de pyuvm](https://pyuvm.readthedocs.io/)
- [Guía de Usuario de UVM](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_1.2.pdf)
- [Documentación de Python](https://docs.python.org/3/)
- [Documentación de cocotb](https://docs.cocotb.org/)
- [Documentación de Verilator](https://verilator.org/)

## Descripción de Archivos

### Ejemplos

| Archivo | Descripción | Pruebas |
|---------|-------------|---------|
| `clp_example.py` | Demostración de procesador de línea de comandos | 1 función de prueba |
| `comparator_example.py` | Demostración de comparador de transacciones | 1 función de prueba |
| `recorder_example.py` | Demostración de grabador de transacciones | 1 función de prueba |
| `pool_example.py` | Demostración de pool de objetos | 1 función de prueba |
| `queue_example.py` | Demostración de estructura de datos de cola | 1 función de prueba |
| `string_utils_example.py` | Demostración de utilidades de cadenas | 1 función de prueba |
| `math_utils_example.py` | Demostración de utilidades matemáticas | 1 función de prueba |
| `random_utils_example.py` | Demostración de utilidades aleatorias | 1 función de prueba |
| `integration_example.py` | Demostración de integración de utilidades | 1 función de prueba |

### Módulos DUT

| Archivo | Descripción | Puertos |
|---------|-------------|---------|
| `simple_dma.v` | Controlador DMA simple | `clk`, `rst_n`, `dma_start`, `dma_done`, `dma_src_addr[31:0]`, `dma_dst_addr[31:0]`, `dma_length[15:0]`, `dma_channel[2:0]` |

### Testbenches

| Archivo | Framework | Descripción | Pruebas |
|---------|-----------|-------------|---------|
| `test_utilities.py` | pyuvm | Testbench de utilidades | 1 prueba UVM |

---

Para preguntas o problemas, consulta el README principal del proyecto o revisa los registros de prueba para mensajes de error detallados.
