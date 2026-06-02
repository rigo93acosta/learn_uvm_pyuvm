# Módulo 5: Conceptos Avanzados de UVM

**Objetivo**: Dominar secuencias, cobertura, configuración y secuencias virtuales

## Resumen

Este módulo cubre conceptos avanzados de UVM incluyendo secuencias virtuales, modelos de cobertura, configuración compleja, callbacks y uso avanzado de modelos de registros. Estos conceptos son esenciales para construir entornos de verificación sofisticados.

### Ejemplos y Estructura de Código

Este módulo incluye ejemplos completos y testbenches ubicados en el directorio `module5/`:

```
module5/
├── examples/              # Ejemplos de pyuvm para cada tema
│   ├── virtual_sequences/ # Ejemplos de secuencias virtuales
│   ├── coverage/         # Ejemplos de modelos de cobertura
│   ├── configuration/    # Ejemplos de objetos de configuración
│   ├── callbacks/        # Ejemplos de callbacks
│   └── register_model/   # Ejemplos de modelos de registros
├── dut/                   # Módulos Verilog Design Under Test
│   └── advanced/          # Módulos avanzados para pruebas
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # Testbenches pyuvm
└── README.md             # Documentación del Módulo 5
```

### Inicio Rápido

**Ejecutar todos los ejemplos usando el script orquestador:**
```bash
# Ejecutar todos los ejemplos
./scripts/module5.sh

# Ejecutar ejemplos específicos
./scripts/module5.sh --virtual-sequences
./scripts/module5.sh --coverage
./scripts/module5.sh --configuration
./scripts/module5.sh --callbacks
./scripts/module5.sh --register-model
./scripts/module5.sh --pyuvm-tests
```

**Ejecutar ejemplos individualmente:**
```bash
# Activar entorno virtual (si usas uno)
source .venv/bin/activate

# Ejecutar pruebas pyuvm
cd module5/tests/pyuvm_tests
make SIM=verilator TEST=test_advanced_uvm

# Los ejemplos son ejemplos estructurales de pyuvm
# Se pueden importar y usar en tus testbenches
```

## Temas Cubiertos

### 1. Secuencias Avanzadas

- **Secuencias Virtuales**
  - ¿Qué son las secuencias virtuales?
  - Propósito de las secuencias virtuales
  - Coordinación de múltiples secuenciadores
  - Implementación de secuencias virtuales

- **Librerías de Secuencias**
  - Clases de secuencia base
  - Secuencias derivadas
  - Patrones de reutilización de secuencias
  - Organización de secuencias

- **Arbitraje de Secuencias**
  - Arbitraje de secuenciador
  - Mecanismos de prioridad
  - Lock y grab
  - Coordinación de secuencias

- **Secuencias en Capas**
  - Secuencias de alto nivel
  - Secuencias de bajo nivel
  - Composición de secuencias
  - Capas de protocolo

### 2. Modelos de Cobertura UVM

- **Resumen de Cobertura**
  - ¿Qué es cobertura?
  - Tipos de cobertura
  - Objetivos de cobertura
  - Métricas de cobertura

- **Cobertura Funcional**
  - Modelos de cobertura
  - Grupos de cobertura
  - Coverpoints
  - Bins de cobertura

- **Implementación de Cobertura**
  - Estructura de clase de cobertura
  - Muestreo de cobertura
  - Análisis de cobertura
  - Reporte de cobertura

- **Patrones de Cobertura**
  - Cobertura de transacciones
  - Cobertura de protocolo
  - Cobertura de estados
  - Cobertura cruzada

### 3. Objetos de Configuración Complejos

- **Objetos de Configuración**
  - Diseño de clase de configuración
  - Campos de configuración
  - Métodos de configuración
  - Validación de configuración

- **Jerarquía de Configuración**
  - Configuración jerárquica
  - Herencia de configuración
  - Sobrescritura de configuración
  - Patrones de configuración

- **Base de Datos de Recursos**
  - Uso de la base de datos de recursos
  - Tipos de recursos
  - Búsqueda de recursos
  - Gestión de recursos

- **Callbacks de Configuración**
  - Callbacks de configuración
  - Callbacks pre/post
  - Registro de callbacks
  - Ejecución de callbacks

### 4. Callbacks UVM

