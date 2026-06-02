# Módulo 6: Testbenches Complejos

Este directorio contiene todos los ejemplos, ejercicios y casos de prueba para el Módulo 6, enfocado en la construcción de testbenches complejos incluyendo entornos multi-agente, verificación de protocolo, verificadores de protocolo, scoreboards multi-canal y arquitecturas de testbench en capas.

## Estructura del Directorio

```
module6/
├── examples/              # Ejemplos de pyuvm para cada tema
│   ├── multi_agent/       # Ejemplos de entornos multi-agente
│   │   └── multi_agent_example.py
│   ├── protocol/          # Ejemplos de verificación de protocolo
│   │   └── protocol_example.py
│   ├── protocol_checkers/ # Ejemplos de verificadores de protocolo
│   │   └── protocol_checker_example.py
│   ├── scoreboards/       # Ejemplos de scoreboards multi-canal
│   │   └── multi_channel_scoreboard_example.py
│   └── architecture/      # Ejemplos de arquitectura de testbench
│       └── architecture_example.py
├── dut/                   # Módulos Verilog Design Under Test
│   └── protocols/         # Módulos de protocolo para pruebas
│       └── axi4_lite_slave.v
├── tests/                 # Testbenches
│   └── pyuvm_tests/       # Testbenches pyuvm
│       └── test_complex_testbench.py
└── exercises/             # Soluciones de ejercicios (si las hay)
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

## Ejemplos de Testbenches Complejos

### 1. Entorno Multi-Agente (`examples/multi_agent/multi_agent_example.py`)

Demuestra un entorno multi-agente con coordinación de agentes:

**Conceptos Clave:**
- Instanciación de múltiples agentes
- Coordinación de agentes usando secuencias virtuales
- Integración de scoreboard multi-agente
- Ejecución paralela de agentes
- Transacciones específicas por agente

**Componentes Multi-Agente:**

1. **MultiAgentAgent**
   - Agente con driver, monitor y secuenciador
   - Contiene `agent_id` para identificación
   - Genera transacciones específicas del agente
   - Conectado al scoreboard

2. **MultiAgentScoreboard**
   - Scoreboard para múltiples agentes
   - Contiene suscriptores para cada agente
   - Rastrea transacciones por agente
   - Reporta estadísticas específicas por agente

3. **MultiAgentSubscriber**
   - Suscriptor para un agente individual
   - Recibe transacciones del monitor del agente
   - Reenvía al scoreboard padre
   - Mantiene estado específico del agente

4. **MultiAgentVirtualSequence**
   - Secuencia virtual que coordina múltiples agentes
   - Inicia secuencias en múltiples secuenciadores en paralelo
   - Usa `cocotb.start_soon()` para ejecución paralela
   - Espera a que todas las secuencias completen

**Patrones Multi-Agente:**

**Creación de Agentes:**
```python
# Crear múltiples agentes
self.agents = []
for i in range(3):
    agent = MultiAgentAgent.create(f"agent_{i}", self)
    agent.agent_id = i
    self.agents.append(agent)
```

**Conexión del Scoreboard:**
```python
# Conectar el monitor de cada agente al scoreboard
for i, agent in enumerate(self.agents):
    agent.monitor.ap.connect(self.scoreboard.subscribers[i].analysis_export)
```

**Ejecución Paralela de Secuencias:**
```python
# Iniciar secuencias en múltiples agentes en paralelo
tasks = []
for i, seqr in enumerate(self.agent_seqrs):
    seq = MultiAgentSequence(f"seq_agent_{i}", agent_id=i, num_items=3)
    task = cocotb.start_soon(seq.start(seqr))
    tasks.append(task)

# Esperar a que todas las secuencias completen
for task in tasks:
    await task
```

**Ejecutar el ejemplo:**

```bash
# Mediante el script del módulo
./scripts/module6.sh --multi-agent

