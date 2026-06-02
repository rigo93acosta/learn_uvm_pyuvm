# Módulo 5: Conceptos Avanzados de UVM

Este directorio contiene todos los ejemplos, ejercicios y casos de prueba para el Módulo 5, enfocado en conceptos avanzados de UVM incluyendo secuencias virtuales, modelos de cobertura, configuración compleja, callbacks y modelos de registros.

## Estructura del Directorio

```
module5/
├── examples/              # Ejemplos de pyuvm para cada tema
│   ├── virtual_sequences/ # Ejemplos de secuencias virtuales
│   │   └── virtual_sequence_example.py
│   ├── coverage/          # Ejemplos de modelos de cobertura
│   │   └── coverage_example.py
│   ├── configuration/     # Ejemplos de objetos de configuración
│   │   └── configuration_example.py
│   ├── callbacks/         # Ejemplos de callbacks
│   │   └── callback_example.py
│   └── register_model/    # Ejemplos de modelos de registros
│       └── register_model_example.py
├── dut/                   # Módulos Verilog Design Under Test
│   └── advanced/          # Módulos avanzados para pruebas
│       └── multi_channel.v
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # Testbenches pyuvm
│       └── test_advanced_uvm.py
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

## Ejemplos Avanzados de UVM

### 1. Secuencias Virtuales (`examples/virtual_sequences/virtual_sequence_example.py`)

Demuestra el secuenciador virtual y la coordinación de secuencias virtuales:

**Conceptos Clave:**
- Secuenciador virtual que contiene referencias a múltiples secuenciadores
- Secuencia virtual que coordina secuencias en diferentes secuenciadores
- Ejecución paralela de secuencias usando `cocotb.start_soon()`
- Ejecución secuencial de secuencias
- Sincronización de secuencias

**Componentes de Secuencia Virtual:**

1. **VirtualSequencer**
   - Extiende `uvm_sequencer`
   - Contiene referencias a múltiples secuenciadores (`master_seqr`, `slave_seqr`)
   - Referencias establecidas en `connect_phase()` desde el entorno
   - Sin transacciones propias (coordina otros secuenciadores)

2. **VirtualSequence**
   - Extiende `uvm_sequence`
   - Coordina secuencias en múltiples secuenciadores
   - Ejecución paralela usando `cocotb.start_soon()`
   - Ejecución secuencial usando `await seq.start()`
   - Demuestra sincronización de secuencias

3. **ChannelSequence**
   - Secuencia regular para un solo canal
   - Genera transacciones para un canal específico
   - Número de canal y cantidad de ítems configurables

**Patrones de Secuencia Virtual:**

**Ejecución Paralela:**
```python
# Iniciar secuencias en paralelo
master_task = cocotb.start_soon(master_seq.start(self.master_seqr))
slave_task = cocotb.start_soon(slave_seq.start(self.slave_seqr))

# Esperar a que ambas completen
await master_task
await slave_task
```

**Ejecución Secuencial:**
```python
# Iniciar secuencias secuencialmente
await seq1.start(self.master_seqr)
await seq2.start(self.slave_seqr)
```

**Ejecutar el ejemplo:**

```bash
# Mediante el script del módulo
./scripts/module5.sh --virtual-sequences

