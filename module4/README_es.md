# Módulo 4: Componentes UVM

Este directorio contiene todos los ejemplos, ejercicios y casos de prueba del Módulo 4, enfocado en la implementación de componentes UVM, incluyendo transacciones, drivers, monitores, sequencers, comunicación TLM, scoreboards y agentes completos.

## Estructura del Directorio

```
module4/
├── examples/              # ejemplos de pyuvm para cada tema
│   ├── transactions/     # ejemplos de modelado de transacciones
│   │   └── transaction_example.py
│   ├── drivers/          # ejemplos de implementación de drivers
│   │   └── driver_example.py
│   ├── monitors/         # ejemplos de implementación de monitores
│   │   └── monitor_example.py
│   ├── sequencers/       # ejemplos de sequencers y secuencias
│   │   └── sequencer_example.py
│   ├── tlm/              # ejemplos de comunicación TLM
│   │   └── tlm_example.py
│   ├── scoreboards/      # ejemplos de scoreboards
│   │   └── scoreboard_example.py
│   └── agents/           # ejemplos de agentes completos
│       └── agent_example.py
├── dut/                   # módulos Verilog del Design Under Test
│   └── interfaces/       # módulos de interfaz para pruebas
│       └── simple_interface.v
├── tests/                 # bancos de prueba
│   └── pyuvm_tests/      # bancos de prueba pyuvm
│       └── test_complete_agent.py
└── exercises/            # soluciones de ejercicios (si las hay)
```

## Requisitos Previos

Antes de ejecutar los experimentos, asegúrate de tener:

- **Python 3.8+** - Requerido para cocotb y pyuvm
- **Verilator 5.036+** - Requerido para la simulación (se recomienda 5.044)
- **cocotb 2.0+** - Instalado en el entorno virtual
- **pyuvm 4.0+** - Instalado en el entorno virtual
- **Make** - Para construir y ejecutar pruebas

Para verificar tu entorno:

```bash
python3 --version        # Debe ser 3.8+
verilator --version      # Debe ser 5.036+
python3 -c "import cocotb; print(cocotb.__version__)"
python3 -c "import pyuvm; print(pyuvm.__version__)"
```

## Ejemplos de Componentes UVM

### 1. Transacciones (`examples/transactions/transaction_example.py`)

Demuestra modelado a nivel de transacción y operaciones sobre transacciones:

**Conceptos Clave:**
- Diseño de clases de transacción que extienden `uvm_sequence_item`
- Campos de transacción y miembros de datos
- Operaciones de copia y comparación de transacciones
- Transacciones extendidas con herencia
- Transacciones aleatorias con restricciones
- Métodos de empaquetado/desempaquetado de transacciones

**Clases de Transacción:**

1. **BaseTransaction**
   - Transacción básica con campos `data` y `address`
   - Implementa los métodos `__str__()`, `__eq__()` y `copy()`
   - Demuestra la comparación de igualdad entre transacciones

2. **ExtendedTransaction**
   - Extiende `BaseTransaction` con los campos `control` y `status`
   - Muestra patrones de herencia en transacciones
   - Demuestra lógica de comparación extendida

3. **ConstrainedTransaction**
   - Transacción con restricciones de aleatorización
   - Restricción de alineación de direcciones (límite de 4 bytes)
   - Restricción de datos no nulos

4. **TransactionWithMethods**
   - Demuestra métodos útiles de transacción
   - `pack()` - Serializa la transacción a bytes
   - `unpack()` - Deserializa bytes a una transacción
   - `convert2string()` - Representación en cadena
   - `do_copy()` - Método de copia de UVM
   - `do_compare()` - Método de comparación de UVM

**Ejecución del ejemplo:**

```bash
# Mediante el script del módulo
./scripts/module4.sh --transactions

# O directamente desde el directorio del ejemplo
cd module4/examples/transactions
make SIM=verilator TEST=transaction_example
```

**Salida Esperada:**
- Creación y manipulación de transacciones
- Operaciones de copia y comparación
- Ejemplos de transacciones extendidas
- Aleatorización con restricciones
- Operaciones de empaquetado/desempaquetado

### 2. Drivers (`examples/drivers/driver_example.py`)

Demuestra la implementación de un driver UVM:

**Conceptos Clave:**
- Estructura de clase driver que extiende `uvm_driver`
- Recepción de transacciones desde el sequencer mediante `seq_item_port`
- Conducción de señales hacia el DUT
- Comunicación entre driver y sequencer
- Patrones de conducción específicos del protocolo