# O directamente desde el directorio del ejemplo
cd module6/examples/multi_agent
make SIM=verilator TEST=multi_agent_example
```

**Salida Esperada:**
- Creación y conexión de múltiples agentes
- Ejecución paralela de secuencias
- Coordinación multi-agente
- Seguimiento de transacciones por agente

### 2. Verificación de Protocolo (`examples/protocol/protocol_example.py`)

Demuestra un agente de verificación de protocolo AXI4-Lite:

**Conceptos Clave:**
- Implementación del protocolo AXI4-Lite
- Clases de transacción específicas del protocolo
- Drivers y monitores específicos del protocolo
- Manejo de transacciones de escritura y lectura
- Patrones de verificación de protocolo

**Componentes AXI4-Lite:**

1. **AXI4LiteTransaction**
   - Transacción para operaciones AXI4-Lite
   - Campos: `addr`, `data`, `is_write`, `prot`, `strb`
   - Soporta operaciones de lectura y escritura
   - Simplificado para demostración

2. **AXI4LiteDriver**
   - Implementa el protocolo AXI4-Lite en el driver
   - Maneja transacciones de escritura (canales de dirección, datos, respuesta)
   - Maneja transacciones de lectura (canales de dirección, datos)
   - Demuestra temporización y handshaking del protocolo

3. **AXI4LiteMonitor**
   - Monitorea las señales del protocolo AXI4-Lite
   - Crea transacciones a partir de las señales monitoreadas
   - Transmite a través del puerto de análisis
   - Soporta monitoreo de escritura y lectura

4. **AXI4LiteSequence**
   - Genera transacciones AXI4-Lite
   - Crea secuencias de escritura y lectura
   - Demuestra patrones de uso del protocolo

**Protocolo AXI4-Lite:**

**Transacción de Escritura:**
- Canal de Dirección de Escritura: `AWVALID`, `AWREADY`, `AWADDR`, `AWPROT`
- Canal de Datos de Escritura: `WVALID`, `WREADY`, `WDATA`, `WSTRB`
- Canal de Respuesta de Escritura: `BVALID`, `BREADY`, `BRESP`

**Transacción de Lectura:**
- Canal de Dirección de Lectura: `ARVALID`, `ARREADY`, `ARADDR`, `ARPROT`
- Canal de Datos de Lectura: `RVALID`, `RREADY`, `RDATA`, `RRESP`

**Implementación del Protocolo:**
```python
async def write_transaction(self, txn):
    """Implement AXI4-Lite write protocol."""
    # Write Address Channel
    await Timer(5, unit="ns")
    
    # Write Data Channel
    await Timer(5, unit="ns")
    
    # Write Response Channel
    await Timer(5, unit="ns")
```

**Ejecutar el ejemplo:**

```bash
./scripts/module6.sh --protocol
# o
cd module6/examples/protocol
make SIM=verilator TEST=protocol_example
```

**Beneficios de la Verificación de Protocolo:**
- Cumplimiento de protocolos estándar
- Agentes de protocolo reutilizables
- Patrones de prueba específicos del protocolo
- Verificación según estándares de la industria

### 3. Verificador de Protocolo (`examples/protocol_checkers/protocol_checker_example.py`)

Demuestra la verificación de cumplimiento de protocolo:

**Conceptos Clave:**
- Verificación de reglas de protocolo
- Detección y reporte de errores
- Monitoreo de cumplimiento de protocolo
- Seguimiento de estado del protocolo
- Detección de violaciones de protocolo

**Componentes del Verificador de Protocolo:**

1. **ProtocolChecker**
   - Extiende `uvm_subscriber`
   - Recibe transacciones del monitor
   - Verifica reglas de protocolo
   - Rastrea errores y advertencias
   - Reporta cumplimiento de protocolo

2. **ProtocolMonitor**
   - Monitorea señales del protocolo
   - Genera transacciones de protocolo
   - Transmite al verificador de protocolo
   - Proporciona marcas de tiempo de transacciones

**Reglas de Protocolo:**

**Regla 1: Handshaking Valid/Ready**
- `valid` no debe cambiar mientras `ready` esté afirmado
- Violación: `valid` cambia durante el handshake

**Regla 2: Handshaking Ready/Valid**
- `ready` no debe cambiar mientras `valid` esté afirmado
- Violación: `ready` cambia durante el handshake

**Regla 3: Validez de Datos**
- Los datos deben ser válidos cuando `valid` y `ready` están ambos en alto
- OK: Handshake válido con transferencia de datos

**Regla 4: Valid Sin Ready**
- Advertencia si `valid` se afirma sin `ready`
- Advertencia: El protocolo puede ser ineficiente

**Verificación de Protocolo:**
```python
def write(self, txn):
    """Check protocol compliance."""
    # Check rule violations
    if self.prev_ready and self.prev_valid and txn.valid != self.prev_valid:
        error = "Protocol violation: valid changed while ready asserted"
        self.errors.append(error)
        self.logger.error(error)
    
    # Track state
    self.prev_valid = txn.valid
    self.prev_ready = txn.ready
