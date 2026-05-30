# Módulo 3: Conceptos Básicos de UVM

Este directorio contiene todos los ejemplos, ejercicios y casos de prueba para el Módulo 3, centrados en los fundamentos de UVM (Universal Verification Methodology) incluyendo jerarquía de clases, fases, reporting, base de datos de configuración, patrón factory y el mecanismo de objeciones.

## Estructura del directorio

```
module3/
├── examples/              # ejemplos de pyuvm por tema
│   ├── class_hierarchy/   # ejemplos de jerarquía de clases UVM
│   │   └── class_hierarchy_example.py
│   ├── phases/           # ejemplos de fases UVM
│   │   └── phases_example.py
│   ├── reporting/        # ejemplos del sistema de reporting
│   │   └── reporting_example.py
│   ├── configdb/         # ejemplos de ConfigDB
│   │   └── configdb_example.py
│   ├── factory/          # ejemplos del patrón factory
│   │   └── factory_example.py
│   └── objections/       # ejemplos del mecanismo de objeciones
│       └── objections_example.py
├── dut/                   # módulos Verilog del DUT
│   └── simple_blocks/     # bloques simples para pruebas UVM
│       └── adder.v        # sumador de 8 bits
├── tests/                 # testbenches
│   └── pyuvm_tests/      # testbenches pyuvm
│       └── test_simple_uvm.py
└── exercises/            # soluciones de ejercicios (si las hay)
```

## Requisitos previos

Antes de ejecutar los experimentos, asegúrate de tener:

- **Python 3.8+** - Requerido para cocotb y pyuvm
- **Verilator 5.036+** - Requerido para la simulación (se recomienda 5.044)
- **cocotb 2.0+** - Instalado en el entorno virtual
- **pyuvm 4.0+** - Instalado en el entorno virtual
- **Make** - Para compilar y ejecutar pruebas

Para verificar el entorno:

```bash
python3 --version        # Debe ser 3.8+
verilator --version      # Debe ser 5.036+
python3 -c "import cocotb; print(cocotb.__version__)"
python3 -c "import pyuvm; print(pyuvm.__version__)"
```

## Ejemplos de UVM

### 1. Jerarquía de clases (`examples/class_hierarchy/class_hierarchy_example.py`)

Demuestra la jerarquía de clases UVM y la estructura de componentes:

**Conceptos clave:**
- `uvm_object` - Clase base para todos los objetos UVM (transacciones, secuencias)
- `uvm_component` - Clase base para todos los componentes UVM (drivers, monitors, agentes)
- Jerarquía de componentes: Test → Environment → Agent → Driver/Monitor
- Creación de componentes usando el factory (`create()`)
- Implementación de fases en componentes

**Clases UVM demostradas:**

1. **Transacción (`MyTransaction`)**
   - Extiende `uvm_sequence_item`
   - Contiene datos de prueba (data, address)
   - Demuestra la jerarquía de `uvm_object`

2. **Driver (`MyDriver`)**
   - Extiende `uvm_driver`
   - Implementa `build_phase()`, `connect_phase()`, `run_phase()`
   - Usa `uvm_seq_item_pull_port` para la comunicación de transacciones

3. **Monitor (`MyMonitor`)**
   - Extiende `uvm_monitor`
   - Implementa `build_phase()`, `run_phase()`
   - Usa `uvm_analysis_port` para reenviar datos

4. **Agent (`MyAgent`)**
   - Extiende `uvm_agent`
   - Contiene driver, monitor y sequencer
   - Demuestra composición de componentes

5. **Environment (`MyEnv`)**
   - Extiende `uvm_env`
   - Contiene instancias de agentes
   - Entorno de verificación de alto nivel

6. **Test (`ClassHierarchyTest`)**
   - Extiende `uvm_test`
   - Clase de test de alto nivel
   - Orquesta la ejecución del test

**Ejecución del ejemplo:**

```bash
# Vía el script del módulo
./scripts/module3.sh --class-hierarchy

# O directamente desde el directorio del ejemplo
cd module3/examples/class_hierarchy
make SIM=verilator TEST=class_hierarchy_example
```

**Salida esperada:**
- Creación y conexión de la jerarquía de componentes
- Ejecución de fases en orden jerárquico
- Creación y manipulación de transacciones