- **Resumen de Callbacks**
  - ¿Qué son los callbacks?
  - Propósito de los callbacks
  - Tipos de callbacks
  - Beneficios de los callbacks

- **Implementación de Callbacks**
  - Definición de clase de callback
  - Registro de callbacks
  - Ejecución de callbacks
  - Patrones de callbacks

- **Callbacks Pre/Post**
  - Pre-callbacks
  - Post-callbacks
  - Orden de callbacks
  - Control de callbacks

- **Casos de Uso de Callbacks**
  - Callbacks de driver
  - Callbacks de monitor
  - Callbacks de scoreboard
  - Callbacks de prueba

### 5. Modelo de Registros UVM (Avanzado)

- **Resumen del Modelo de Registros**
  - Propósito del modelo de registros
  - Estructura del modelo de registros
  - Beneficios del modelo de registros
  - Componentes del modelo de registros

- **Componentes del Modelo de Registros**
  - `uvm_reg_block` - Bloques de registros
  - `uvm_reg` - Registros
  - `uvm_reg_field` - Campos de registro
  - `uvm_reg_map` - Mapas de direcciones

- **Operaciones de Registros**
  - Lectura de registros
  - Escritura de registros
  - Peek/poke de registros
  - Actualización de registros

- **Secuencias de Registros**
  - Secuencias de acceso a registros
  - Secuencias de prueba de registros
  - Integración del modelo de registros
  - Predictor de registros

- **Acceso Backdoor**
  - Lectura/escritura backdoor
  - Backdoor vs frontdoor
  - Casos de uso de backdoor
  - Implementación de backdoor

### 6. Secuencias Virtuales y Secuenciadores Virtuales

- **Secuenciador Virtual**
  - Propósito del secuenciador virtual
  - Estructura del secuenciador virtual
  - Referencias a múltiples secuenciadores
  - Implementación del secuenciador virtual

- **Coordinación de Secuencias Virtuales**
  - Coordinando múltiples secuenciadores
  - Ejecución paralela de secuencias
  - Sincronización de secuencias
  - Patrones de coordinación de secuencias

- **Patrones de Secuencias Virtuales**
  - Coordinación maestro-esclavo
  - Coordinación multi-canal
  - Coordinación de protocolo
  - Coordinación de prueba

### 7. Análisis y Cierre de Cobertura

- **Análisis de Cobertura**
  - Recolección de cobertura
  - Reporte de cobertura
  - Brechas de cobertura
  - Herramientas de análisis de cobertura

- **Cierre de Cobertura**
  - Objetivos de cobertura
  - Estrategias de cobertura
  - Mejora de cobertura
  - Métricas de cobertura

- **Patrones de Cobertura**
  - Cobertura funcional
  - Cobertura de código
  - Cobertura de aserciones
  - Correlación de cobertura

### 8. Patrones Avanzados de Configuración

- **Estrategias de Configuración**
  - Configuración descendente
  - Configuración ascendente
  - Configuración mixta
  - Mejores prácticas de configuración

- **Configuración Dinámica**
  - Configuración en tiempo de ejecución
  - Actualizaciones de configuración
  - Validación de configuración
  - Depuración de configuración

### 9. Optimización de Rendimiento

- **Rendimiento del Testbench**
  - Cuellos de botella de rendimiento
  - Estrategias de optimización
  - Optimización de memoria
  - Velocidad de simulación

- **Optimización de Secuencias**
  - Diseño eficiente de secuencias
  - Reutilización de secuencias
  - Caché de secuencias
  - Rendimiento de secuencias

### 10. Técnicas Avanzadas de Depuración

- **Depuración UVM**
  - Herramientas de depuración UVM
  - Depuración de fases
  - Depuración de componentes
  - Depuración de transacciones

- **Depuración de Cobertura**
  - Brechas de cobertura
  - Análisis de cobertura
  - Mejora de cobertura
  - Herramientas de cobertura

## Resultados de Aprendizaje

Al final de este módulo, deberías ser capaz de:

- Crear y usar secuencias virtuales
- Implementar modelos de cobertura
- Diseñar objetos de configuración complejos
- Usar callbacks UVM efectivamente
- Usar características avanzadas del modelo de registros
- Coordinar múltiples secuenciadores
- Analizar y cerrar cobertura
- Optimizar el rendimiento del testbench
- Depurar testbenches avanzados
- Aplicar patrones avanzados