```

**Ejecutar el ejemplo:**

```bash
./scripts/module6.sh --protocol-checkers
# o
cd module6/examples/protocol_checkers
make SIM=verilator TEST=protocol_checker_example
```

**Salida Esperada:**
- Verificación de reglas de protocolo
- Detección de errores y advertencias
- Reporte de cumplimiento de protocolo
- Seguimiento de estado del protocolo

**Beneficios del Verificador de Protocolo:**
- Verificación automática de cumplimiento de protocolo
- Detección temprana de errores
- Soporte de depuración de protocolo
- Reporte de cumplimiento

### 4. Scoreboard Multi-Canal (`examples/scoreboards/multi_channel_scoreboard_example.py`)

Demuestra la implementación de un scoreboard multi-canal:

**Conceptos Clave:**
- Verificación de múltiples canales
- Coordinación de canales
- Coincidencia basada en tiempo
- Scoreboarding específico por canal
- Verificación multi-canal

**Componentes del Scoreboard Multi-Canal:**

1. **MultiChannelScoreboard**
   - Scoreboard para múltiples canales
   - Contiene suscriptores para cada canal
   - Rastrea esperado y real por canal
   - Coincide transacciones por canal
   - Reporta estadísticas específicas por canal

2. **ChannelSubscriber**
   - Suscriptor para un canal individual
   - Recibe transacciones para un canal específico
   - Reenvía al scoreboard padre
   - Mantiene estado específico del canal

3. **ChannelMonitor**
   - Monitor para un canal
   - Genera transacciones específicas del canal
   - Transmite a través del puerto de análisis
   - Mantiene ID del canal

**Patrones Multi-Canal:**

**Creación del Scoreboard:**
```python
# Crear scoreboard con múltiples canales
self.scoreboard = MultiChannelScoreboard.create("scoreboard", self)
self.scoreboard.num_channels = 3

# Crear suscriptores para cada canal
for i in range(self.num_channels):
    subscriber = ChannelSubscriber(f"subscriber_channel_{i}", self, i)
    self.subscribers.append(subscriber)
```

**Coincidencia Específica por Canal:**
```python
def receive_transaction(self, txn, channel_id):
    """Match transaction for specific channel."""
    if len(self.expected[channel_id]) > 0:
        exp_txn = self.expected[channel_id].pop(0)
        if txn.actual == exp_txn.expected:
            self.matched[channel_id].append((exp_txn, txn))
        else:
            self.mismatches[channel_id].append((exp_txn, txn))