# O directamente desde el directorio del ejemplo
cd module5/examples/virtual_sequences
make SIM=verilator TEST=virtual_sequence_example
```

**Salida Esperada:**
- Creación y conexión del secuenciador virtual
- Ejecución paralela de secuencias
- Ejecución secuencial de secuencias
- Coordinación multi-secuenciador

### 2. Cobertura (`examples/coverage/coverage_example.py`)

Demuestra la implementación de cobertura funcional:

**Conceptos Clave:**
- Clase de modelo de cobertura que extiende `uvm_subscriber`
- Muestreo de cobertura mediante el método `write()`
- Coverpoints y bins (implementación simplificada en Python)
- Cobertura cruzada entre múltiples campos
- Análisis y reporte de cobertura

**Clases de Cobertura:**

1. **CoverageModel**
   - Extiende `uvm_subscriber`
   - Recibe transacciones a través del puerto de análisis
   - Muestrea cobertura en el método `write()`
   - Rastrea estructuras de datos de cobertura
   - Reporta cobertura en `report_phase()`

2. **CoverageMonitor**
   - Genera transacciones de muestra
   - Transmite a través del puerto de análisis
   - Conectado al modelo de cobertura

**Tipos de Cobertura:**

1. **Cobertura de Datos**
   - Rastrea valores de datos únicos
   - Cobertura: número de valores únicos / total de valores posibles
   - Ejemplo: 5 valores únicos / 256 posibles = 2.0% de cobertura

2. **Cobertura de Rango de Direcciones**
   - Rastrea rangos de direcciones (bajo, medio, alto)
   - Cobertura: muestras en cada rango
   - Ejemplo: Bajo (0x0000-0x3FFF), Medio (0x4000-0x7FFF), Alto (0x8000-0xFFFF)

3. **Cobertura de Comandos**
   - Rastrea valores de comando únicos
   - Cobertura: número de comandos únicos / total posible
   - Ejemplo: 3 comandos únicos / 256 posibles = 1.2% de cobertura

4. **Cobertura Cruzada**
   - Rastrea combinaciones de datos y comando
   - Cobertura: número de combinaciones únicas
   - Ejemplo: pares (data, command)

**Muestreo de Cobertura:**
```python
def write(self, txn):
    """Sample coverage for transaction."""
    # Data coverage
    self.data_coverage[txn.data] = self.data_coverage.get(txn.data, 0) + 1
    
    # Address range coverage
    if txn.address < 0x4000:
        self.address_ranges['low'] += 1
    elif txn.address < 0x8000:
        self.address_ranges['mid'] += 1
    else:
        self.address_ranges['high'] += 1
    
    # Cross coverage
    key = (txn.data, txn.command)
    self.cross_coverage[key] = self.cross_coverage.get(key, 0) + 1
```

**Ejecutar el ejemplo:**

```bash
./scripts/module5.sh --coverage
# o
cd module5/examples/coverage
make SIM=verilator TEST=coverage_example
```

**Salida Esperada:**
- Demostración de muestreo de cobertura
- Reporte de estadísticas de cobertura
- Cálculos de porcentaje de cobertura
- Seguimiento de cobertura cruzada

### 3. Configuración (`examples/configuration/configuration_example.py`)

Demuestra el diseño de objetos de configuración complejos y jerarquía:

**Conceptos Clave:**
- Objetos de configuración que extienden `uvm_object`
- Estructura de configuración jerárquica
- Validación de configuración
- Composición de configuración
- Herencia de configuración

**Clases de Configuración:**

1. **AgentConfig**
   - Configuración para componentes del agente
   - Campos: `active`, `has_coverage`, `address_width`, `data_width`, `max_outstanding`
   - Método `validate()` para validación de configuración
   - Utilizado por agentes para configurar comportamiento

2. **EnvConfig**
   - Configuración a nivel de entorno
   - Contiene configuraciones de agente (`master_config`, `slave_config`)
   - Campos: `num_agents`, `enable_scoreboard`, `enable_coverage`
   - Demuestra composición de configuración

**Patrones de Configuración:**

**Validación de Configuración:**
```python
def validate(self):
    """Validate configuration values."""
    if self.address_width not in [16, 32, 64]:
        return False
    if self.data_width not in [8, 16, 32, 64]:
        return False
    if self.max_outstanding < 1:
        return False
    return True
```

**Configuración Jerárquica:**
```python
# Establecer configuración en diferentes niveles de jerarquía
ConfigDB().set(None, "", "env.config", env_config)
ConfigDB().set(None, "", "env.master_agent.config", master_config)
ConfigDB().set(None, "", "env.slave_agent.config", slave_config)
```

**Uso de Configuración:**
```python
# Obtener configuración en build_phase
config = None
success = ConfigDB().get(None, "", f"{self.get_full_name()}.config", config)
if success and config is not None:
    self.config = config
    if not self.config.validate():
        self.logger.error("Configuration validation failed")
