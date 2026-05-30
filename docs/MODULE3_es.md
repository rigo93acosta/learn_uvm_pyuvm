# Módulo 3: Fundamentos de UVM

**Objetivo**: Dominar la jerarquía de clases de UVM y las fases

## Visión general

Este módulo introduce la Metodología Universal de Verificación (UVM) y su implementación en pyuvm. Aprenderás los conceptos fundamentales de UVM, la jerarquía de clases, las fases y cómo estructurar bancos de pruebas UVM.

### Ejemplos y estructura de código

Este módulo incluye ejemplos y bancos de pruebas completos ubicados en el directorio `module3/`:

```
module3/
├── examples/              # ejemplos de pyuvm para cada tema
│   ├── class_hierarchy/   # ejemplos de jerarquía de clases UVM
│   ├── phases/            # ejemplos de fases UVM
│   ├── reporting/         # ejemplos de reporting UVM
│   ├── configdb/          # ejemplos de ConfigDB
│   ├── factory/           # ejemplos del patrón Factory
│   └── objections/        # ejemplos del mecanismo de objeciones
├── dut/                   # módulos Verilog Design Under Test
│   └── simple_blocks/     # bloques simples para pruebas UVM
├── tests/                 # bancos de pruebas
│   └── pyuvm_tests/       # bancos de pruebas pyuvm
└── README.md              # documentación del Módulo 3
```

### Inicio rápido

**Ejecutar todos los ejemplos usando el script orquestador:**
```bash
# Ejecutar todos los ejemplos
./scripts/module3.sh

# Ejecutar ejemplos específicos
./scripts/module3.sh --class-hierarchy
./scripts/module3.sh --phases
./scripts/module3.sh --reporting
./scripts/module3.sh --configdb
./scripts/module3.sh --factory
./scripts/module3.sh --objections
./scripts/module3.sh --pyuvm-tests
```

**Ejecutar ejemplos individualmente:**
```bash
# Activar entorno virtual (si corresponde)
source .venv/bin/activate

# Ejecutar pruebas pyuvm
cd module3/tests/pyuvm_tests
make SIM=verilator TEST=test_simple_uvm

# Los ejemplos son ejemplos estructurales de pyuvm
# Se pueden importar y usar en tus bancos de pruebas
```

## Temas cubiertos

### 1. Introducción a UVM

- **¿Qué es UVM?**
  - Metodología Universal de Verificación
  - Estándar industrial para verificación
  - Metodología vs librería
  - Historia y evolución

- **¿Por qué UVM?**
  - Reusabilidad
  - Estandarización
  - Escalabilidad
  - Mantenibilidad

- **UVM en Python (pyuvm)**
  - Implementación en Python de UVM 1.2
  - Ventajas frente a SystemVerilog UVM
  - Compatibilidad y características

### 2. Jerarquía de clases de UVM

- **Clases base**
  - `uvm_object` - Base para todos los objetos UVM
  - `uvm_component` - Base para todos los componentes UVM
  - Diferencias y casos de uso

- **Clases de componente**
  - `uvm_test` - Clase de test de nivel superior
  - `uvm_env` - Contenedor de entornos
  - `uvm_agent` - Agente (driver, monitor, sequencer)
  - `uvm_driver` - Genera transacciones hacia el DUT
  - `uvm_monitor` - Monitorea señales del DUT
  - `uvm_sequencer` - Maneja secuencias
  - `uvm_scoreboard` - Verifica resultados

- **Clases de objeto**
  - `uvm_sequence_item` - Objetos de transacción
  - `uvm_sequence` - Secuencia de transacciones
  - `uvm_config_object` - Objetos de configuración

- **Relaciones entre clases**
  - Jerarquía de herencia
  - Patrones de composición
  - Patrón Factory

### 3. Fases UVM

- **Visión general de fases**
  - Por qué existen las fases
  - Orden de ejecución de fases
  - Sincronización entre fases
  - Tipos de fases