```

**Ejecutar el ejemplo:**

```bash
./scripts/module6.sh --scoreboards
# o
cd module6/examples/scoreboards
make SIM=verilator TEST=multi_channel_scoreboard_example
```

**Salida Esperada:**
- Creación de scoreboard multi-canal
- Seguimiento de transacciones por canal
- Coincidencia específica por canal
- Reportes de verificación multi-canal

**Beneficios del Scoreboard Multi-Canal:**
- Verificación específica por canal
- Verificación paralela de canales
- Coordinación de canales
- Verificación escalable

### 5. Arquitectura de Testbench (`examples/architecture/architecture_example.py`)

Demuestra arquitectura de testbench en capas y componentes reutilizables:

**Conceptos Clave:**
- Patrones de arquitectura en capas
- Comunicación entre capas
- Niveles de abstracción
- Reutilización de componentes
- Parameterización

**Componentes de Arquitectura:**

1. **Arquitectura en Capas:**
   - **Capa 0**: Nivel de abstracción más bajo (nivel de señales)
   - **Capa 1**: Nivel de abstracción medio (nivel de transacciones)
   - **Capa 2**: Nivel de abstracción más alto (nivel de aplicación)

2. **Componentes de Capa:**
   - **Layer0Component**: Procesamiento a nivel de señales
   - **Layer1Component**: Procesamiento a nivel de transacciones
   - **Layer2Component**: Procesamiento a nivel de aplicación

3. **Componentes Reutilizables:**
   - **ReusableComponent**: Componente configurable
   - Soporta configuración `enabled` y `mode`
   - Demuestra patrones de reutilización de componentes

**Patrones de Arquitectura en Capas:**

**Comunicación entre Capas:**
```python
# Conectar capas: Layer0 -> Layer1 -> Layer2
self.layer0.ap.connect(self.layer1.subscriber.analysis_export)
self.layer1.ap_out.connect(self.layer2.subscriber.analysis_export)
```

**Procesamiento por Capa:**
```python
# Layer 0: Signal-level
txn.layer = 0
self.ap.write(txn)

# Layer 1: Transaction-level
processed_txn.data = txn.data + 0x10
processed_txn.layer = 1
self.ap_out.write(processed_txn)