```

**Ejecutar el ejemplo:**

```bash
./scripts/module5.sh --configuration
# o
cd module5/examples/configuration
make SIM=verilator TEST=configuration_example
```

**Beneficios de la Configuración:**
- Gestión centralizada de configuración
- Herencia jerárquica de configuración
- Validación y verificación de errores de configuración
- Personalización fácil de pruebas sin cambios de código

### 4. Callbacks (`examples/callbacks/callback_example.py`)

Demuestra patrones de implementación de callbacks:

**Conceptos Clave:**
- Diseño de clases de callback (nota: pyuvm puede tener soporte limitado de callbacks)
- Callbacks pre/post para drivers y monitores
- Registro de callbacks (demostración conceptual)
- Patrones de uso de callbacks

**Clases de Callback:**

1. **DriverCallback**
   - Callback para operaciones del driver
   - Métodos: `pre_drive()`, `post_drive()`
   - Puede modificar transacciones antes/después de manejarlas
   - Demuestra estructura de callback

2. **MonitorCallback**
   - Callback para operaciones del monitor
   - Métodos: `pre_sample()`, `post_sample()`
   - Puede modificar transacciones antes/después de muestrearlas
   - Demuestra estructura de callback

**Nota:** pyuvm puede no tener soporte completo de callbacks como en SystemVerilog UVM. Este ejemplo demuestra el patrón de callback conceptualmente.

**Patrones de Callback:**

**Callback Pre-Drive:**
```python
def pre_drive(self, driver, txn):
    """Called before driving transaction."""
    # Can modify transaction
    txn.data = modify_data(txn.data)
    return txn
```

**Callback Post-Drive:**
```python
def post_drive(self, driver, txn):
    """Called after driving transaction."""
    # Can perform actions after driving
    self.logger.info(f"Transaction driven: {txn}")
```

**Registro de Callback (Conceptual):**
```python
# In end_of_elaboration_phase
callback = DriverCallback.create("callback")
# In full UVM: driver.add_callback(callback)
```

**Ejecutar el ejemplo:**

```bash
./scripts/module5.sh --callbacks
# o
cd module5/examples/callbacks
make SIM=verilator TEST=callback_example
```

**Beneficios de los Callbacks:**
- Mejoras no intrusivas en las pruebas
- Implementaciones de callbacks reutilizables
- Personalización flexible de pruebas
- Separación de preocupaciones

### 5. Modelo de Registros (`examples/register_model/register_model_example.py`)

Demuestra la implementación de un modelo de registros:

**Conceptos Clave:**
- Diseño de clase de modelo de registros (ejemplo simplificado)
- Operaciones de registros por frontdoor (lectura/escritura)
- Operaciones de registros por backdoor (peek/poke)
- Operaciones de actualización de registros
- Integración con secuencias de registros

**Nota:** Este es un ejemplo simplificado. El soporte completo del modelo de registros UVM puede requerir características adicionales de pyuvm.

**Clases del Modelo de Registros:**

1. **RegisterModel**
   - Implementación simplificada de modelo de registros
   - Almacena valores de registros (dirección -> valor)
   - Proporciona operaciones frontdoor: `read()`, `write()`
   - Proporciona operaciones backdoor: `peek()`, `poke()`
   - Proporciona operación de actualización: `update()`

2. **RegisterSequence**
   - Secuencia para acceso a registros
   - Genera transacciones de lectura/escritura de registros
   - Se integra con el modelo de registros

3. **RegisterDriver**
   - Driver para operaciones de registros
   - Ejecuta operaciones de lectura/escritura de registros
   - Utiliza el modelo de registros para las operaciones

**Operaciones de Registros:**

**Operaciones Frontdoor:**
```python
# Escribir registro por frontdoor (a través de la interfaz DUT)
reg_model.write(0x0000, 0x01)

# Leer registro por frontdoor
value = reg_model.read(0x0000)
```

**Operaciones Backdoor:**
```python
# Poke a registro por backdoor (acceso directo)
reg_model.poke(0x0004, 0x80)