- **Fases de construcción**
  - `build_phase()` - Construcción de componentes
  - `connect_phase()` - Conexiones entre componentes
  - `end_of_elaboration_phase()` - Configuración final

- **Fases de ejecución (run phases)**
  - `run_phase()` - Ejecución principal del test
  - `pre_reset_phase()` - Antes del reset
  - `reset_phase()` - Secuencia de reset
  - `post_reset_phase()` - Después del reset
  - `pre_configure_phase()` - Antes de la configuración
  - `configure_phase()` - Configuración
  - `post_configure_phase()` - Después de configurar
  - `pre_main_phase()` - Antes del test principal
  - `main_phase()` - Ejecución principal del test
  - `post_main_phase()` - Después del test principal
  - `pre_shutdown_phase()` - Antes del apagado
  - `shutdown_phase()` - Secuencia de apagado
  - `post_shutdown_phase()` - Después del apagado

- **Fases de limpieza**
  - `extract_phase()` - Extraer resultados
  - `check_phase()` - Comprobaciones finales
  - `report_phase()` - Generar reportes
  - `final_phase()` - Limpieza final

- **Implementación de fases**
  - Fases síncronas (build, connect)
  - Fases asíncronas (run phases)
  - Métodos de fase
  - Orden de fases

### 4. Sistema de reporting de UVM

- **Visión general del reporting**
  - Sistema de mensajes de UVM
  - Niveles de severidad
  - Niveles de verbosidad
  - Formato de mensajes

- **Niveles de severidad**
  - `UVM_FATAL` - Errores fatales
  - `UVM_ERROR` - Errores
  - `UVM_WARNING` - Advertencias
  - `UVM_INFO` - Información
  - `UVM_DEBUG` - Mensajes de depuración

- **Niveles de verbosidad**
  - `UVM_NONE` - Sin mensajes
  - `UVM_LOW` - Baja verbosidad
  - `UVM_MEDIUM` - Verbosidad media
  - `UVM_HIGH` - Alta verbosidad
  - `UVM_FULL` - Verbosidad completa
  - `UVM_DEBUG` - Verbosidad de depuración

- **Uso del reporting**
  - `self.logger.info()`
  - `self.logger.warning()`
  - `self.logger.error()`
  - `self.logger.fatal()`
  - Formato de mensajes
  - Control de verbosidad

### 5. Base de datos de configuración (ConfigDB)

- **Visión general de ConfigDB**
  - ¿Qué es ConfigDB?
  - ¿Por qué usar ConfigDB?
  - Jerarquía de configuración

- **Establecer configuración**
  - `ConfigDB().set()`
  - Rutas de configuración
  - Objetos de configuración
  - Configuración escalar

- **Obtener configuración**
  - `ConfigDB().get()`
  - Búsqueda en la configuración
  - Valores por defecto
  - Comprobación de configuración

- **Patrones de configuración**
  - Configuración de agentes
  - Configuración de entornos
  - Configuración de tests
  - Configuración jerárquica

### 6. Patrón Factory

- **Visión general del Factory**
  - ¿Qué es el factory?
  - ¿Por qué usar el factory?
  - Beneficios del factory

- **Uso del Factory**
  - Registro de tipos
  - Creación de objetos
  - Mecanismo de override
  - Patrones del factory

### 7. Primera clase de test UVM

- **Estructura del test**
  - Definición de la clase de test
  - Heredar desde `uvm_test`
  - Métodos requeridos
  - Organización del test

- **Creación del entorno**
  - Crear el entorno
  - Jerarquía del entorno
  - Instanciación de componentes

- **Ejecución del test**
  - Implementación de `run_phase()`
  - Mecanismo de objeciones
  - Flujo del test
  - Finalización

### 8. Estructura del entorno

- **Fundamentos del entorno**
  - ¿Qué es un entorno?
  - Propósito del entorno
  - Estructura del entorno

- **Componentes del entorno**
  - Instanciación de agentes
  - Instanciación de scoreboards
  - Instanciación de coverage
  - Otros componentes