# Layer 2: Application-level
self.received.append(txn)
```

**Patrones de Componente Reutilizable:**

**Configuración de Componente:**
```python
# Crear componente reutilizable con configuración
self.comp1 = ReusableComponent.create("comp1", self)
self.comp1.config = {'enabled': True, 'mode': 'normal'}
self.comp1.enabled = True
self.comp1.mode = 'normal'
```

**Reutilización de Componente:**
```python
# Crear múltiples instancias con diferentes configuraciones
comp1: enabled=True, mode='normal'
comp2: enabled=True, mode='debug'
comp3: enabled=False, mode='normal'
```

**Ejecutar el ejemplo:**

```bash
./scripts/module6.sh --architecture
# o
cd module6/examples/architecture
make SIM=verilator TEST=architecture_example
```

**Salida Esperada:**
- Demostración de arquitectura en capas
- Comunicación entre capas
- Uso de componentes reutilizables
- Reutilización de componentes basada en configuración

**Beneficios de la Arquitectura:**
- Niveles de abstracción claros
- Componentes reutilizables
- Arquitectura escalable
- Personalización basada en configuración

## Design Under Test (DUT)

### Esclavo AXI4-Lite (`dut/protocols/axi4_lite_slave.v`)

Un esclavo AXI4-Lite simplificado para verificación de protocolo.

**Interfaz del Módulo:**
```verilog
module axi4_lite_slave (
    input  wire        ACLK,      // Señal de reloj
    input  wire        ARESETn,   // Reset activo en bajo
    
    // Canal de Dirección de Escritura
    input  wire        AWVALID,   // Dirección de escritura válida
    output reg         AWREADY,   // Dirección de escritura lista
    input  wire [31:0] AWADDR,    // Dirección de escritura
    input  wire [2:0]  AWPROT,    // Tipo de protección de escritura
    
    // Canal de Datos de Escritura
    input  wire        WVALID,    // Dato de escritura válido
    output reg         WREADY,    // Dato de escritura listo
    input  wire [31:0] WDATA,     // Dato de escritura
    input  wire [3:0]  WSTRB,     // Strobe de escritura
    
    // Canal de Respuesta de Escritura
    output reg         BVALID,    // Respuesta de escritura válida
    input  wire        BREADY,    // Respuesta de escritura lista
    output reg  [1:0]  BRESP,     // Respuesta de escritura
    
    // Canal de Dirección de Lectura
    input  wire        ARVALID,   // Dirección de lectura válida
    output reg         ARREADY,   // Dirección de lectura lista
    input  wire [31:0] ARADDR,    // Dirección de lectura
    input  wire [2:0]  ARPROT,    // Tipo de protección de lectura
    
    // Canal de Datos de Lectura
    output reg         RVALID,    // Dato de lectura válido
    input  wire        RREADY,    // Dato de lectura listo
    output reg  [31:0] RDATA,     // Dato de lectura
    output reg  [1:0]  RRESP      // Respuesta de lectura
);
```

**Funcionalidad:**
- Memoria de 4KB (1024 palabras × 32 bits)
- Transacciones de escritura: Dirección → Dato → Respuesta
- Transacciones de lectura: Dirección → Dato
- Máquinas de estado para operaciones de escritura y lectura
- Handshaking en todos los canales
- Códigos de respuesta: OKAY (00), EXOKAY (01), SLVERR (10), DECERR (11)

**Características:**
- Implementación AXI4-Lite simplificada
- Operación síncrona con reset asíncrono
- Máquinas de estado separadas para escritura y lectura
- Almacenamiento basado en memoria
- Adecuado para verificación de protocolo

**Soporte de Protocolo:**
- Handshaking del canal de dirección de escritura
- Handshaking del canal de datos de escritura
- Handshaking del canal de respuesta de escritura
- Handshaking del canal de dirección de lectura
- Handshaking del canal de datos de lectura

## Testbenches

### Pruebas pyuvm (`tests/pyuvm_tests/`)

#### Prueba de Testbench Complejo (`test_complex_testbench.py`)

Testbench UVM completo que demuestra la construcción de testbenches complejos:

**Componentes UVM:**

1. **Transaction (`ComplexTransaction`)**
   - Contiene campos `data`, `address` y `channel`
   - Utilizado para pruebas de testbench complejo

2. **Sequence (`ComplexSequence`)**
   - Genera transacciones de prueba
   - Crea y envía transacciones

3. **Driver (`ComplexDriver`)**
   - Recibe transacciones del secuenciador
   - Maneja las entradas del DUT (patrón mostrado)

4. **Monitor (`ComplexMonitor`)**
   - Muestrea las salidas del DUT
   - Crea transacciones a partir de los datos muestreados
   - Transmite a través del puerto de análisis

5. **Scoreboard (`ComplexScoreboard`)**
   - Extiende `uvm_subscriber`
   - Recibe transacciones del monitor
   - Rastrea transacciones recibidas

6. **Agent (`ComplexAgent`)**
   - Contiene driver, monitor y secuenciador
   - Conecta componentes

7. **Environment (`ComplexEnv`)**
   - Contiene agente y scoreboard
   - Conecta el monitor con el scoreboard

8. **Test (`ComplexTestbenchTest`)**
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
./scripts/module6.sh --pyuvm-tests

# Directamente desde el directorio de pruebas
cd module6/tests/pyuvm_tests
make SIM=verilator TEST=test_complex_testbench
```

**Resultados Esperados:**
- 1 caso de prueba exitoso
- Todos los componentes creados y conectados
- Ejecución de secuencia demostrada
- Seguimiento de scoreboard demostrado
- Conceptos de testbench complejo integrados

## Ejecutar Ejemplos y Pruebas

### Usando el Script del Módulo

El script `module6.sh` proporciona una forma conveniente de ejecutar todos los ejemplos y pruebas:

```bash
# Ejecutar todo (todos los ejemplos + todas las pruebas)
./scripts/module6.sh

# Ejecutar solo ejemplos
./scripts/module6.sh --all-examples

# Ejecutar solo pruebas
./scripts/module6.sh --pyuvm-tests

# Ejecutar ejemplos específicos
./scripts/module6.sh --multi-agent
./scripts/module6.sh --protocol
./scripts/module6.sh --protocol-checkers
./scripts/module6.sh --scoreboards
./scripts/module6.sh --architecture

# Combinar opciones
./scripts/module6.sh --multi-agent --protocol --pyuvm-tests
```