### 2. Fases (`examples/phases/phases_example.py`)

Demuestra la ejecución e implementación de las fases UVM:

**Conceptos clave:**
- Orden de ejecución de fases UVM
- Fases de tiempo de compilación (síncronas)
- Fases de tiempo de ejecución (asíncronas)
- Fases de limpieza

**Fases UVM demostradas:**

**Fases de compilación (de arriba hacia abajo):**
1. `build_phase()` - Construcción de componentes
2. `connect_phase()` - Conexión de componentes
3. `end_of_elaboration_phase()` - Configuración final

**Fases de tiempo de ejecución (de abajo hacia arriba):**
4. `pre_reset_phase()` - Antes del reset
5. `reset_phase()` - Secuencia de reset
6. `post_reset_phase()` - Después del reset
7. `pre_configure_phase()` - Antes de configuración
8. `configure_phase()` - Configuración
9. `post_configure_phase()` - Después de configuración
10. `pre_main_phase()` - Antes del test principal
11. `main_phase()` - Ejecución principal del test
12. `post_main_phase()` - Después del test principal
13. `pre_shutdown_phase()` - Antes del apagado
14. `shutdown_phase()` - Secuencia de apagado
15. `post_shutdown_phase()` - Después del apagado

**Fases de limpieza (de abajo hacia arriba):**
16. `extract_phase()` - Extracción de resultados
17. `check_phase()` - Comprobaciones finales
18. `report_phase()` - Generación de reportes
19. `final_phase()` - Limpieza final

**Ejecución del ejemplo:**

```bash
./scripts/module3.sh --phases
# o
cd module3/examples/phases
make SIM=verilator TEST=phases_example
```

**Orden de ejecución de fases:**
- Las fases de compilación se ejecutan de arriba hacia abajo (padre antes que hijos)
- Las fases de tiempo de ejecución se ejecutan de abajo hacia arriba (hijos antes que padre)
- Las fases de limpieza se ejecutan de abajo hacia arriba (hijos antes que padre)

### 3. Reporting (`examples/reporting/reporting_example.py`)

Demuestra el sistema de reporting de UVM con niveles de severidad y verbosidad:

**Conceptos clave:**
- Niveles de severidad: INFO, WARNING, ERROR, FATAL
- Niveles de verbosidad: UVM_LOW, UVM_MEDIUM, UVM_HIGH, UVM_FULL, UVM_DEBUG
- Formato de mensajes y contexto
- Reporting jerárquico con nombres de componente

**Casos de prueba:**

1. `test_reporting` - Demostración básica de reporting
   - Ejemplos de niveles de severidad
   - Formato de mensajes con datos
   - Información de contexto del componente
   - Explicación de niveles de verbosidad

2. `test_hierarchical_reporting` - Reporting jerárquico
   - Reporting desde diferentes componentes
   - Inclusión del nombre del componente en los mensajes

**Métodos de reporting:**
- `self.logger.info()` - Mensajes informativos
- `self.logger.warning()` - Mensajes de advertencia
- `self.logger.error()` - Mensajes de error
- `self.logger.fatal()` - Errores fatales (detienen la simulación)

**Ejecución del ejemplo:**

```bash
./scripts/module3.sh --reporting
# o
cd module3/examples/reporting
make SIM=verilator TEST=reporting_example
```

**Salida esperada:**
- Mensajes con distintos niveles de severidad
- Mensajes formateados con valores de datos
- Contexto del componente en los mensajes
- Reporting jerárquico de componentes

### 4. ConfigDB (`examples/configdb/configdb_example.py`)

Demuestra la base de datos de configuración UVM para pasar configuraciones:

**Conceptos clave:**
- Establecer valores de configuración en ConfigDB
- Recuperar valores desde ConfigDB
- Búsqueda jerárquica de configuración
- Objetos de configuración vs valores escalares
- Configuración específica por componente

**Casos de prueba:**

1. `test_configdb` - Uso básico de ConfigDB
   - Establecer objetos de configuración
   - Establecer valores escalares de configuración
   - Recuperar configuración desde ConfigDB
   - Rutas jerárquicas de configuración

2. `test_configdb_hierarchy` - Configuración jerárquica
   - Configuración en diferentes niveles de jerarquía
   - Configuración global vs específica por componente
   - Prioridad en la búsqueda de configuración