**Clases de Driver:**

1. **SimpleDriver**
   - Implementación básica de driver
   - Recibe transacciones desde el sequencer
   - Conduce señales del DUT (se muestra el patrón)
   - Señaliza la finalización de la transacción

2. **ProtocolDriver**
   - Driver consciente del protocolo
   - Implementa handshaking (request/grant)
   - Control de tiempos del protocolo
   - Demuestra patrones específicos del protocolo

**Flujo del Driver:**
1. `build_phase()` - Crea `seq_item_port`
2. `connect_phase()` - Conecta al sequencer
3. `run_phase()` - Bucle principal del driver:
   - `get_next_item()` - Obtiene la transacción del sequencer
   - `drive_transaction()` - Conduce señales hacia el DUT
   - `item_done()` - Señala la finalización

**Ejecución del ejemplo:**

```bash
./scripts/module4.sh --drivers
# or
cd module4/examples/drivers
make SIM=verilator TEST=driver_example
```

**Patrones de Driver:**
- Bucle continuo en `run_phase()`
- Actualizaciones de señales guiadas por transacciones
- Implementación del tiempo del protocolo
- Handshaking con el DUT

### 3. Monitores (`examples/monitors/monitor_example.py`)

Demuestra la implementación de un monitor UVM:

**Conceptos Clave:**
- Estructura de clase monitor que extiende `uvm_monitor`
- Muestreo de señales del DUT
- Creación de transacciones a partir de señales muestreadas
- Difusión mediante analysis port
- Monitoreo consciente del protocolo

**Clases de Monitor:**

1. **SimpleMonitor**
   - Implementación básica de monitor
   - Muestrea señales del DUT
   - Crea transacciones a partir de los datos muestreados
   - Difunde mediante analysis port

2. **ProtocolMonitor**
   - Monitoreo consciente del protocolo
   - Espera eventos del protocolo
   - Muestrea en condiciones específicas del protocolo
   - Lleva un conteo de muestras

**Flujo del Monitor:**
1. `build_phase()` - Crea `analysis_port`
2. `run_phase()` - Bucle principal del monitor:
   - `sample_signals()` - Muestra señales del DUT
   - Crea una transacción a partir de los datos muestreados
   - `ap.write()` - Difunde mediante analysis port

**Ejecución del ejemplo:**

```bash
./scripts/module4.sh --monitors
# or
cd module4/examples/monitors
make SIM=verilator TEST=monitor_example
```

**Patrones de Monitor:**
- Bucle de monitoreo continuo
- Muestreo impulsado por eventos
- Creación y difusión de transacciones
- Muestreo específico del protocolo

### 4. Sequencers (`examples/sequencers/sequencer_example.py`)

Demuestra la implementación de sequencer y secuencias UVM:

**Conceptos Clave:**
- Clase sequencer (`uvm_sequencer`)
- Clase sequence que extiende `uvm_sequence`
- Implementación del cuerpo de la secuencia
- Generación de transacciones en secuencias
- Estratificación y composición de secuencias
- Generación de secuencias aleatorias

**Clases de Secuencia:**

1. **SimpleSequence**
   - Implementación básica de secuencia
   - Genera vectores de prueba fijos
   - Usa `start_item()` y `finish_item()`
   - Demuestra la ejecución de secuencias

2. **RandomSequence**
   - Generación aleatoria de transacciones
   - Número configurable de elementos
   - Valores aleatorios con restricciones
   - Patrón de secuencia reutilizable

3. **LayeredSequence**
   - Composición de secuencias
   - Llama a otras secuencias
   - Estructura jerárquica de secuencias
   - Demuestra la reutilización de secuencias

**Flujo de Secuencia:**
1. `body()` - Método de ejecución de la secuencia
2. `start_item(txn)` - Solicita una transacción al sequencer
3. `finish_item(txn)` - Envía la transacción al driver
4. La secuencia termina cuando `body()` retorna

**Ejecución del ejemplo:**

```bash
./scripts/module4.sh --sequencers
# or
cd module4/examples/sequencers
make SIM=verilator TEST=sequencer_example
```

**Patrones de Secuencia:**
- Bucles de generación de transacciones
- Secuencias aleatorias vs deterministas
- Composición de secuencias
- Bibliotecas de secuencias reutilizables

### 5. TLM (`examples/tlm/tlm_example.py`)

Demuestra interfaces de Transaction-Level Modeling (TLM):