## Casos de Prueba

### Caso de Prueba 5.1: Secuencias Virtuales
**Objetivo**: Crear secuencia virtual coordinando múltiples secuenciadores

**Temas**:
- Secuenciador virtual
- Secuencia virtual
- Coordinación de múltiples secuenciadores

#### Ejemplo 5.1: Secuencias Virtuales (`module5/examples/virtual_sequences/virtual_sequence_example.py`)

**Qué demuestra:**
- **Secuenciador Virtual**: Contenedor para múltiples referencias de secuenciadores
- **Secuencia Virtual**: Secuencia que coordina múltiples secuenciadores
- **Ejecución Paralela**: Iniciando secuencias en diferentes secuenciadores concurrentemente
- **Ejecución Secuencial**: Ejecutando secuencias en orden
- **Coordinación Multi-Canal**: Coordinando canales maestro y esclavo
- **Sincronización de Secuencias**: Sincronizando múltiples ejecuciones de secuencias

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module5.sh --virtual-sequences

# O directamente (verificación de sintaxis)
cd module5/examples/virtual_sequences
python3 -c "import pyuvm; exec(open('virtual_sequence_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Virtual Sequence Example Test
============================================================
Building VirtualEnv
Building MasterAgent
Building SlaveAgent
[virtual_seqr] Building virtual sequencer
[virtual_seqr] Connecting virtual sequencer
[VirtualSequence] Starting virtual sequence
[VirtualSequence] Starting parallel sequences
[master_seq] Starting channel 0 sequence
[slave_seq] Starting channel 1 sequence
...
[VirtualSequence] Parallel sequences completed
```

**Conceptos Clave:**
- **Secuenciador Virtual**: Contiene referencias a múltiples secuenciadores
- **Secuencia Virtual**: Coordina secuencias a través de múltiples secuenciadores
- **Ejecución Paralela**: Usa `cocotb.start_soon()` para secuencias concurrentes
- **Ejecución Secuencial**: Usa `await` para ejecución ordenada de secuencias
- **Coordinación Multi-Agente**: Coordina secuencias a través de múltiples agentes
- **Capas de Secuencia**: Las secuencias virtuales pueden llamar a otras secuencias

### Caso de Prueba 5.2: Modelo de Cobertura
**Objetivo**: Implementar cobertura funcional

**Temas**:
- Clase de cobertura
- Coverpoints y bins
- Muestreo de cobertura

#### Ejemplo 5.2: Modelos de Cobertura (`module5/examples/coverage/coverage_example.py`)

**Qué demuestra:**
- **Clase de Cobertura**: Heredando de `uvm_subscriber` para cobertura
- **Muestreo de Cobertura**: Muestreando transacciones a través del puerto de análisis
- **Coverpoints**: Seguimiento de datos, rangos de direcciones, comandos
- **Bins de Cobertura**: Organizando cobertura en bins (rangos de direcciones bajo, medio, alto)
- **Cobertura Cruzada**: Seguimiento de combinaciones de ítems de cobertura
- **Reporte de Cobertura**: Generando reportes de cobertura en report_phase

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module5.sh --coverage

# O directamente
cd module5/examples/coverage
python3 -c "import pyuvm; exec(open('coverage_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Coverage Example Test
============================================================
[coverage] Building coverage model
[monitor] Starting coverage monitor
[coverage] Sampling coverage for: data=0x00, addr=0x1000, cmd=0x01
...
============================================================
[coverage] Coverage Report
============================================================
Data Coverage: 5 unique values
Address Coverage:
  Low (0x0000-0x3FFF):  2 samples
  Mid (0x4000-0x7FFF):  1 samples
  High (0x8000-0xFFFF): 2 samples
Command Coverage: 3 unique commands
Cross Coverage: 5 unique combinations
Data Coverage: 2.0%
Command Coverage: 1.2%
```

**Conceptos Clave:**
- **`uvm_subscriber`**: Clase base para modelos de cobertura
- **Conexión de Puerto de Análisis**: Conectar monitor a cobertura a través del puerto de análisis
- **Muestreo de Cobertura**: Muestrear transacciones en el método `write()`
- **Bins de Cobertura**: Organizar cobertura en bins significativos
- **Cobertura Cruzada**: Seguimiento de combinaciones de ítems de cobertura
- **Reporte de Cobertura**: Reportar estadísticas de cobertura en report_phase