**Patrones de configuración:**

**Establecer configuración:**
```python
ConfigDB().set(None, "", "config_name", value)  # Global
ConfigDB().set(self, "env.agent", "config_name", value)  # Ruta específica
```

**Obtener configuración:**
```python
config = None
success = ConfigDB().get(None, "", "config_name", config)
if success and config is not None:
    # Usar config
```

**Ejemplo de objeto de configuración:**
```python
class AgentConfig(uvm_object):
    def __init__(self, name="AgentConfig"):
        super().__init__(name)
        self.active = True
        self.has_coverage = False
        self.address_width = 32
```

**Ejecución del ejemplo:**

```bash
./scripts/module3.sh --configdb
# o
cd module3/examples/configdb
make SIM=verilator TEST=configdb_example
```

**Jerarquía de configuración:**
- La configuración se busca comenzando desde la ruta del componente
- Si no se encuentra, se hace fallback a configuración más global
- Permite configurar pruebas sin cambiar el código

### 5. Factory (`examples/factory/factory_example.py`)

Demuestra el patrón factory de UVM para creación de objetos y overrides:

**Conceptos clave:**
- Registro de clases en el factory
- Creación de objetos mediante el factory
- Overrides de tipo para sustituir clases
- Overrides por instancia para casos específicos
- Factory de componentes vs factory de objetos

**Casos de prueba:**

1. `test_factory` - Uso básico del factory
   - Registro en el factory
   - Creación de objetos mediante factory
   - Creación de transacciones y componentes

2. `test_factory_override` - Overrides en el factory
   - Override de tipo: `BaseDriver` → `ExtendedDriver`
   - El override afecta todas las instancias del tipo base
   - Permite personalizar tests sin modificar el código base

**Patrones del factory:**

**Creación de objetos:**
```python
# Crear componente usando el factory
driver = MyDriver.create("driver", self)

# Crear objeto manualmente
txn = BaseTransaction("txn_name")
```

**Override de tipo:**
```python
# Establecer override en build_phase
uvm_factory().set_type_override(BaseDriver, ExtendedDriver)
```

**Ejecución del ejemplo:**

```bash
./scripts/module3.sh --factory
# o
cd module3/examples/factory
make SIM=verilator TEST=factory_example
```

**Beneficios del factory:**
- Creación centralizada de objetos
- Sustitución fácil de implementaciones
- Personalización de tests sin modificar código base
- Soporta jerarquías de herencia

### 6. Objeciones (`examples/objections/objections_example.py`)

Demuestra el mecanismo de objeciones de UVM para controlar la ejecución del test:

**Conceptos clave:**
- Levantar objeciones para mantener la simulación en ejecución
- Soltar objeciones para permitir la finalización de la fase
- Múltiples objeciones por componente
- Seguimiento de objeciones en la jerarquía
- La simulación termina cuando todas las objeciones son soltadas

**Casos de prueba:**

1. `test_objection` - Mecanismo básico de objeciones
   - Levantar objeciones en test y componentes
   - Soltar objeciones cuando el trabajo termina
   - Control de simulación mediante objeciones

2. `test_objection_timing` - Temporización de objeciones
   - Múltiples componentes con duraciones diferentes de objeción
   - Coordinación del soltar de objeciones
   - Asegurar que todos completan antes de que termine el test

**Métodos de objeción:**
- `self.raise_objection()` - Levantar una objeción (mantiene la simulación)
- `self.drop_objection()` - Soltar una objeción (puede permitir finalizar la fase)

**Comportamiento de objeciones:**
- Cada componente puede levantar múltiples objeciones
- La fase completa solo cuando todas las objeciones han sido soltadas
- Las objeciones se rastrean por fase
- La simulación termina cuando las objeciones del `run_phase` son todas soltadas

**Ejecución del ejemplo:**

```bash
./scripts/module3.sh --objections
# o
cd module3/examples/objections
make SIM=verilator TEST=objections_example
```

**Buenas prácticas con objeciones:**
- Siempre levantar una objeción al inicio de `run_phase()` si se hace trabajo
- Soltar la objeción cuando el trabajo finalice
- Coordinar objeciones entre componentes
- Usar objeciones solo en fases de tiempo de ejecución (fases asíncronas)