**Conceptos Clave:**
- Puertos, exports e implementaciones TLM
- Interfaz put (productor-consumidor)
- Interfaz get (proveedor-consumidor)
- Interfaz transport (request-response)
- FIFO TLM para buffering
- Conexiones y comunicación TLM

**Interfaces TLM:**

1. **Interfaz Put**
   - `PutProducer` - Usa `uvm_put_port`
   - `PutConsumer` - Implementa `uvm_put_export`
   - Métodos: `put()`, `try_put()`, `can_put()`

2. **Interfaz Get**
   - `GetProducer` - Implementa `uvm_get_export`
   - `GetConsumer` - Usa `uvm_get_port`
   - Métodos: `get()`, `try_get()`, `can_get()`

3. **Interfaz Transport**
   - `TransportComponent` - Implementa `uvm_transport_export`
   - Patrón request-response
   - Métodos: `transport()`, `nb_transport()`

4. **FIFO TLM**
   - `uvm_tlm_fifo` - Comunicación con buffering
   - `FIFOProducer` - Produce hacia el FIFO
   - `FIFOConsumer` - Consume desde el FIFO

**Conexión TLM:**
```python
# Interfaz put
producer.put_port.connect(consumer)

# Interfaz get
consumer.get_port.connect(producer)

# FIFO
producer.put_port.connect(fifo.put_export)
consumer.get_port.connect(fifo.get_export)
```

**Ejecución del ejemplo:**

```bash
./scripts/module4.sh --tlm
# or
cd module4/examples/tlm
make SIM=verilator TEST=tlm_example
```

**Beneficios de TLM:**
- Comunicación desacoplada entre componentes
- Abstracción a nivel de transacción
- Patrones de conexión flexibles
- Interfaces de comunicación reutilizables

### 6. Scoreboards (`examples/scoreboards/scoreboard_example.py`)

Demuestra la implementación de scoreboards para verificación de resultados:

**Conceptos Clave:**
- Clase scoreboard que extiende `uvm_subscriber`
- Conexiones de analysis port
- Comparación entre esperado y observado
- Detección y reporte de discrepancias
- Integración con modelos de referencia

**Clases de Scoreboard:**

1. **SimpleScoreboard**
   - Implementación básica de scoreboard
   - Almacena transacciones esperadas y reales
   - Compara y reporta discrepancias
   - Proporciona estadísticas en `check_phase()`

2. **ReferenceModelScoreboard**
   - Scoreboard con modelo de referencia
   - Calcula valores esperados dinámicamente
   - Compara con la salida del modelo de referencia
   - Demuestra el patrón de referencia dorada

**Flujo del Scoreboard:**
1. `build_phase()` - Inicializa el almacenamiento
2. `write(txn)` - Recibe transacciones del monitor
3. Compara con lo esperado (o con el modelo de referencia)
4. `check_phase()` - Verificación y reporte final

**Ejecución del ejemplo:**

```bash
./scripts/module4.sh --scoreboards
# or
cd module4/examples/scoreboards
make SIM=verilator TEST=scoreboard_example
```

**Patrones de Scoreboard:**
- Gestión de colas esperadas
- Lógica de comparación de transacciones
- Seguimiento de discrepancias
- Integración con modelos de referencia
- Reporte de estadísticas

### 7. Agentes (`examples/agents/agent_example.py`)

Demuestra la implementación de un agente completo:

**Conceptos Clave:**
- Estructura de clase agent que extiende `uvm_agent`
- Configuración de agente activo vs pasivo
- Integración de componentes (driver, monitor, sequencer)
- Conexiones entre componentes
- Configuración del agente mediante ConfigDB

**Componentes del Agente:**

1. **CompleteAgent**
   - Contiene driver, monitor y sequencer
   - Configuración activa/pasiva
   - Creación y conexión de componentes
   - Demuestra la estructura completa del agente

2. **AgentDriver**
   - Conduce transacciones hacia el DUT
   - Conectado al sequencer

3. **AgentMonitor**
   - Muestrea señales del DUT
   - Difunde mediante analysis port

4. **AgentSequence**
   - Genera transacciones de prueba
   - Las envía al sequencer

**Modos del Agente:**

- **Agente Activo**: Contiene driver, sequencer y monitor
  - Se usa para verificación activa

- **Agente Pasivo**: Contiene solo el monitor
  - Observa únicamente el DUT
  - Se usa para monitoreo pasivo o verificación de referencia

**Ejecución del ejemplo:**

```bash
./scripts/module4.sh --agents
# or
cd module4/examples/agents
make SIM=verilator TEST=agent_example
```