### Caso de Prueba 5.3: Objetos de Configuración
**Objetivo**: Crear configuración compleja

**Temas**:
- Clase de configuración
- Jerarquía de configuración
- Uso de configuración

#### Ejemplo 5.3: Objetos de Configuración (`module5/examples/configuration/configuration_example.py`)

**Qué demuestra:**
- **Diseño de Clase de Configuración**: Creando objetos de configuración que heredan de `uvm_object`
- **Campos de Configuración**: Definiendo parámetros de configuración
- **Validación de Configuración**: Validando valores de configuración
- **Configuración Jerárquica**: Configuración a nivel de entorno y agente
- **Composición de Configuración**: Componiendo configuraciones complejas a partir de otras más simples
- **Uso de ConfigDB**: Estableciendo y obteniendo configuración a través de ConfigDB

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module5.sh --configuration

# O directamente
cd module5/examples/configuration
python3 -c "import pyuvm; exec(open('configuration_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Configuration Example Test
============================================================
Building ConfigurableEnv
Set environment configuration: num_agents=2, master_config=...
[master_agent] Building configurable agent
[master_agent] Got config: active=True, has_coverage=True, ...
[master_agent] Agent is ACTIVE
[slave_agent] Building configurable agent
[slave_agent] Got config: active=False, has_coverage=False, ...
[slave_agent] Agent is PASSIVE
Configuration Hierarchy:
  Master agent config: active=True, has_coverage=True, ...
  Slave agent config: active=False, has_coverage=False, ...
```

**Conceptos Clave:**
- **`uvm_object`**: Clase base para objetos de configuración
- **Diseño de Configuración**: Diseñar clases de configuración con validación
- **Configuración Jerárquica**: Establecer configuración en diferentes niveles de jerarquía
- **Validación de Configuración**: Validar configuración en el método `validate()`
- **ConfigDB**: Usar ConfigDB para almacenamiento y recuperación de configuración
- **Composición de Configuración**: Construir configuraciones complejas a partir de otras más simples

### Caso de Prueba 5.4: Callbacks
**Objetivo**: Implementar mecanismo de callbacks

**Temas**:
- Clase de callback
- Registro de callbacks
- Ejecución de callbacks

#### Ejemplo 5.4: Callbacks UVM (`module5/examples/callbacks/callback_example.py`)

**Qué demuestra:**
- **Clase de Callback**: Creando clases de callback que heredan de `uvm_callback`
- **Métodos de Callback**: Implementando métodos de callback pre/post
- **Registro de Callbacks**: Registrando callbacks con componentes
- **Ejecución de Callbacks**: Ejecutando callbacks en puntos apropiados
- **Callbacks de Driver**: Callbacks pre-drive y post-drive
- **Callbacks de Monitor**: Callbacks pre-sample y post-sample

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module5.sh --callbacks

# O directamente
cd module5/examples/callbacks
python3 -c "import pyuvm; exec(open('callback_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Callback Example Test
============================================================
Building CallbackEnv
Building CallbackAgent
[driver] Building driver with callbacks
[monitor] Building monitor with callbacks
Registering callbacks
Registered driver callback
Registered monitor callback
[driver] Starting driver
[driver] Executing pre-drive callbacks
[driver_callback] Pre-drive callback: data=0x00
[driver] Driving: data=0x00
[driver] Executing post-drive callbacks
[driver_callback] Post-drive callback: data=0x00
```

**Conceptos Clave:**
- **`uvm_callback`**: Clase base para todos los callbacks
- **Métodos de Callback**: Implementar métodos de callback (pre/post)
- **Registro de Callbacks**: Registrar callbacks en `end_of_elaboration_phase()`
- **Ejecución de Callbacks**: Ejecutar callbacks usando `get_callbacks()`
- **Callbacks Pre/Post**: Pre-callbacks antes de la acción, post-callbacks después
- **Casos de Uso de Callbacks**: Modificar transacciones, agregar logging, agregar verificaciones

### Caso de Prueba 5.5: Modelo de Registros Avanzado
**Objetivo**: Usar características avanzadas de registros

**Temas**:
- Modelo de registros
- Secuencias de registros
- Acceso backdoor

#### Ejemplo 5.5: Modelo de Registros (`module5/examples/register_model/register_model_example.py`)