# Peek a registro por backdoor
value = reg_model.peek(0x0004)
```

**Operación de Actualización:**
```python
# Actualizar todos los registros (escribir valores deseados en hardware)
reg_model.update()
```

**Definiciones de Registros:**
```python
self.reg_defs = {
    0x0000: "CONTROL",
    0x0004: "STATUS",
    0x0008: "DATA",
    0x000C: "CONFIG",
}
```

**Ejecutar el ejemplo:**

```bash
./scripts/module5.sh --register-model
# o
cd module5/examples/register_model
make SIM=verilator TEST=register_model_example
```

**Beneficios del Modelo de Registros:**
- Interfaz abstracta de acceso a registros
- Operaciones frontdoor y backdoor
- Actualización y verificación de registros
- Integración con secuencias y drivers

## Design Under Test (DUT)

### Interfaz Multi-Canal (`dut/advanced/multi_channel.v`)

Una interfaz multi-canal para pruebas avanzadas de UVM.

**Interfaz del Módulo:**
```verilog
module multi_channel (
    input  wire       clk,            // Señal de reloj
    input  wire       rst_n,          // Reset activo en bajo
    input  wire       master_valid,   // Canal master válido
    output reg        master_ready,   // Canal master listo
    input  wire [7:0] master_data,    // Datos del canal master (8-bit)
    input  wire       slave_valid,    // Canal slave válido
    output reg        slave_ready,    // Canal slave listo
    input  wire [7:0] slave_data      // Datos del canal slave (8-bit)
);
```

**Funcionalidad:**
- Se resetea a todos ceros cuando `rst_n` está en bajo
- Canal master: afirma `master_ready` cuando `master_valid` está afirmado
- Canal slave: afirma `slave_ready` cuando `slave_valid` está afirmado
- Handshaking independiente para cada canal
- Protocolo multi-canal simple para pruebas de secuencias virtuales

**Características:**
- Operación síncrona con reset asíncrono
- Dos canales independientes (master y slave)
- Handshaking valid/ready por canal
- Adecuado para pruebas de secuencias virtuales y multi-agente

**Protocolo:**
- Canal master: Handshaking valid/ready
- Canal slave: Handshaking valid/ready
- Operación independiente de los canales

## Testbenches

### Pruebas pyuvm (`tests/pyuvm_tests/`)

#### Prueba Avanzada de UVM (`test_advanced_uvm.py`)

Testbench UVM completo que demuestra conceptos avanzados:

**Componentes UVM:**

1. **Transaction (`AdvancedTransaction`)**
   - Contiene campos `data` y `channel`
   - Utilizado para pruebas multi-canal

2. **Sequence (`AdvancedSequence`)**
   - Genera transacciones de prueba
   - Crea y envía transacciones

3. **Driver (`AdvancedDriver`)**
   - Recibe transacciones del secuenciador
   - Maneja las entradas del DUT (patrón mostrado)

4. **Monitor (`AdvancedMonitor`)**
   - Muestrea las salidas del DUT
   - Crea transacciones a partir de los datos muestreados
   - Transmite a través del puerto de análisis

5. **Coverage (`AdvancedCoverage`)**
   - Extiende `uvm_subscriber`
   - Recibe transacciones del monitor
   - Muestrea cobertura para valores de datos

6. **Agent (`AdvancedAgent`)**
   - Contiene driver, monitor y secuenciador
   - Conecta componentes

7. **Environment (`AdvancedEnv`)**
   - Contiene agente y cobertura
   - Conecta el monitor con la cobertura

8. **Test (`AdvancedUVMTest`)**
   - Clase de prueba de nivel superior
   - Crea el entorno y ejecuta la prueba
   - Inicia la secuencia y verifica la cobertura

**Flujo de Prueba:**
1. `build_phase()` - Crear todos los componentes
2. `connect_phase()` - Conectar componentes
3. `run_phase()` - Iniciar secuencia, generar transacciones
4. `check_phase()` - Verificar resultados
5. `report_phase()` - Generar reporte de prueba

**Ejecutar la prueba:**

```bash
# Mediante el script del módulo
./scripts/module5.sh --pyuvm-tests

# Directamente desde el directorio de pruebas
cd module5/tests/pyuvm_tests
make SIM=verilator TEST=test_advanced_uvm
```

**Resultados Esperados:**
- 1 caso de prueba exitoso
- Todos los componentes creados y conectados
- Ejecución de secuencia demostrada
- Muestreo de cobertura demostrado
- Conceptos avanzados de UVM integrados

## Ejecutar Ejemplos y Pruebas

### Usando el Script del Módulo

El script `module5.sh` proporciona una forma conveniente de ejecutar todos los ejemplos y pruebas:

```bash
# Ejecutar todo (todos los ejemplos + todas las pruebas)
./scripts/module5.sh

# Ejecutar solo ejemplos
./scripts/module5.sh --all-examples