- **Conexiones del entorno**
  - Conexiones entre componentes
  - Conexiones de puertos de análisis
  - Conexiones TLM

### 9. Mecanismo de objeciones

- **Visión general de objeciones**
  - ¿Qué son las objeciones?
  - ¿Por qué las objeciones?
  - Ciclo de vida de las objeciones

- **Uso de objeciones**
  - `raise_objection()`
  - `drop_objection()`
  - Sincronización temporal de objeciones
  - Objeciones múltiples

- **Patrones de objeciones**
  - Objeciones en tests
  - Objeciones en secuencias
  - Objeciones en componentes
  - Buenas prácticas

### 10. Ejecución de tests UVM

- **Flujo del test**
  - Inicio del test
  - Ejecución de fases
  - Finalización del test
  - Limpieza

- **Ejecución de tests**
  - `uvm_root().run_test()`
  - Selección de tests
  - Parámetros del test
  - Ejecución del test

- **Organización de tests**
  - Múltiples tests
  - Herencia de tests
  - Bibliotecas de tests
  - Selección de tests

## Resultados de aprendizaje

Al final de este módulo, deberías ser capaz de:

- Entender la metodología UVM
- Explicar la jerarquía de clases de UVM
- Comprender y usar las fases UVM
- Usar el reporting de UVM eficazmente
- Usar ConfigDB para configuración
- Entender el patrón Factory
- Crear clases de test UVM
- Estructurar entornos UVM
- Usar el mecanismo de objeciones
- Ejecutar tests UVM

## Casos de prueba

### Caso de prueba 3.1: Test UVM simple
**Objetivo**: Crear la primera clase de test UVM

**Temas**:
- Definición de la clase de test
- Fases básicas
- Mecanismo de objeciones

#### Ejemplo 3.1: Jerarquía de clases (`module3/examples/class_hierarchy/class_hierarchy_example.py`)

**Lo que demuestra:**
- **Jerarquía `uvm_object`**: `uvm_sequence_item` para transacciones
- **Jerarquía `uvm_component`**: `uvm_driver`, `uvm_monitor`, `uvm_agent`, `uvm_env`, `uvm_test`
- **Composición de componentes**: Construcción de la jerarquía (Test → Env → Agent → Driver/Monitor)
- **Implementación de fases**: `build_phase()`, `connect_phase()`, `run_phase()`
- **Patrón Factory**: Uso de `create()` para instanciar componentes
- **Relaciones entre componentes**: Relaciones padre-hijo en UVM

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module3.sh --class-hierarchy

# O directamente (comprobación de sintaxis)
cd module3/examples/class_hierarchy
python3 -c "import pyuvm; exec(open('class_hierarchy_example.py').read())"
```

**Salida esperada:**
```
============================================================
Building ClassHierarchyTest
============================================================
[BUILD] Building MyEnv
[BUILD] Building MyAgent
[BUILD] Building MyDriver
[BUILD] Building MyMonitor
[CONNECT] Connecting MyAgent
[CONNECT] Connecting MyDriver
Running ClassHierarchyTest
Created transaction: MyTransaction: data=0xAB, addr=0x1000
============================================================
ClassHierarchyTest completed
============================================================
```

**Conceptos clave:**
- **`uvm_object`**: Base para todos los objetos UVM (transacciones, configs)
- **`uvm_component`**: Base para todos los componentes UVM (test, env, agent, driver, monitor)
- **`uvm_test`**: Clase de test de nivel superior
- **`uvm_env`**: Contenedor de entorno para agentes y otros componentes
- **`uvm_agent`**: Contiene driver, monitor, sequencer
- **`create()`**: Método del factory para creación de componentes
- **Jerarquía de componentes**: Test → Env → Agent → Driver/Monitor

### Caso de prueba 3.2: Entorno UVM
**Objetivo**: Crear un entorno UVM

**Temas**:
- Estructura del entorno
- Instanciación de componentes
- Implementación de fases

#### Ejemplo 3.2: Fases UVM (`module3/examples/phases/phases_example.py`)

**Lo que demuestra:**
- **Fases de construcción**: `build_phase()`, `connect_phase()`, `end_of_elaboration_phase()`
- **Fases de ejecución**: Las 12 run phases (pre_reset, reset, post_reset, etc.)
- **Fases de limpieza**: `extract_phase()`, `check_phase()`, `report_phase()`, `final_phase()`
- **Orden de ejecución de fases**: Fases síncronas se ejecutan top-down, las asíncronas concurrentes
- **Sincronización de fases**: Cómo coordinan las fases entre componentes
- **Implementación de fases**: Implementación de todas las fases en un componente

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module3.sh --phases

# O directamente
cd module3/examples/phases
python3 -c "import pyuvm; exec(open('phases_example.py').read())"
```