**Qué demuestra:**
- **Estructura del Modelo de Registros**: Creando clases de modelo de registros
- **Operaciones de Registros**: Operaciones de lectura, escritura, peek, poke
- **Secuencias de Registros**: Secuencias para acceso a registros
- **Acceso Frontdoor**: Acceso normal a registros a través del bus
- **Acceso Backdoor**: Acceso directo a registros (peek/poke)
- **Actualización de Registros**: Actualizando registros del modelo al hardware

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module5.sh --register-model

# O directamente
cd module5/examples/register_model
python3 -c "import pyuvm; exec(open('register_model_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Register Model Example Test
============================================================
Building RegisterEnv
Building RegisterAgent
[reg_model] Writing register 0x0000 (CONTROL): 0x01
[reg_model] Reading register 0x0000 (CONTROL): 0x01
Read back value: 0x01
[reg_model] Poking register 0x0004: 0x80
[reg_model] Peeking register 0x0004: 0x80
Peeked value: 0x80
[seq] Starting register sequence
[seq] Register operation: WRITE: addr=0x0000, data=0x01
```

**Conceptos Clave:**
- **Modelo de Registros**: Modelo software de registros hardware
- **Acceso Frontdoor**: Acceso normal a registros basado en bus
- **Acceso Backdoor**: Acceso directo a registros (peek/poke)
- **Operaciones de Registros**: read(), write(), peek(), poke(), update()
- **Secuencias de Registros**: Secuencias para pruebas de registros
- **Nota**: El soporte completo del modelo de registros UVM puede variar en pyuvm

#### Prueba: Prueba UVM Avanzada (`module5/tests/pyuvm_tests/test_advanced_uvm.py`)

**Qué demuestra:**
- Testbench completo con características UVM avanzadas
- Integración de cobertura
- Uso avanzado de componentes
- Flujo de prueba completo

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module5.sh --pyuvm-tests

# O manualmente
cd module5/tests/pyuvm_tests
make SIM=verilator TEST=test_advanced_uvm
```

**Estructura de la Prueba:**
- `AdvancedTransaction`: Transacción para prueba avanzada
- `AdvancedSequence`: Genera vectores de prueba
- `AdvancedDriver`: Maneja transacciones
- `AdvancedMonitor`: Monitorea DUT
- `AdvancedCoverage`: Modelo de cobertura
- `AdvancedAgent`: Contiene driver, monitor, secuenciador
- `AdvancedEnv`: Contiene agente y cobertura
- `AdvancedUVMTest`: Clase de prueba de nivel superior

### Módulos Design Under Test (DUT)

#### Interfaz Multi-Canal (`module5/dut/advanced/multi_channel.v`)
- **Propósito**: Interfaz multi-canal con canales maestro y esclavo
- **Usado en**: Prueba UVM avanzada
- **Características**: Operación sincronizada, reset, handshaking valid/ready, canales separados

## Ejercicios

1. **Secuencias Virtuales**
   - Crear secuenciador virtual
   - Crear secuencia virtual
   - Coordinar múltiples agentes
   - **Ubicación**: Extiende `module5/examples/virtual_sequences/virtual_sequence_example.py`
   - **Pista**: Agrega más canales y coordínalos en la secuencia virtual

2. **Implementación de Cobertura**
   - Diseñar modelo de cobertura
   - Implementar cobertura
   - Analizar cobertura
   - **Ubicación**: Extiende `module5/examples/coverage/coverage_example.py`
   - **Pista**: Agrega más coverpoints y bins de cobertura cruzada

3. **Diseño de Configuración**
   - Crear clases de configuración
   - Implementar jerarquía
   - Usar configuración
   - **Ubicación**: Extiende `module5/examples/configuration/configuration_example.py`
   - **Pista**: Crea configuración para múltiples agentes con diferentes configuraciones

4. **Implementación de Callbacks**
   - Crear callbacks
   - Registrar callbacks
   - Usar callbacks
   - **Ubicación**: Extiende `module5/examples/callbacks/callback_example.py`
   - **Pista**: Agrega callbacks para scoreboard y agrega modificación de transacciones

5. **Modelo de Registros**
   - Crear modelo de registros
   - Implementar secuencias
   - Usar acceso backdoor
   - **Ubicación**: Extiende `module5/examples/register_model/register_model_example.py`
   - **Pista**: Agrega más registros e implementa acceso a campos de registro