# Ejecutar solo pruebas
./scripts/module5.sh --pyuvm-tests

# Ejecutar ejemplos específicos
./scripts/module5.sh --virtual-sequences
./scripts/module5.sh --coverage
./scripts/module5.sh --configuration
./scripts/module5.sh --callbacks
./scripts/module5.sh --register-model

# Combinar opciones
./scripts/module5.sh --virtual-sequences --coverage --pyuvm-tests
```

### Ejecutar Ejemplos Individuales

#### Ejecución Directa desde el Directorio del Ejemplo

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio del ejemplo
cd module5/examples/virtual_sequences

# Ejecutar ejemplo
make SIM=verilator TEST=virtual_sequence_example

# Limpiar artefactos de compilación
make clean
```

#### Ejecutar Todos los Ejemplos Secuencialmente

```bash
cd module5/examples

# Virtual sequences
cd virtual_sequences && make SIM=verilator TEST=virtual_sequence_example && cd ..

# Coverage
cd coverage && make SIM=verilator TEST=coverage_example && cd ..

# Configuration
cd configuration && make SIM=verilator TEST=configuration_example && cd ..

# Callbacks
cd callbacks && make SIM=verilator TEST=callback_example && cd ..

# Register model
cd register_model && make SIM=verilator TEST=register_model_example && cd ..
```

### Ejecutar Pruebas pyuvm

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio de pruebas
cd module5/tests/pyuvm_tests

# Ejecutar prueba
make SIM=verilator TEST=test_advanced_uvm

# Limpiar artefactos de compilación
make clean
```

## Resultados de las Pruebas

Cuando las pruebas se completen exitosamente, deberías ver una salida similar a:

### Salida de Ejemplo de Prueba

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** virtual_sequence_example.test_virtual_sequence  PASS         200.00           0.00     123456.78  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 200.00           0.00      12345.67  **
```

### Conteo Esperado de Pruebas

- **Ejemplo de Secuencias Virtuales**: 1 prueba
- **Ejemplo de Cobertura**: 1 prueba
- **Ejemplo de Configuración**: 1 prueba
- **Ejemplo de Callbacks**: 1 prueba
- **Ejemplo de Modelo de Registros**: 1 prueba
- **Prueba Avanzada de UVM**: 1 prueba
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

#### 3. Secuencia Virtual No Coordina

**Error:** La secuencia virtual no coordina múltiples secuenciadores

**Solución:**
- Verifica que las referencias del secuenciador virtual estén establecidas en `connect_phase()`
- Asegúrate de que las secuencias se inicien en los secuenciadores correctos
- Verifica que la secuencia virtual tenga referencias a los secuenciadores
- Comprueba que la ejecución paralela use `cocotb.start_soon()` correctamente

#### 4. La Cobertura No Muestrea

**Error:** El modelo de cobertura no recibe transacciones

**Solución:**
- Verifica que la cobertura extienda `uvm_subscriber` (proporciona `analysis_export`)
- Comprueba que el puerto de análisis del monitor esté conectado a la exportación de análisis de la cobertura
- Asegúrate de que el método `write()` esté implementado en el modelo de cobertura
- Verifica que la conexión se realice en el `connect_phase()` del entorno

#### 5. Configuración No Encontrada

**Error:** Configuración no encontrada en ConfigDB

**Solución:**
- Verifica que la configuración se establezca antes de que los componentes intenten obtenerla
- Comprueba que la ruta de jerarquía coincida exactamente
- Usa la ruta de jerarquía completa para la configuración específica del componente
- Asegúrate de que la configuración se establezca en el `build_phase()` del padre antes del `build_phase()` del hijo

#### 6. Callbacks No Funcionan

**Error:** Los callbacks no se ejecutan

**Solución:**
- Nota: pyuvm puede tener soporte limitado de callbacks en comparación con SystemVerilog UVM
- Este ejemplo demuestra patrones de callback conceptualmente
- Revisa la documentación de pyuvm para ver el soporte de callbacks
- Considera usar llamadas a métodos directas como alternativa a los callbacks

#### 7. Problemas con el Modelo de Registros

**Error:** Las operaciones de registros fallan