## Diseño bajo prueba (DUT)

### Sumador (`dut/simple_blocks/adder.v`)

Un sumador de 8 bits con salida de acarreo para pruebas UVM.

**Interfaz del módulo:**
```verilog
module adder (
    input  wire       clk,     // Señal de reloj
    input  wire       rst_n,   // Reset activo bajo
    input  wire [7:0] a,       // Operando A
    input  wire [7:0] b,       // Operando B
    output reg  [7:0] sum,     // Salida suma (8-bit)
    output reg        carry    // Salida de acarreo
);
```

**Funcionalidad:**
- Resetea a ceros cuando `rst_n` está en bajo
- Calcula `{carry, sum} = a + b` en flanco positivo de reloj
- Maneja suma de 8 bits con detección de overflow
- El bit `carry` indica overflow (suma > 255)

**Características:**
- Operación síncrona con reset asíncrono
- Aritmética sin signo de 8 bits
- Detección de overflow mediante la señal de acarreo
- Diseño simple para demostración en testbench UVM

**Tabla de verdad (ejemplos):**
| a   | b   | sum | carry |
|-----|-----|-----|-------|
| 0x00 | 0x00 | 0x00 | 0 |
| 0x01 | 0x01 | 0x02 | 0 |
| 0xFF | 0x01 | 0x00 | 1 |
| 0x80 | 0x80 | 0x00 | 1 |

## Testbenches

### Tests pyuvm (`tests/pyuvm_tests/`)

#### Test UVM simple (`test_simple_uvm.py`)

Testbench UVM completo que demuestra todos los conceptos principales:

**Componentes UVM:**

1. **Transacción (`AdderTransaction`)**
   - Extiende `uvm_sequence_item`
   - Contiene operandos (a, b) y resultados esperados
   - Usada para estímulo y comprobación

2. **Secuencia (`AdderSequence`)**
   - Extiende `uvm_sequence`
   - Genera vectores de prueba para el sumador
   - Crea y envía transacciones al sequencer

3. **Driver (`AdderDriver`)**
   - Extiende `uvm_driver`
   - Recibe transacciones desde el sequencer
   - Conduce las entradas del DUT (patrón mostrado, no conectado en el ejemplo)

4. **Monitor (`AdderMonitor`)**
   - Extiende `uvm_monitor`
   - Observa las salidas del DUT
   - Reenvía transacciones vía analysis port

5. **Scoreboard (`AdderScoreboard`)**
   - Extiende `uvm_subscriber`
   - Recibe transacciones del monitor
   - Compara resultado esperado vs real

6. **Agent (`AdderAgent`)**
   - Extiende `uvm_agent`
   - Contiene driver, monitor y sequencer
   - Conecta componentes en `connect_phase()`

7. **Environment (`AdderEnv`)**
   - Extiende `uvm_env`
   - Contiene agent y scoreboard
   - Conecta monitor con scoreboard

8. **Test (`AdderTest`)**
   - Extiende `uvm_test`
   - Clase de test de alto nivel
   - Crea el entorno, inicia la secuencia y verifica resultados

**Flujo del test:**
1. `build_phase()` - Crear entorno y componentes
2. `connect_phase()` - Conectar componentes (driver-sequencer, monitor-scoreboard)
3. `run_phase()` - Iniciar la secuencia, generar transacciones
4. `check_phase()` - Verificar resultados en el scoreboard
5. `report_phase()` - Generar el reporte del test

**Ejecución del test:**

```bash
# Vía el script del módulo
./scripts/module3.sh --pyuvm-tests

# Directamente desde el directorio de tests
cd module3/tests/pyuvm_tests
make SIM=verilator TEST=test_simple_uvm

# Limpiar artefactos
make clean
```

**Resultados esperados:**
- 1 caso de prueba pasando
- Todas las fases UVM ejecutadas correctamente
- Generación y procesamiento de transacciones demostrado
- Verificación completada por el scoreboard

## Ejecución de ejemplos y pruebas

### Usando el script del módulo

El script `module3.sh` ofrece una forma conveniente de ejecutar todos los ejemplos y pruebas:

```bash
# Ejecuta todo (todos los ejemplos + todas las pruebas)
./scripts/module3.sh

# Ejecuta solo ejemplos
./scripts/module3.sh --all-examples

# Ejecuta solo pruebas
./scripts/module3.sh --pyuvm-tests

# Ejecuta ejemplos específicos
./scripts/module3.sh --class-hierarchy
./scripts/module3.sh --phases
./scripts/module3.sh --reporting
./scripts/module3.sh --configdb
./scripts/module3.sh --factory
./scripts/module3.sh --objections

# Combinar opciones
./scripts/module3.sh --phases --factory --pyuvm-tests
```

### Ejecutar ejemplos individuales

#### Ejecución directa desde el directorio del ejemplo

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio del ejemplo
cd module3/examples/phases

# Ejecutar ejemplo
make SIM=verilator TEST=phases_example

# Limpiar artefactos
make clean
```

#### Ejecutar todos los ejemplos secuencialmente

```bash
cd module3/examples

# Class hierarchy
cd class_hierarchy && make SIM=verilator TEST=class_hierarchy_example && cd ..

# Phases
cd phases && make SIM=verilator TEST=phases_example && cd ..

# Reporting
cd reporting && make SIM=verilator TEST=reporting_example && cd ..

# ConfigDB
cd configdb && make SIM=verilator TEST=configdb_example && cd ..

# Factory
cd factory && make SIM=verilator TEST=factory_example && cd ..

# Objections
cd objections && make SIM=verilator TEST=objections_example && cd ..
```

### Ejecutar tests pyuvm

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio de tests
cd module3/tests/pyuvm_tests

# Ejecutar test
make SIM=verilator TEST=test_simple_uvm

# Limpiar artefactos
make clean
```

## Resultados de pruebas

Cuando las pruebas se completan con éxito, deberías ver una salida similar a:

### Ejemplo de salida de test

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** phases_example.test_phases                      PASS         200.00           0.00     232758.27  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 200.00           0.00     123000.12  **
```

### Conteos esperados de pruebas

- **Ejemplo Jerarquía de Clases**: 1 test
- **Ejemplo Fases**: 1 test
- **Ejemplo Reporting**: 2 tests
- **Ejemplo ConfigDB**: 2 tests
- **Ejemplo Factory**: 2 tests
- **Ejemplo Objeciones**: 2 tests
- **Test UVM simple**: 1 test
- **Total**: 11 tests en todos los ejemplos y testbenches

## Solución de problemas

### Problemas comunes

#### 1. Error de versión de Verilator

**Error:** `cocotb requires Verilator 5.036 or later, but using 5.020`

**Solución:** Actualizar Verilator a 5.036 o posterior:

```bash
./scripts/install_verilator.sh --from-submodule --force
```

#### 2. Errores de módulo no encontrado

**Error:** `ModuleNotFoundError: No module named 'pyuvm'` o `ModuleNotFoundError: No module named 'cocotb'`

**Solución:** Activar el entorno virtual:

```bash
source .venv/bin/activate
```

#### 3. Errores de ejecución de fases

**Error:** `RuntimeWarning: coroutine 'Test.build_phase' was never awaited`

**Solución:** Esta es una advertencia conocida en pyuvm cuando las fases son llamadas de forma síncrona. No afecta la funcionalidad. El planificador de fases de UVM ejecuta las fases correctamente.

#### 4. Override del factory que no funciona

**Error:** El override parece no tener efecto

**Solución:**
- Asegurarse de que el override se establece en `build_phase()` antes de crear componentes
- Usar `set_type_override()` para todos los casos, o `set_inst_override()` para instancias específicas
- Verificar que la clase base sea la usada en las llamadas `create()`

#### 5. Objeciones que no funcionan

**Error:** La simulación termina demasiado pronto o se queda colgada

**Solución:**
- Asegurarse de llamar a `raise_objection()` al inicio de `run_phase()` si se realiza trabajo
- Asegurarse de llamar a `drop_objection()` cuando el trabajo termine
- Verificar que todos los componentes hayan soltado sus objeciones
- Las objeciones sólo funcionan en fases asíncronas (run-time)

#### 6. Fallo en la búsqueda de ConfigDB

**Error:** No se encuentra la configuración en ConfigDB

**Solución:**
- Verificar que la configuración se establezca antes de que los componentes intenten obtenerla
- Comprobar que la ruta jerárquica coincida exactamente
- Usar `None` para configuración global, o el componente para rutas específicas
- Asegurarse de establecer configuración en el `build_phase()` del padre antes del `build_phase()` del hijo

### Consejos de depuración

1. **Comprobar instalación de pyuvm:**
   ```bash
   python3 -c "import pyuvm; print(pyuvm.__version__)"
   ```

2. **Verificar entorno virtual:**
   ```bash
   which python3  # Debe apuntar a .venv/bin/python3
   python3 -c "import cocotb; import pyuvm"
   ```

3. **Habilitar logging verboso:**
   ```python
   # Establecer verbosidad UVM en el test
   uvm_report_object.set_report_verbosity_level(UVM_DEBUG)
   ```

4. **Comprobar ejecución de fases:**
   - Añadir logging en cada fase para verificar el orden de ejecución
   - Usar `report_phase()` para confirmar finalización del test

5. **Inspeccionar jerarquía de componentes:**
   ```python
   # Imprimir la topología de componentes
   self.print_topology()
   ```

6. **Comprobar contador de objeciones:**
   ```python
   # Consultar contador de objeciones
   objection_count = uvm_objection().get_objection_count()
   self.logger.info(f"Objection count: {objection_count}")
   ```

## Temas cubiertos

1. **Introducción a UVM** - Entender la metodología UVM y sus ventajas
2. **Jerarquía de clases** - Clases base UVM (`uvm_object`, `uvm_component`) y herencia
3. **Fases UVM** - Fases de compilación, ejecución y limpieza
4. **Sistema de reporting** - Niveles de severidad, verbosidad y formato de mensajes
5. **ConfigDB** - Base de datos de configuración para pruebas flexibles
6. **Patrón Factory** - Creación centralizada y overrides de tipos/instancias
7. **Clases de test** - Cómo crear y estructurar tests UVM
8. **Estructura del entorno** - Construir entornos UVM con agentes
9. **Mecanismo de objeciones** - Control de ejecución del test y finalización de fases
10. **Comunicación entre componentes** - Puertos TLM, exports y analysis ports
11. **Sequence/Sequencer/Driver** - Generación y procesamiento de transacciones
12. **Monitor y Scoreboard** - Observación del DUT y verificación de resultados

## Próximos pasos

Después de completar el Módulo 3, procede a:

- **Módulo 4**: Componentes UVM - Implementación detallada de agent, driver, monitor, sequencer
- **Módulo 5**: UVM avanzado - Callbacks, coverage, modelo de registros, secuencias virtuales
- **Módulo 6**: Verificación de protocolos - Testbenches multi-agente, verificadores de protocolo
- **Módulo 7**: Temas avanzados - DMA, integración de VIP, buenas prácticas

## Recursos adicionales

- [pyuvm Documentation](https://pyuvm.readthedocs.io/)
- [UVM User's Guide](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_1.2.pdf)
- [cocotb Documentation](https://docs.cocotb.org/)
- [Verilator Documentation](https://verilator.org/)

## Descripción de archivos

### Ejemplos

| File | Description | Tests |
|------|-------------|-------|
| `class_hierarchy_example.py` | Jerarquía de clases UVM y estructura de componentes | 1 función de test |
| `phases_example.py` | Implementación y ejecución de fases UVM | 1 función de test |
| `reporting_example.py` | Sistema de reporting UVM | 2 funciones de test |
| `configdb_example.py` | Base de datos de configuración UVM | 2 funciones de test |
| `factory_example.py` | Patrón factory UVM | 2 funciones de test |
| `objections_example.py` | Mecanismo de objeciones UVM | 2 funciones de test |

### Módulos DUT

| File | Description | Ports |
|------|-------------|-------|
| `adder.v` | Sumador de 8 bits con acarreo | `clk`, `rst_n`, `a[7:0]`, `b[7:0]`, `sum[7:0]`, `carry` |

### Testbenches

| File | Framework | Description | Tests |
|------|-----------|-------------|-------|
| `test_simple_uvm.py` | pyuvm | Testbench UVM completo para el sumador | 1 test UVM |

---

Para preguntas o problemas, consulta el README principal del proyecto o revisa los logs de test para mensajes de error detallados.