**Salida esperada:**
```
============================================================
PHASES TEST - Build Phase
============================================================
[BUILD] Building PhasesEnv
[BUILD] Building PhasesComponent
[CONNECT] Connecting PhasesEnv
[END_OF_ELAB] PhasesEnv elaboration complete
[END_OF_ELAB] PhasesComponent: Elaboration complete
PHASES TEST - Run Phase (all run phases execute here)
[PRE_RESET] PhasesComponent: Pre-reset phase
[RESET] PhasesComponent: Reset phase
[POST_RESET] PhasesComponent: Post-reset phase
...
[FINAL] PhasesComponent: Final cleanup
============================================================
PHASES TEST - Report Phase
============================================================
```

**Conceptos clave:**
- **Fases de construcción**: Síncronas, ejecución top-down
- **Fases de ejecución**: Asíncronas, ejecución concurrente
- **Fases de limpieza**: Síncronas, ejecución bottom-up
- **Orden de fases**: Build → Connect → End_of_Elab → Run Phases → Extract → Check → Report → Final
- **Fases síncronas**: Se ejecutan en orden, un componente a la vez
- **Fases asíncronas**: Todos los componentes ejecutan fases concurrentemente

### Caso de prueba 3.3: Reporting UVM
**Objetivo**: Usar el sistema de reporting de UVM

**Temas**:
- Niveles de severidad
- Control de verbosidad
- Formato de mensajes

#### Ejemplo 3.3: Reporting UVM (`module3/examples/reporting/reporting_example.py`)

**Lo que demuestra:**
- **Niveles de severidad**: `info()`, `warning()`, `error()`, `fatal()`
- **Formato de mensajes**: Uso de f-strings y especificadores de formato
- **Contexto del componente**: Obtener nombre del componente, tipo, nombre completo
- **Control de verbosidad**: Entender niveles de verbosidad (LOW, MEDIUM, HIGH, FULL, DEBUG)
- **Reporting jerárquico**: Los mensajes incluyen la jerarquía de componentes
- **Integración con logging**: El reporting de UVM usa el logging de Python

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module3.sh --reporting

# O directamente
cd module3/examples/reporting
python3 -c "import pyuvm; exec(open('reporting_example.py').read())"
```

**Salida esperada:**
```
============================================================
UVM Reporting Example
============================================================
Demonstrating UVM severity levels:
This is an INFO message
WARNING: This is a WARNING message
ERROR: This is an ERROR message
FATAL: This is a FATAL message (would stop simulation)
============================================================
Demonstrating message formatting:
Formatted message: data=0xAB, addr=0x1000
============================================================
Component context:
  Component name: ReportingTest
  Component type: ReportingTest
  Full name: uvm_test_top