**Solución:**
- Verifica que el modelo de registros esté creado y sea accesible
- Comprueba que la dirección del registro esté en el diccionario `reg_defs`
- Asegúrate de que las operaciones de registros usen las direcciones correctas
- Nota: Este es un ejemplo simplificado; el modelo de registros UVM completo puede requerir características adicionales

### Consejos de Depuración

1. **Verificar Conexiones del Secuenciador Virtual:**
   ```python
   # Verify sequencer references are set
   self.logger.info(f"Master sequencer: {self.virtual_seqr.master_seqr}")
   self.logger.info(f"Slave sequencer: {self.virtual_seqr.slave_seqr}")
   ```

2. **Monitorear el Muestreo de Cobertura:**
   ```python
   # Add logging in coverage write method
   self.logger.info(f"Sampling coverage for: {txn}")
   ```

3. **Verificar Valores de Configuración:**
   ```python
   # Print configuration after getting it
   self.logger.info(f"Configuration: {self.config}")
   ```

4. **Verificar Ejecución de Secuencia:**
   ```python
   # Add logging in sequence body
   print(f"Starting sequence on sequencer: {self.sequencer}")
   ```

5. **Inspeccionar Estadísticas de Cobertura:**
   ```python
   # Check coverage in report_phase
   coverage_stats = self.coverage.get_coverage()
   self.logger.info(f"Coverage stats: {coverage_stats}")
   ```

6. **Validar Configuración:**
   ```python
   # Validate configuration before use
   if not self.config.validate():
       self.logger.error("Configuration validation failed")
   ```

## Temas Cubiertos

1. **Secuencias Virtuales** - Coordinación de múltiples secuenciadores, ejecución paralela/secuencial
2. **Modelos de Cobertura** - Cobertura funcional, coverpoints, cobertura cruzada
3. **Configuración Compleja** - Objetos de configuración, jerarquía, validación
4. **Callbacks** - Patrones de callback, callbacks pre/post (conceptual)
5. **Modelo de Registros** - Operaciones de registros, acceso frontdoor/backdoor
6. **Coordinación de Secuencias** - Coordinación multi-secuenciador, sincronización
7. **Análisis de Cobertura** - Recolección de cobertura, reporte, cierre
8. **Patrones de Configuración** - Estrategias de configuración, validación, herencia
9. **Depuración Avanzada** - Técnicas de depuración para UVM avanzado
10. **Integración de Testbench** - Integración de conceptos avanzados en testbenches

## Próximos Pasos

Después de completar el Módulo 5, continúa con:

- **Módulo 6**: Verificación de Protocolo - Testbenches multi-agente, verificadores de protocolo
- **Módulo 7**: Temas Avanzados - DMA, integración VIP, mejores prácticas
- **Módulo 8**: Utilidades Avanzadas - CLP, comparadores, pools, colas, grabadores

## Recursos Adicionales

- [Documentación de pyuvm](https://pyuvm.readthedocs.io/)
- [Guía de Usuario de UVM](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_1.2.pdf)
- [Documentación de cocotb](https://docs.cocotb.org/)
- [Documentación de Verilator](https://verilator.org/)

## Descripción de Archivos

### Ejemplos

| Archivo | Descripción | Pruebas |
|---------|-------------|---------|
| `virtual_sequence_example.py` | Secuenciador virtual y coordinación de secuencias | 1 función de prueba |
| `coverage_example.py` | Implementación de cobertura funcional | 1 función de prueba |
| `configuration_example.py` | Objetos de configuración complejos | 1 función de prueba |
| `callback_example.py` | Patrones de implementación de callbacks | 1 función de prueba |
| `register_model_example.py` | Implementación de modelo de registros | 1 función de prueba |

### Módulos DUT

| Archivo | Descripción | Puertos |
|---------|-------------|---------|
| `multi_channel.v` | Interfaz multi-canal | `clk`, `rst_n`, `master_valid`, `master_ready`, `master_data[7:0]`, `slave_valid`, `slave_ready`, `slave_data[7:0]` |

### Testbenches

| Archivo | Framework | Descripción | Pruebas |
|---------|-----------|-------------|---------|
| `test_advanced_uvm.py` | pyuvm | Testbench UVM avanzado | 1 prueba UVM |

---

Para preguntas o problemas, consulta el README principal del proyecto o revisa los registros de prueba para mensajes de error detallados.