**Casos de Prueba:**
1. `test_complete_agent` - Demostración de agente activo
2. `test_passive_agent` - Demostración de agente pasivo

**Salida Esperada:**
- Creación de componentes del agente
- Configuración de modo activo/pasivo
- Conexiones entre componentes
- Demostración de la operación del agente

## Design Under Test (DUT)

### Interfaz Simple (`dut/interfaces/simple_interface.v`)

Un módulo de interfaz simple para pruebas de componentes UVM.

**Interfaz del Módulo:**
```verilog
module simple_interface (
    input  wire       clk,      // señal de reloj
    input  wire       rst_n,    // reset activo en bajo
    input  wire       valid,    // señal de validez
    output reg        ready,    // señal de disponibilidad
    input  wire [7:0] data,     // bus de datos (8 bits)
    input  wire [15:0] address,  // bus de direcciones (16 bits)
    output reg  [7:0] result    // salida de resultado (8 bits)
);
```

**Funcionamiento:**
- Se reinicia a ceros cuando `rst_n` está en bajo
- Cuando `valid` se afirma, establece `ready` y calcula `result = data + 1`
- Protocolo simple de handshaking (valid/ready)
- Demuestra una interfaz básica para pruebas de componentes UVM

**Características:**
- Operación síncrona con reset asíncrono
- Handshaking valid/ready
- Transformación simple de datos (incremento)
- Adecuado para demostración de componentes UVM

**Protocolo:**
- El driver afirma `valid` con `data` y `address`
- El DUT responde con `ready` y `result = data + 1`
- El monitor muestrea `ready` y `result`

## Bancos de Prueba

### Pruebas pyuvm (`tests/pyuvm_tests/`)

#### Prueba de Agente Completo (`test_complete_agent.py`)

Banco de prueba UVM completo que demuestra la integración de todos los componentes:

**Componentes UVM:**

1. **Transacción (`InterfaceTransaction`)**
   - Contiene `data`, `address` y `expected_result`
   - Se usa para estímulo y comprobación

2. **Secuencia (`InterfaceSequence`)**
   - Genera vectores de prueba
   - Crea y envía transacciones

3. **Driver (`InterfaceDriver`)**
   - Recibe transacciones del sequencer
   - Conduce las entradas del DUT (se muestra el patrón)

4. **Monitor (`InterfaceMonitor`)**
   - Muestrea las salidas del DUT
   - Crea transacciones a partir de datos muestreados
   - Difunde mediante analysis port

5. **Scoreboard (`InterfaceScoreboard`)**
   - Recibe transacciones del monitor
   - Compara esperado vs real
   - Reporta discrepancias

6. **Agente (`InterfaceAgent`)**
   - Contiene driver, monitor y sequencer
   - Conecta componentes

7. **Entorno (`InterfaceEnv`)**
   - Contiene agente y scoreboard
   - Conecta el monitor al scoreboard

8. **Prueba (`CompleteAgentTest`)**
   - Clase de prueba de nivel superior
   - Crea el entorno y ejecuta la prueba

**Flujo de la Prueba:**
1. `build_phase()` - Crea todos los componentes
2. `connect_phase()` - Conecta los componentes
3. `run_phase()` - Ejecuta la prueba (aquí se iniciaría la secuencia)
4. `check_phase()` - Verifica resultados en el scoreboard
5. `report_phase()` - Genera el informe de la prueba

**Ejecución de la prueba:**

```bash
# Mediante el script del módulo
./scripts/module4.sh --pyuvm-tests

# Directamente desde el directorio de pruebas
cd module4/tests/pyuvm_tests
make SIM=verilator TEST=test_complete_agent
```

**Resultados Esperados:**
- 1 caso de prueba aprobado
- Todos los componentes creados y conectados
- Integración de componentes demostrada
- Verificación del scoreboard completada

## Ejecución de Ejemplos y Pruebas

### Uso del Script del Módulo

El script `module4.sh` ofrece una forma conveniente de ejecutar todos los ejemplos y pruebas:

```bash
# Ejecutar todo (todos los ejemplos + todas las pruebas)
./scripts/module4.sh

# Ejecutar solo ejemplos
./scripts/module4.sh --all-examples

# Ejecutar solo pruebas
./scripts/module4.sh --pyuvm-tests

# Ejecutar ejemplos específicos
./scripts/module4.sh --transactions
./scripts/module4.sh --drivers
./scripts/module4.sh --monitors
./scripts/module4.sh --sequencers
./scripts/module4.sh --tlm
./scripts/module4.sh --scoreboards
./scripts/module4.sh --agents

# Combinar opciones
./scripts/module4.sh --drivers --monitors --tlm --pyuvm-tests
```