```

**Conceptos clave:**
- **`self.logger.info()`**: Mensajes informativos
- **`self.logger.warning()`**: Mensajes de advertencia
- **`self.logger.error()`**: Mensajes de error
- **`self.logger.fatal()`**: Errores fatales (detienen la simulación)
- **`get_name()`**: Obtener nombre de instancia del componente
- **`get_type_name()`**: Obtener nombre de la clase del componente
- **`get_full_name()`**: Obtener nombre jerárquico completo
- **Verbosidad**: Controla qué mensajes se muestran

### Caso de prueba 3.4: Uso de ConfigDB
**Objetivo**: Usar ConfigDB

**Temas**:
- Establecer configuración
- Obtener configuración
- Jerarquía de configuración

#### Ejemplo 3.4: ConfigDB (`module3/examples/configdb/configdb_example.py`)

**Lo que demuestra:**
- **Establecer configuración**: `ConfigDB().set()` para objetos y escalares
- **Obtener configuración**: `ConfigDB().get()` con búsqueda
- **Objetos de configuración**: Crear clases de configuración personalizadas
- **Configuración jerárquica**: Establecer/obtener en distintos niveles de jerarquía
- **Búsqueda en ConfigDB**: Cómo busca la configuración en la jerarquía
- **Valores por defecto**: Proveer valores por defecto si no se encuentra la config

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module3.sh --configdb

# O directamente
cd module3/examples/configdb
python3 -c "import pyuvm; exec(open('configdb_example.py').read())"
```

**Salida esperada:**
```
============================================================
ConfigDB Example
============================================================
Building ConfigurableEnv
Set agent_config in ConfigDB
Set scalar configs in ConfigDB
[agent] Building agent
  Got config: active=True, has_coverage=True
  Got address_width: 16
Running ConfigDBTest
============================================================
Hierarchical Configuration Example:
Set configurations at different hierarchy levels
  Global config: global_value
  Test config: test_value
  Env config: env_value
============================================================
ConfigDB test completed
============================================================
```

**Conceptos clave:**
- **`ConfigDB().set(context, path, name, value)`**: Establecer configuración
- **`ConfigDB().get(context, path, name, value)`**: Obtener configuración
- **Objetos de configuración**: Clases personalizadas que heredan de `uvm_object`
- **Jerarquía**: ConfigDB busca desde específico a general (component → parent → global)
- **Coincidencia de rutas**: Usar cadena vacía para el componente actual, rutas específicas para niveles
- **Seguridad de tipos**: ConfigDB mantiene información de tipo

#### Ejemplo 3.5: Patrón Factory (`module3/examples/factory/factory_example.py`)

**Lo que demuestra:**
- **Registro del Factory**: Registro automático de clases UVM
- **Creación mediante Factory**: Usar el factory para crear objetos y componentes
- **Overrides de tipo**: `uvm_factory().set_type_override()` para sustituciones
- **Clases base y extendidas**: Crear versiones base y extendidas
- **Beneficios del Factory**: Polimorfismo sin comprobaciones de tipo explícitas
- **Mecanismo de override**: Cómo el factory resuelve tipos con overrides

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module3.sh --factory

# O directamente
cd module3/examples/factory
python3 -c "import pyuvm; exec(open('factory_example.py').read())"
```

**Conceptos clave:**
- **Registro del Factory**: Todas las clases UVM se registran automáticamente
- **`create()`**: Método del factory para creación de componentes
- **`uvm_factory().set_type_override()`**: Sobrescribir un tipo base por uno extendido
- **Resolución de tipos**: El factory resuelve tipos en tiempo de creación
- **Polimorfismo**: Usar el tipo base y obtener instancia del tipo extendido

#### Ejemplo 3.6: Mecanismo de objeciones (`module3/examples/objections/objections_example.py`)

**Lo que demuestra:**
- **Levantar objeciones**: `raise_objection()` para mantener la simulación activa
- **Bajar objeciones**: `drop_objection()` para permitir completar la fase
- **Objeciones múltiples**: Los componentes pueden levantar múltiples objeciones
- **Ciclo de vida de objeciones**: Cómo controlan la ejecución del test
- **Objeciones en componentes**: Cada componente gestiona sus propias objeciones
- **Control del test**: El test usa objeciones para controlar cuándo termina la simulación

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module3.sh --objections

# O directamente
cd module3/examples/objections
python3 -c "import pyuvm; exec(open('objections_example.py').read())"
```