### Ejecutar Ejemplos Individuales

#### Ejecución Directa desde el Directorio del Ejemplo

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio del ejemplo
cd module6/examples/multi_agent

# Ejecutar ejemplo
make SIM=verilator TEST=multi_agent_example

# Limpiar artefactos de compilación
make clean
```

#### Ejecutar Todos los Ejemplos Secuencialmente

```bash
cd module6/examples

# Multi-agent
cd multi_agent && make SIM=verilator TEST=multi_agent_example && cd ..

# Protocol
cd protocol && make SIM=verilator TEST=protocol_example && cd ..

# Protocol checkers
cd protocol_checkers && make SIM=verilator TEST=protocol_checker_example && cd ..

# Scoreboards
cd scoreboards && make SIM=verilator TEST=multi_channel_scoreboard_example && cd ..

# Architecture
cd architecture && make SIM=verilator TEST=architecture_example && cd ..
```

### Ejecutar Pruebas pyuvm

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio de pruebas
cd module6/tests/pyuvm_tests

# Ejecutar prueba
make SIM=verilator TEST=test_complex_testbench

# Limpiar artefactos de compilación
make clean
```

## Resultados de las Pruebas

Cuando las pruebas se completen exitosamente, deberías ver una salida similar a:

### Salida de Ejemplo de Prueba

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** multi_agent_example.test_multi_agent           PASS         200.00           0.00     123456.78  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 200.00           0.00      12345.67  **
```

### Conteo Esperado de Pruebas

- **Ejemplo multi-agente**: 1 prueba
- **Ejemplo de protocolo**: 1 prueba
- **Ejemplo de verificador de protocolo**: 1 prueba
- **Ejemplo de scoreboard multi-canal**: 1 prueba
- **Ejemplo de arquitectura**: 1 prueba
- **Prueba de testbench complejo**: 1 prueba
- **Total**: 6 pruebas en todos los ejemplos y testbenches

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

#### 3. Problemas de Coordinación Multi-Agente

**Error:** Los agentes no se coordinan correctamente

**Solución:**
- Verifica que la secuencia virtual tenga referencias a todos los secuenciadores
- Comprueba que la ejecución paralela use `cocotb.start_soon()` correctamente
- Asegúrate de que todas las secuencias sean esperadas con await
- Verifica las conexiones del scoreboard para todos los agentes

#### 4. Problemas de Verificación de Protocolo

**Error:** Las transacciones de protocolo fallan

**Solución:**
- Verifica que las señales del protocolo estén conectadas correctamente
- Comprueba que la temporización del protocolo coincida con la especificación
- Asegúrate de que las señales de handshaking sean correctas
- Verifica que los campos de las transacciones coincidan con el protocolo

#### 5. El Verificador de Protocolo No Detecta Violaciones

**Error:** El verificador de protocolo no reporta violaciones

**Solución:**
- Verifica que el monitor esté generando transacciones correctamente
- Comprueba que las reglas de protocolo estén implementadas correctamente
- Asegúrate de que el seguimiento de estado esté funcionando
- Verifica que el verificador reciba transacciones del monitor

#### 6. Discrepancias en el Scoreboard Multi-Canal

**Error:** El scoreboard reporta discrepancias incorrectamente

**Solución:**
- Verifica que los IDs de canal sean correctos
- Comprueba que las transacciones esperadas se añadan para los canales correctos
- Asegúrate de que la lógica de coincidencia específica por canal sea correcta
- Verifica las conexiones de los suscriptores por canal

#### 7. Problemas de Comunicación entre Capas de Arquitectura

**Error:** Las capas no se comunican correctamente

**Solución:**
- Verifica las conexiones entre capas en `connect_phase()`
- Comprueba las conexiones de puertos de análisis entre capas
- Asegúrate de que los métodos `write()` de los suscriptores reenvíen correctamente
- Verifica el orden de procesamiento de las capas

### Consejos de Depuración

1. **Verificar Coordinación Multi-Agente:**
   ```python
   # Verify agent sequencers are set
   self.logger.info(f"Agent sequencers: {self.agent_seqrs}")
   ```

2. **Monitorear Transacciones de Protocolo:**
   ```python
   # Add logging in protocol driver
   self.logger.info(f"Protocol transaction: {txn}")
   ```

3. **Verificar Cumplimiento de Protocolo:**
   ```python
   # Verify protocol checker receives transactions
   self.logger.info(f"Protocol checker errors: {len(self.errors)}")
   ```

4. **Inspeccionar Scoreboard Multi-Canal:**
   ```python
   # Check channel-specific data
   self.logger.info(f"Channel {channel_id}: expected={len(self.expected[channel_id])}, actual={len(self.actual[channel_id])}")
   ```

5. **Verificar Conexiones entre Capas:**
   ```python
   # Check layer connections
   self.logger.info(f"Layer0 -> Layer1: {self.layer0.ap} -> {self.layer1.subscriber}")
   ```

## Temas Cubiertos

1. **Entornos Multi-Agente** - Coordinación de múltiples agentes, ejecución paralela
2. **Verificación de Protocolo** - Protocolo AXI4-Lite, agentes específicos de protocolo
3. **Verificadores de Protocolo** - Verificación de cumplimiento de protocolo, validación de reglas
4. **Scoreboards Multi-Canal** - Verificación específica por canal, verificación paralela
5. **Arquitectura de Testbench** - Arquitectura en capas, componentes reutilizables
6. **Depuración y Análisis** - Técnicas avanzadas de depuración, patrones de análisis
7. **Verificación Multi-Canal** - Coordinación de canales, verificación paralela
8. **Verificación de Rendimiento** - Monitoreo de rendimiento, análisis de throughput
9. **Inyección de Errores** - Patrones de inyección y recuperación de errores
10. **Integración de Testbench** - Integración de componentes, verificación a nivel de sistema

## Próximos Pasos

Después de completar el Módulo 6, continúa con:

- **Módulo 7**: Temas Avanzados - DMA, integración VIP, mejores prácticas
- **Módulo 8**: Utilidades Avanzadas - CLP, comparadores, pools, colas, grabadores

## Recursos Adicionales

- [Documentación de pyuvm](https://pyuvm.readthedocs.io/)
- [Guía de Usuario de UVM](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_1.2.pdf)
- [Especificación del Protocolo AXI4](https://developer.arm.com/documentation/ihi0022/latest/)
- [Documentación de cocotb](https://docs.cocotb.org/)
- [Documentación de Verilator](https://verilator.org/)

## Descripción de Archivos

### Ejemplos

| Archivo | Descripción | Pruebas |
|---------|-------------|---------|
| `multi_agent_example.py` | Coordinación de entorno multi-agente | 1 función de prueba |
| `protocol_example.py` | Verificación de protocolo AXI4-Lite | 1 función de prueba |
| `protocol_checker_example.py` | Verificación de cumplimiento de protocolo | 1 función de prueba |
| `multi_channel_scoreboard_example.py` | Scoreboard multi-canal | 1 función de prueba |
| `architecture_example.py` | Arquitectura en capas y componentes reutilizables | 1 función de prueba |

### Módulos DUT

| Archivo | Descripción | Puertos |
|---------|-------------|---------|
| `axi4_lite_slave.v` | Interfaz esclavo AXI4-Lite | `ACLK`, `ARESETn`, `AWVALID`, `AWREADY`, `AWADDR`, `AWPROT`, `WVALID`, `WREADY`, `WDATA`, `WSTRB`, `BVALID`, `BREADY`, `BRESP`, `ARVALID`, `ARREADY`, `ARADDR`, `ARPROT`, `RVALID`, `RREADY`, `RDATA`, `RRESP` |

### Testbenches

| Archivo | Framework | Descripción | Pruebas |
|---------|-----------|-------------|---------|
| `test_complex_testbench.py` | pyuvm | Prueba de testbench complejo | 1 prueba UVM |

---

Para preguntas o problemas, consulta el README principal del proyecto o revisa los registros de prueba para mensajes de error detallados.