## Evaluación

- [ ] Puedo crear secuencias virtuales
- [ ] Puedo implementar modelos de cobertura
- [ ] Puedo diseñar objetos de configuración
- [ ] Puedo usar callbacks efectivamente
- [ ] Puedo usar el modelo de registros avanzado
- [ ] Puedo coordinar múltiples secuenciadores
- [ ] Puedo analizar cobertura
- [ ] Puedo optimizar rendimiento
- [ ] Puedo depurar testbenches avanzados
- [ ] Entiendo los patrones avanzados

## Próximos Pasos

Después de completar este módulo, continúa con [Módulo 6: Testbenches Complejos](MODULE6.md) para aprender a construir testbenches complejos multi-agente.

## Recursos Adicionales

- **Documentación de pyuvm**: https://pyuvm.readthedocs.io/
- **Guía de Usuario de UVM 1.2**: Accellera Systems Initiative
- **UVM Avanzado**: Ray Salemi
- **Ejemplos de pyuvm**: https://github.com/pyuvm/pyuvm/tree/main/examples

## Solución de Problemas

### Problemas Comunes

**Problema: Error "pyuvm not found"**
```bash
# Solución: Instalar pyuvm
./scripts/install_pyuvm.sh --pip --venv .venv
# O
./scripts/module0.sh
```

**Problema: La secuencia virtual no coordina secuenciadores**
```bash
# Solución: Asegurar que el secuenciador virtual tenga referencias a los secuenciadores reales
# Establecer en connect_phase: virtual_seqr.master_seqr = master_agent.seqr
# Pasar a secuencia virtual: virtual_seq.master_seqr = env.virtual_seqr.master_seqr
```

**Problema: La cobertura no muestrea**
```bash
# Solución: Verificar la conexión del puerto de análisis
# Asegurar: monitor.ap.connect(coverage.ap)
# Verificar que cobertura implemente el método write()
```

**Problema: Los callbacks no se ejecutan**
```bash
# Solución: Registrar callbacks en end_of_elaboration_phase()
# Asegurar: component.add_callback(callback)
# Verificar que los métodos de callback estén implementados correctamente
```

**Problema: Configuración no encontrada**
```bash
# Solución: Establecer configuración antes del build_phase del componente
# Usar ConfigDB().set() en el build_phase de la prueba
# Verificar que la ruta de configuración coincida con la jerarquía del componente
```

### Obteniendo Ayuda

- Revisa los comentarios del código de ejemplo para explicaciones detalladas
- Consulta el `module5/README.md` para la estructura del directorio
- Ejecuta ejemplos individualmente para entender cada concepto avanzado
- Estudia la coordinación de secuencias virtuales en `virtual_sequence_example.py`
- Revisa la implementación de cobertura en `coverage_example.py`
- Consulta la documentación de pyuvm para características avanzadas

### Resumen de Ejemplos y Pruebas

**Ejemplos (ejemplos estructurales de pyuvm en `module5/examples/`):**
1. **Ejemplo 5.1: Secuencias Virtuales** (`virtual_sequences/`) - Secuenciador virtual y coordinación de secuencias
2. **Ejemplo 5.2: Modelos de Cobertura** (`coverage/`) - Implementación de cobertura funcional
3. **Ejemplo 5.3: Objetos de Configuración** (`configuration/`) - Diseño de configuración compleja
4. **Ejemplo 5.4: Callbacks UVM** (`callbacks/`) - Implementación y uso de callbacks
5. **Ejemplo 5.5: Modelo de Registros** (`register_model/`) - Operaciones de modelo de registros

**Testbenches (pruebas ejecutables en `module5/tests/pyuvm_tests/`):**
1. **Prueba UVM Avanzada** (`test_advanced_uvm.py`) - Testbench completo con características avanzadas

**Módulos DUT (en `module5/dut/`):**
1. **Interfaz Multi-Canal** (`advanced/multi_channel.v`) - Interfaz multi-canal para pruebas avanzadas

**Cobertura:**
- ✅ Secuencias virtuales y secuenciadores virtuales
- ✅ Modelos de cobertura funcional
- ✅ Objetos de configuración complejos
- ✅ Mecanismo de callbacks UVM
- ✅ Operaciones de modelo de registros
- ✅ Integración avanzada de testbench