**Salida esperada:**
```
============================================================
Objection Mechanism Example
============================================================
Building ObjectionEnv
[Test] Raised objection - simulation will run
[comp1] Raised objection
[comp2] Raised objection
[comp3] Raised 2 objections
[comp1] Work completed
[comp1] Dropped objection
[comp2] Work completed
[comp2] Dropped objection
[comp3] Dropped 1 objection, 1 remaining
[comp3] Dropped all objections
[Test] Dropping objection - simulation will end
============================================================
Objection test completed
============================================================
```

**Conceptos clave:**
- **`raise_objection()`**: Incrementa el contador de objeciones, mantiene la fase activa
- **`drop_objection()`**: Decrementa el contador de objeciones
- **Finalización de fase**: La fase termina cuando todas las objeciones se han bajado
- **Objeciones múltiples**: Se pueden levantar varias veces; hay que bajarlas tantas veces
- **Objeciones en tests**: El test típicamente levanta una objeción en `run_phase()`
- **Objeciones en componentes**: Componentes levantan/bajan según su trabajo

#### Test: Test UVM simple (`module3/tests/pyuvm_tests/test_simple_uvm.py`)

**Lo que demuestra:**
- Estructura completa del banco de pruebas UVM
- Jerarquía Test → Env → Agent → Driver/Monitor/Sequencer
- Uso de secuencias y sequence items
- Integración con scoreboard
- Conexiones de analysis ports
- Implementación completa de fases

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module3.sh --pyuvm-tests