### Ejecución de Ejemplos Individuales

#### Ejecución Directa desde el Directorio del Ejemplo

```bash
# Activar el entorno virtual
source .venv/bin/activate

# Cambiar al directorio del ejemplo
cd module4/examples/drivers

# Ejecutar el ejemplo
make SIM=verilator TEST=driver_example

# Limpiar artefactos de compilación
make clean
```

#### Ejecución Secuencial de Todos los Ejemplos

```bash
cd module4/examples

# Transactions
cd transactions && make SIM=verilator TEST=transaction_example && cd ..

# Drivers
cd drivers && make SIM=verilator TEST=driver_example && cd ..

# Monitors
cd monitors && make SIM=verilator TEST=monitor_example && cd ..

# Sequencers
cd sequencers && make SIM=verilator TEST=sequencer_example && cd ..

# TLM
cd tlm && make SIM=verilator TEST=tlm_example && cd ..

# Scoreboards
cd scoreboards && make SIM=verilator TEST=scoreboard_example && cd ..

# Agents
cd agents && make SIM=verilator TEST=agent_example && cd ..
```

### Ejecución de Pruebas pyuvm

```bash
# Activar el entorno virtual
source .venv/bin/activate

# Cambiar al directorio de pruebas
cd module4/tests/pyuvm_tests

# Ejecutar la prueba
make SIM=verilator TEST=test_complete_agent

# Limpiar artefactos de compilación
make clean
```

## Resultados de Prueba

Cuando las pruebas se ejecutan correctamente, deberías ver una salida similar a esta:

### Salida de Ejemplo de Prueba

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** transaction_example.test_transaction           PASS          10.00           0.00      12256.88  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 10.00           0.00       7345.54  **
```

### Conteos Esperados de Pruebas

- **Ejemplo de transacciones**: 1 prueba
- **Ejemplo de driver**: 1 prueba
- **Ejemplo de monitor**: 1 prueba
- **Ejemplo de sequencer**: 1 prueba
- **Ejemplo de TLM**: 1 prueba
- **Ejemplo de scoreboard**: 1 prueba
- **Ejemplo de agente**: 2 pruebas (activa y pasiva)
- **Prueba de agente completo**: 1 prueba
- **Total**: 9 pruebas entre todos los ejemplos y bancos de prueba

## Resolución de Problemas

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

#### 3. Errores de Importación TLM

**Error:** `NameError: name 'uvm_put_imp' is not defined`

**Solución:** Algunas clases TLM pueden necesitar imports explícitos. Los ejemplos incluyen lógica de importación de respaldo. Si el problema persiste, revisa la compatibilidad de la versión de pyuvm.

#### 4. La Secuencia No Se Inicia

**Error:** La secuencia no se ejecuta o se queda colgada

**Solución:**
- Asegúrate de que el sequencer esté conectado al driver
- Verifica que la secuencia se inicie con la referencia correcta al sequencer
- Comprueba que el método `body()` sea async y use `await`
- Asegúrate de que la prueba levante una objection antes de iniciar la secuencia

#### 5. El Driver No Recibe Transacciones

**Error:** El bucle del driver no recibe transacciones

**Solución:**
- Verifica que `seq_item_port` esté conectado al `seq_item_export` del sequencer
- Comprueba que la conexión se haga en `connect_phase()`
- Asegúrate de que la secuencia se inicie en el sequencer correcto
- Verifica que el sequencer se cree en `build_phase()` del agente

#### 6. El Monitor No Difunde

**Error:** El scoreboard no recibe transacciones del monitor

**Solución:**
- Verifica que el `analysis_port` del monitor esté conectado al `analysis_export` del scoreboard
- Comprueba que la conexión se haga en `connect_phase()` del entorno
- Asegúrate de que el monitor llame a `ap.write(txn)` después del muestreo
- Verifica que el scoreboard extienda `uvm_subscriber` (proporciona `analysis_export`)

#### 7. Discrepancias en el Scoreboard

**Error:** El scoreboard reporta discrepancias inesperadas

**Solución:**
- Verifica que las transacciones esperadas se agreguen antes de que lleguen las transacciones reales
- Revisa la lógica de comparación de transacciones
- Asegúrate de que los campos de transacción coincidan (tipos de datos, valores)
- Revisa el modelo de referencia si estás usando uno

### Consejos de Depuración

1. **Revisa las Conexiones de Componentes:**
   ```python
   # Imprime la jerarquía de componentes
   self.print_topology()
   ```

2. **Verifica las Conexiones TLM:**
   ```python
   # Comprueba si los puertos están conectados
   if self.put_port.is_connected():
       self.logger.info("Put port is connected")
   ```

3. **Monitorea el Flujo de Transacciones:**
   ```python
   # Agrega logging en el driver
   self.logger.info(f"Received transaction: {item}")
   
   # Agrega logging en el monitor
   self.logger.info(f"Sampled transaction: {txn}")
   
   # Agrega logging en el scoreboard
   self.logger.info(f"Received for checking: {txn}")
   ```

4. **Revisa la Ejecución de la Secuencia:**
   ```python
   # Verifica que la secuencia se haya iniciado
   seq = MySequence.create("seq")
   await seq.start(self.env.agent.seqr)
   self.logger.info("Sequence started")
   ```

5. **Verifica la Configuración del Agente:**
   ```python
   # Revisa el modo del agente
   self.logger.info(f"Agent active: {self.active}")
   ```

6. **Inspecciona el Contenido de la Transacción:**
   ```python
   # Imprime detalles de la transacción
   self.logger.info(f"Transaction: {txn}")
   self.logger.info(f"Transaction data: 0x{txn.data:02X}")
   ```

## Temas Cubiertos

1. **Modelado de Transacciones** - Diseño de clases de transacción, operaciones y métodos
2. **Implementación de Drivers** - Recepción de transacciones, conducción de señales, implementación de protocolos
3. **Implementación de Monitores** - Muestreo de señales, creación de transacciones, analysis ports
4. **Sequencer y Secuencias** - Generación, ejecución y composición de secuencias
5. **Comunicación TLM** - Interfaces Put/Get/Transport, puertos, exports, FIFOs
6. **Implementación de Scoreboards** - Comparación esperado vs real, modelos de referencia
7. **Agente Completo** - Estructura del agente, modos activo/pasivo, integración de componentes
8. **Conexiones de Componentes** - Conexiones puerto/export, interfaces TLM
9. **Arquitectura del Agente** - Integración driver-monitor-sequencer
10. **Integración del Banco de Pruebas** - Estructura del entorno, ensamblado de componentes

## Próximos Pasos

Después de completar el Módulo 4, continúa con:

- **Módulo 5**: UVM Avanzado - Callbacks, cobertura, modelo de registros, secuencias virtuales
- **Módulo 6**: Verificación de Protocolos - Bancos de prueba multiagente, verificadores de protocolo
- **Módulo 7**: Temas Avanzados - DMA, integración de VIP, mejores prácticas
- **Módulo 8**: Utilidades Avanzadas - CLP, comparadores, pools, colas, recorders

## Recursos Adicionales

- [pyuvm Documentation](https://pyuvm.readthedocs.io/)
- [UVM User's Guide](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_1.2.pdf)
- [cocotb Documentation](https://docs.cocotb.org/)
- [Verilator Documentation](https://verilator.org/)

## Descripción de Archivos

### Ejemplos

| Archivo | Descripción | Pruebas |
|------|-------------|-------|
| `transaction_example.py` | Modelado y operaciones de transacciones | 1 función de prueba |
| `driver_example.py` | Patrones de implementación de drivers | 1 función de prueba |
| `monitor_example.py` | Patrones de implementación de monitores | 1 función de prueba |
| `sequencer_example.py` | Patrones de sequencer y secuencia | 1 función de prueba |
| `tlm_example.py` | Interfaces de comunicación TLM | 1 función de prueba |
| `scoreboard_example.py` | Implementación de scoreboard | 1 función de prueba |
| `agent_example.py` | Implementación de agente completo | 2 funciones de prueba |

### Módulos DUT

| Archivo | Descripción | Puertos |
|------|-------------|-------|
| `simple_interface.v` | Interfaz simple para pruebas de componentes | `clk`, `rst_n`, `valid`, `ready`, `data[7:0]`, `address[15:0]`, `result[7:0]` |

### Bancos de Prueba

| Archivo | Framework | Descripción | Pruebas |
|------|-----------|-------------|-------|
| `test_complete_agent.py` | pyuvm | Banco de prueba de agente completo | 1 prueba UVM |

---

Si tienes preguntas o problemas, consulta el README principal del proyecto o revisa los logs de prueba para obtener mensajes de error detallados.