# O manualmente
cd module3/tests/pyuvm_tests
make SIM=verilator TEST=test_simple_uvm
```

**Estructura del test:**
- `AdderTransaction`: Sequence item con datos de prueba
- `AdderSequence`: Genera vectores de prueba
- `AdderDriver`: Envía transacciones al DUT
- `AdderMonitor`: Monitorea salidas del DUT
- `AdderScoreboard`: Verifica resultados
- `AdderAgent`: Contiene driver, monitor, sequencer
- `AdderEnv`: Contiene agent y scoreboard
- `AdderTest`: Clase de test de nivel superior

### Módulos Design Under Test (DUT)

#### Sumador (`module3/dut/simple_blocks/adder.v`)
- **Propósito**: Sumador de 8 bits con salida de acarreo
- **Usado en**: Test UVM simple
- **Características**: Operación sincronizada por reloj, reset, operandos de 8 bits

## Ejercicios

1. **Creación de clase de test**
   - Crear clase de test
   - Implementar fases
   - Usar objeciones
   - **Ubicación**: Crear nuevo test en `module3/tests/pyuvm_tests/`
   - **Pista**: Comienza con `AdderTest` como plantilla

2. **Estructura del entorno**
   - Diseñar el entorno
   - Instanciar componentes
   - Conectar componentes
   - **Ubicación**: Extender `module3/examples/class_hierarchy/class_hierarchy_example.py`
   - **Pista**: Añade un scoreboard y conecta los analysis ports

3. **Reporting**
   - Añadir reporting
   - Controlar la verbosidad
   - Formatear mensajes
   - **Ubicación**: Extender `module3/examples/reporting/reporting_example.py`
   - **Pista**: Añade reporting en todas las fases

4. **Configuración**
   - Crear objetos de configuración
   - Establecer configuración
   - Obtener configuración
   - **Ubicación**: Extender `module3/examples/configdb/configdb_example.py`
   - **Pista**: Crea configuración para múltiples agentes

5. **Comprensión de fases**
   - Implementar todas las fases
   - Entender el orden de ejecución
   - Sincronizar fases
   - **Ubicación**: Extender `module3/examples/phases/phases_example.py`
   - **Pista**: Añade múltiples componentes y observa el orden de fases

## Evaluación

- [ ] Entiende la metodología UVM
- [ ] Puede explicar la jerarquía de clases
- [ ] Entiende todas las fases UVM
- [ ] Puede usar el reporting de UVM
- [ ] Puede usar ConfigDB
- [ ] Entiende el patrón Factory
- [ ] Puede crear clases de test
- [ ] Puede estructurar entornos
- [ ] Puede usar el mecanismo de objeciones
- [ ] Puede ejecutar tests

## Siguientes pasos

Después de completar este módulo, continúa con [Module 4: UVM Components](MODULE4.md) para aprender a construir agentes UVM completos.

## Recursos adicionales

- **Documentación de pyuvm**: https://pyuvm.readthedocs.io/
- **Guía de usuario UVM 1.2**: Accellera Systems Initiative
- **The UVM Primer**: Ray Salemi
- **Ejemplos pyuvm**: https://github.com/pyuvm/pyuvm/tree/main/examples

## Solución de problemas

### Problemas comunes

**Problema: error "pyuvm not found"**
```bash
# Solución: Instalar pyuvm
./scripts/install_pyuvm.sh --pip --venv .venv
# O
./scripts/module0.sh
```

**Problema: error "cocotb not found" (para ejecutar tests)**
```bash
# Solución: Instalar cocotb
./scripts/install_cocotb.sh --pip --venv .venv
# O
./scripts/module0.sh
```

**Problema: errores de importación en ejemplos**
```bash
# Solución: Asegurarse de que pyuvm esté instalado y el entorno virtual activado
source .venv/bin/activate
python3 -c "import pyuvm; print(pyuvm.__version__)"
```

**Problema: confusión en el orden de ejecución de fases**
```bash
# Solución: Revisar phases_example.py para ver el orden de ejecución
# Fases de construcción: top-down, síncronas
# Fases de ejecución: concurrentes, asíncronas
# Fases de limpieza: bottom-up, síncronas
```

**Problema: objeciones que no funcionan**
```bash
# Solución: Asegurarse de llamar a raise_objection() en run_phase()
# La simulación termina cuando todas las objeciones se han bajado
# Comprobar el contador de objeciones con los métodos de uvm_objection
```

### Obtener ayuda

- Revisar los comentarios del código de ejemplo para explicaciones detalladas
- Revisar `module3/README.md` para la estructura del directorio
- Ejecutar ejemplos individualmente para entender cada concepto
- Estudiar el orden de ejecución de fases en `phases_example.py`
- Revisar la documentación de pyuvm para detalles de la API

## Resumen de ejemplos y tests

**Ejemplos (ejemplos estructurales de pyuvm en `module3/examples/`):**
1. **Ejemplo 3.1: Jerarquía de clases** (`class_hierarchy/`) - Clases base y componentes UVM
2. **Ejemplo 3.2: Fases UVM** (`phases/`) - Todas las fases UVM y su orden de ejecución
3. **Ejemplo 3.3: Reporting UVM** (`reporting/`) - Niveles de severidad y verbosidad
4. **Ejemplo 3.4: ConfigDB** (`configdb/`) - Uso de la base de datos de configuración
5. **Ejemplo 3.5: Patrón Factory** (`factory/`) - Creación y overrides con el factory
6. **Ejemplo 3.6: Objeciones** (`objections/`) - Mecanismo de objeciones

**Bancos de pruebas (tests ejecutables en `module3/tests/pyuvm_tests/`):**
1. **Test UVM simple** (`test_simple_uvm.py`) - Banco de pruebas completo con todos los componentes

**Módulos DUT (en `module3/dut/`):**
1. **Sumador** (`simple_blocks/adder.v`) - Sumador de 8 bits para pruebas UVM

**Cobertura:**
- ✅ Jerarquía de clases UVM (uvm_object, uvm_component)
- ✅ Todas las fases UVM (build, run, cleanup)
- ✅ Sistema de reporting UVM
- ✅ Uso de ConfigDB
- ✅ Patrón Factory
- ✅ Mecanismo de objeciones
- ✅ Estructura completa del banco de pruebas
