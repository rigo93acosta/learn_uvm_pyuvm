# Módulo 4: Componentes UVM

**Objetivo**: Construir agentes UVM completos con driver, monitor y sequencer

## Visión general

Este módulo cubre los componentes centrales de UVM que se usan para construir entornos de verificación. Aprenderás a crear agentes, drivers, monitores, sequencers y secuencias para construir entornos de verificación completos.

### Ejemplos y estructura de código

Este módulo incluye ejemplos completos y bancos de pruebas ubicados en el directorio `module4/`:

```
module4/
├── examples/              # ejemplos de pyuvm para cada tema
│   ├── drivers/          # ejemplos de implementación de drivers
│   ├── monitors/         # ejemplos de implementación de monitores
│   ├── sequencers/       # ejemplos de sequencers y secuencias
│   ├── tlm/              # ejemplos de comunicación TLM
│   ├── scoreboards/      # ejemplos de scoreboards
│   ├── transactions/     # ejemplos de modelado de transacciones
│   └── agents/           # ejemplos de agentes completos
├── dut/                   # módulos Verilog Design Under Test
│   └── interfaces/       # interfaces para pruebas
├── tests/                 # bancos de pruebas
│   └── pyuvm_tests/      # bancos de pruebas pyuvm
└── README.md             # documentación del Módulo 4
```

### Inicio rápido

**Ejecutar todos los ejemplos usando el script orquestador:**
```bash
# Ejecutar todos los ejemplos
./scripts/module4.sh

# Ejecutar ejemplos específicos
./scripts/module4.sh --drivers
./scripts/module4.sh --monitors
./scripts/module4.sh --sequencers
./scripts/module4.sh --tlm
./scripts/module4.sh --scoreboards
./scripts/module4.sh --transactions
./scripts/module4.sh --agents
./scripts/module4.sh --pyuvm-tests
```

**Ejecutar ejemplos individualmente:**
```bash
# Activar el entorno virtual (si usas uno)
source .venv/bin/activate

# Ejecutar pruebas pyuvm
cd module4/tests/pyuvm_tests
make SIM=verilator TEST=test_complete_agent

# Los ejemplos son ejemplos estructurales de pyuvm
# Se pueden importar y usar en tus bancos de pruebas
```

## Temas cubiertos

### 1. Arquitectura de un agente UVM

- **Visión general del agente**
  - ¿Qué es un agente?
  - Componentes del agente
  - Propósito del agente
  - Tipos de agentes

- **Agentes activos vs pasivos**
  - Agentes activos (driver + sequencer + monitor)
  - Agentes pasivos (solo monitor)
  - Cuándo usar cada uno
  - Configuración del agente

- **Estructura del agente**
  - Componente driver
  - Componente monitor
  - Componente sequencer
  - Contenedor del agente

### 2. Implementación de un driver UVM

- **Visión general del driver**
  - Propósito del driver
  - Responsabilidades del driver
  - Interfaz del driver
  - Ciclo de vida del driver

- **Implementación del driver**
  - Herencia de `uvm_driver`
  - Implementación de `run_phase()`
  - Recepción de transacciones
  - Conducción de señales

- **Comunicación driver-sequencer**
  - Interfaz `seq_item_port`
  - `get_next_item()`
  - `item_done()`
  - Flujo de transacciones

- **Conducción a nivel de señal**
  - Acceso a señales del DUT
  - Asignación de valores a señales
  - Control de temporización
  - Implementación del protocolo

### 3. Implementación de un monitor UVM

- **Visión general del monitor**
  - Propósito del monitor
  - Responsabilidades del monitor
  - Tipos de monitor
  - Ciclo de vida del monitor

- **Implementación del monitor**
  - Herencia de `uvm_monitor`
  - Implementación de `run_phase()`
  - Muestreo de señales
  - Creación de transacciones

- **Puertos de análisis**
  - Propósito del puerto de análisis
  - Creación de puertos de análisis
  - Escritura en puertos de análisis
  - Conexiones de puertos de análisis

- **Creación de transacciones**
  - Muestreo de señales
  - Creación de objetos de transacción
  - Población de campos de transacción
  - Difusión de transacciones

### 4. Sequencer UVM y secuencias

- **Visión general del sequencer**
  - Propósito del sequencer
  - Responsabilidades del sequencer
  - Tipos de sequencer
  - Ciclo de vida del sequencer

- **Implementación del sequencer**
  - Herencia de `uvm_sequencer`
  - Uso del sequencer por defecto
  - Funcionalidades de sequencers personalizados
  - Configuración del sequencer

- **Elementos de secuencia**
  - Clase base `uvm_sequence_item`
  - Definición de transacciones
  - Campos de transacción
  - Métodos de transacción

- **Conceptos básicos de secuencias**
  - Clase base `uvm_sequence`
  - Método `body()`
  - Ejecución de secuencias
  - Ciclo de vida de la secuencia

- **Operaciones de secuencia**
  - `start_item()`
  - `finish_item()`
  - `wait_for_grant()`
  - Creación de transacciones

### 5. TLM (Transaction-Level Modeling) - Cobertura completa

- **Visión general de TLM**
  - ¿Qué es TLM?
  - Beneficios de TLM
  - Niveles de abstracción de TLM
  - Patrones de comunicación TLM

- **Tipos de interfaz TLM**
  - Interfaz `put` - put bloqueante unidireccional
  - Interfaz `get` - get bloqueante unidireccional
  - Interfaz `peek` - peek no bloqueante unidireccional
  - Interfaz `transport` - transport bloqueante bidireccional
  - Características de las interfaces y casos de uso

- **Tipos de puertos TLM**
  - `uvm_put_port` - puerto put
  - `uvm_get_port` - puerto get
  - `uvm_peek_port` - puerto peek
  - `uvm_transport_port` - puerto transport
  - Puerto vs export vs implementación

- **Tipos de exports TLM**
  - `uvm_put_export` - export put
  - `uvm_get_export` - export get
  - `uvm_peek_export` - export peek
  - `uvm_transport_export` - export transport
  - Patrones de uso de exports

- **Tipos de implementación TLM**
  - `uvm_put_imp` - implementación put
  - `uvm_get_imp` - implementación get
  - `uvm_peek_imp` - implementación peek
  - `uvm_transport_imp` - implementación transport
  - Requisitos de implementación

- **Puertos y exports de análisis (tipo especial de TLM)**
  - Concepto de puerto de análisis
  - Patrón publicador-suscriptor
  - Comunicación de difusión
  - Conexiones uno a muchos
  - `uvm_analysis_port` - puerto de análisis
  - `uvm_analysis_export` - export de análisis
  - `uvm_analysis_imp` - implementación de análisis
  - Patrones de conexión

- **FIFOs TLM**
  - `uvm_tlm_fifo` - FIFO TLM
  - Propósito y uso de la FIFO
  - Capacidad de la FIFO y comportamiento bloqueante
  - Patrones de conexión de FIFO
  - Cuándo usar FIFOs

- **Patrones de conexión TLM**
  - Conexiones directas (puerto a export)
  - Conexiones con FIFO (puerto a FIFO a export)
  - Conexiones de múltiples puertos
  - Conexiones jerárquicas
  - Buenas prácticas de conexión

- **Patrones de uso TLM**
  - Patrón productor-consumidor
  - Patrón solicitud-respuesta
  - Patrón de difusión
  - Patrón de pipeline
  - TLM vs puertos de análisis

- **Ejemplos de implementación TLM**
  - Uso de interfaces put/get
  - Uso de la interfaz transport
  - Uso de FIFOs TLM
  - Combinación de tipos TLM
  - Depuración de TLM

### 6. Implementación de Scoreboard

- **Visión general del scoreboard**
  - Propósito del scoreboard
  - Tipos de scoreboard
  - Responsabilidades del scoreboard
  - Ciclo de vida del scoreboard

- **Implementación del scoreboard**
  - Herencia de `uvm_component`
  - Conexiones de puertos de análisis
  - Almacenamiento de transacciones
  - Lógica de comparación

- **Patrones de scoreboard**
  - Comparación con modelo de referencia
  - Esperado vs actual
  - Emparejamiento de transacciones
  - Reporte de errores

- **Scoreboards avanzados**
  - Scoreboards multicanal
  - Emparejamiento basado en tiempo
  - Lógica de comparación compleja
  - Optimización de rendimiento

### 7. Modelado a nivel de transacción

- **Conceptos de transacción**
  - ¿Qué son las transacciones?
  - Abstracción de transacciones
  - Campos de transacción
  - Métodos de transacción

- **Diseño de transacciones**
  - Estructura de la clase de transacción
  - Definición de campos
  - Definición de restricciones
  - Implementación de métodos

- **Operaciones de transacción**
  - Creación de transacciones
  - Copia de transacciones
  - Comparación de transacciones
  - Conversión de transacciones

### 8. Ejemplo de agente completo

- **Estructura del agente**
  - Definición de la clase agente
  - Instanciación de componentes
  - Conexiones entre componentes
  - Configuración del agente

- **Build phase del agente**
  - Creación de componentes
  - Aplicación de configuración
  - Selección activo/pasivo

- **Connect phase del agente**
  - Conexión driver-sequencer
  - Puerto de análisis del monitor
  - Conexiones externas

### 9. Bibliotecas de secuencias

- **Organización de secuencias**
  - Secuencias base
  - Secuencias derivadas
  - Bibliotecas de secuencias
  - Reutilización de secuencias

- **Secuencias comunes**
  - Secuencias simples
  - Secuencias aleatorias
  - Secuencias restringidas
  - Secuencias por capas

### 10. Integración de agentes

- **Integración con el entorno**
  - Añadir agentes al entorno
  - Configuración del agente
  - Conexiones del agente
  - Coordinación del agente

- **Integración con el test**
  - Instanciación del agente
  - Ejecución de secuencias
  - Coordinación del test
  - Verificación de resultados

## Resultados de aprendizaje

Al final de este módulo, deberías ser capaz de:

- Entender la arquitectura de agentes
- Implementar drivers UVM
- Implementar monitores UVM
- Implementar sequencers y secuencias
- Usar puertos de análisis de forma efectiva
- Implementar scoreboards
- Diseñar modelos de transacción
- Construir agentes completos
- Integrar agentes en entornos
- Ejecutar secuencias en tests

## Casos de prueba

### Caso de prueba 4.1: Driver simple
**Objetivo**: Implementar un driver básico

**Temas**:
- Clase driver
- Recepción de transacciones
- Conducción de señales

#### Ejemplo 4.1: Implementación del driver (`module4/examples/drivers/driver_example.py`)

**Lo que demuestra:**
- **Estructura de la clase driver**: Herencia de `uvm_driver`
- **Puerto del sequencer**: Creación de `seq_item_port` para la recepción de transacciones
- **Recepción de transacciones**: Uso de `get_next_item()` para recibir transacciones
- **Conducción de señales**: Conducción de señales del DUT según los campos de la transacción
- **Implementación del protocolo**: Demostración de conducción de señales específica del protocolo
- **Comunicación driver-sequencer**: `item_done()` para señalar la finalización

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module4.sh --drivers

# O directamente (verificación de sintaxis)
cd module4/examples/drivers
python3 -c "import pyuvm; exec(open('driver_example.py').read())"
```

**Salida esperada:**
```
============================================================
Prueba del ejemplo del driver
============================================================
[driver] Construyendo driver
[driver] Conectando driver
[driver] Iniciando run_phase del driver
[driver] Transacción recibida: data=0x00, addr=0x0000
[driver] Conduciendo transacción: data=0x00, addr=0x0000
[driver] Señales conducidas: data=0x00, addr=0x0000
[driver] Transacción completada
```

**Conceptos clave:**
- **`uvm_driver`**: Clase base para todos los drivers
- **`seq_item_port`**: Puerto para recibir transacciones desde el sequencer
- **`get_next_item()`**: Obtener la siguiente transacción del sequencer
- **`item_done()`**: Señalar la finalización de la transacción al sequencer
- **`run_phase()`**: Bucle principal del driver
- **Implementación del protocolo**: Conducir señales según la temporización del protocolo

### Caso de prueba 4.2: Monitor simple
**Objetivo**: Implementar un monitor básico

**Temas**:
- Clase monitor
- Muestreo de señales
- Puertos de análisis

#### Ejemplo 4.2: Implementación del monitor (`module4/examples/monitors/monitor_example.py`)

**Lo que demuestra:**
- **Estructura de la clase monitor**: Herencia de `uvm_monitor`
- **Puerto de análisis**: Creación de `uvm_analysis_port` para difundir transacciones
- **Muestreo de señales**: Muestreo de señales del DUT y creación de transacciones
- **Creación de transacciones**: Creación de objetos de transacción a partir de señales muestreadas
- **Difusión por puerto de análisis**: Uso de `write()` para difundir transacciones
- **Muestreo consciente del protocolo**: Patrones de muestreo específicos del protocolo

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module4.sh --monitors

# O directamente
cd module4/examples/monitors
python3 -c "import pyuvm; exec(open('monitor_example.py').read())"
```

**Salida esperada:**
```
============================================================
Prueba del ejemplo del monitor
============================================================
[monitor] Construyendo monitor
[monitor] Iniciando run_phase del monitor
[monitor] Transacción muestreada: data=0xAB, addr=0x1000, time=0ns
[monitor] Transacción difundida vía puerto de análisis
```

**Conceptos clave:**
- **`uvm_monitor`**: Clase base para todos los monitores
- **`uvm_analysis_port`**: Puerto para difundir transacciones
- **`write()`**: Método para difundir transacciones mediante el puerto de análisis
- **Muestreo de señales**: Esperar datos válidos, muestrear señales, crear transacciones
- **Difusión de transacciones**: Patrón de comunicación uno a muchos
- **Monitoreo del protocolo**: Monitorear eventos específicos del protocolo

### Caso de prueba 4.3: Sequencer y secuencia simples
**Objetivo**: Implementar un sequencer y una secuencia

**Temas**:
- Clase sequencer
- Elementos de secuencia
- Ejecución de secuencias

#### Ejemplo 4.3: Sequencer y secuencias (`module4/examples/sequencers/sequencer_example.py`)

**Lo que demuestra:**
- **Clase de secuencia**: Herencia de `uvm_sequence`
- **Cuerpo de la secuencia**: Implementación del método `body()` para la ejecución de la secuencia
- **Creación de transacciones**: Creación de sequence items dentro de las secuencias
- **Operaciones de secuencia**: `start_item()` y `finish_item()` para el flujo de transacciones
- **Secuencias aleatorias**: Generación de transacciones aleatorias
- **Secuencias por capas**: Llamada a otras secuencias desde dentro de una secuencia
- **Ejecución de secuencias**: Inicio de secuencias sobre sequencers

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module4.sh --sequencers

# O directamente
cd module4/examples/sequencers
python3 -c "import pyuvm; exec(open('sequencer_example.py').read())"
```

**Salida esperada:**
```
============================================================
Prueba del ejemplo del sequencer
============================================================
Iniciando SimpleSequence
[seq1] Iniciando cuerpo de la secuencia
[seq1] Creando transacción 0: data=0x00, addr=0x0000
[seq1] Item iniciado: data=0x00, addr=0x0000
[seq1] Item finalizado: data=0x00, addr=0x0000
...
[seq1] Cuerpo de la secuencia completado
```

**Conceptos clave:**
- **`uvm_sequence`**: Clase base para todas las secuencias
- **`body()`**: Método principal de ejecución de la secuencia
- **`start_item()`**: Solicitar una transacción al sequencer
- **`finish_item()`**: Enviar la transacción al driver
- **`uvm_sequencer`**: Gestiona la ejecución de secuencias
- **Secuencias por capas**: Las secuencias pueden llamar a otras secuencias
- **Generación aleatoria**: Generar transacciones aleatorias con restricciones

### Caso de prueba 4.4: Agente completo
**Objetivo**: Construir un agente completo

**Temas**:
- Estructura del agente
- Integración de componentes
- Conexiones

#### Ejemplo 4.4: Agente completo (`module4/examples/agents/agent_example.py`)

**Lo que demuestra:**
- **Estructura del agente**: Agente completo con driver, monitor y sequencer
- **Activo vs pasivo**: Configuración del agente para modos activos/pasivos
- **Integración de componentes**: Construcción del agente a partir de componentes
- **Conexiones entre componentes**: Conexión del driver al sequencer
- **Configuración del agente**: Uso de ConfigDB para configurar el agente
- **Integración con el entorno**: Integración del agente en el entorno

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module4.sh --agents

# O directamente
cd module4/examples/agents
python3 -c "import pyuvm; exec(open('agent_example.py').read())"
```

**Salida esperada:**
```
============================================================
Prueba del ejemplo de agente completo
============================================================
[agent] Construyendo agente completo
[agent] Modo del agente: ACTIVE
[agent] Creado driver y sequencer
[driver] Construyendo driver
[monitor] Construyendo monitor
[agent] Conectando agente
[agent] Driver conectado al sequencer
```

**Conceptos clave:**
- **`uvm_agent`**: Contenedor para driver, monitor y sequencer
- **Agente activo**: Contiene driver, sequencer y monitor
- **Agente pasivo**: Contiene solo monitor
- **Integración de componentes**: El agente construye y conecta todos los componentes
- **ConfigDB**: Configura el modo del agente (activo/pasivo)
- **Integración con el entorno**: El agente se conecta con componentes del entorno

### Caso de prueba 4.5: Scoreboard
**Objetivo**: Implementar un scoreboard

**Temas**:
- Clase scoreboard
- Conexiones de análisis
- Lógica de comparación

#### Ejemplo 4.5: Implementación del scoreboard (`module4/examples/scoreboards/scoreboard_example.py`)

**Lo que demuestra:**
- **Clase scoreboard**: Herencia de `uvm_scoreboard`
- **Export de análisis**: Creación de `uvm_analysis_export` y `uvm_analysis_imp`
- **Recepción de transacciones**: Implementación del método `write()` para recibir transacciones
- **Lógica de comparación**: Comparación entre transacciones esperadas y reales
- **Modelo de referencia**: Uso de un modelo de referencia para calcular el valor esperado
- **Reporte de errores**: Reporte de discrepancias y estadísticas

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module4.sh --scoreboards

# O directamente
cd module4/examples/scoreboards
python3 -c "import pyuvm; exec(open('scoreboard_example.py').read())"
```

**Salida esperada:**
```
============================================================
Prueba del ejemplo de scoreboard
============================================================
[scoreboard] Construyendo scoreboard
[scoreboard] Transacción recibida: data=0x00, expected=0x00, actual=0x00
[scoreboard] Coincidencia: expected=0x00, actual=0x00
[scoreboard] Discrepancia: expected=0x20, actual=0xFF
============================================================
[scoreboard] Verificación del scoreboard
  Total esperado: 0
  Total real: 5
  Discrepancias: 1
```

**Conceptos clave:**
- **`uvm_scoreboard`**: Clase base para scoreboards
- **`uvm_analysis_export`**: Export para recibir transacciones
- **`uvm_analysis_imp`**: Implementación de la interfaz de análisis
- **`write()`**: Método llamado cuando se recibe una transacción
- **Lógica de comparación**: Comparar valores esperados y reales
- **Modelo de referencia**: Calcular valores esperados usando un modelo de referencia
- **Reporte de errores**: Reportar discrepancias en `check_phase`

#### Ejemplo 4.6: Comunicación TLM (`module4/examples/tlm/tlm_example.py`)

**Lo que demuestra:**
- **Interfaz TLM put**: Patrón productor-consumidor con puerto/export put
- **Interfaz TLM get**: Patrón productor-consumidor con puerto/export get
- **Interfaz TLM transport**: Patrón solicitud-respuesta
- **FIFO TLM**: Uso de `uvm_tlm_fifo` para almacenamiento intermedio
- **Conexiones TLM**: Conexión de puertos, exports e implementaciones
- **Patrones TLM**: Diferentes patrones de comunicación TLM

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module4.sh --tlm

# O directamente
cd module4/examples/tlm
python3 -c "import pyuvm; exec(open('tlm_example.py').read())"
```

**Conceptos clave:**
- **`uvm_put_port`**: Puerto para enviar transacciones
- **`uvm_put_export`**: Export para recibir transacciones
- **`uvm_put_imp`**: Implementación de la interfaz put
- **`uvm_get_port`**: Puerto para recibir transacciones
- **`uvm_transport_port`**: Puerto para solicitud-respuesta
- **`uvm_tlm_fifo`**: FIFO para almacenamiento de transacciones
- **Patrones TLM**: Productor-consumidor, solicitud-respuesta, difusión

#### Ejemplo 4.7: Modelado de transacciones (`module4/examples/transactions/transaction_example.py`)

**Lo que demuestra:**
- **Diseño de transacciones**: Clases de transacción base y extendidas
- **Métodos de transacción**: `copy()`, `__eq__()`, `__str__()`
- **Transacciones con restricciones**: Randomización con restricciones
- **Empaquetado de transacciones**: pack/unpack para serialización
- **Comparación de transacciones**: Métodos de igualdad y comparación

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module4.sh --transactions

# O directamente
cd module4/examples/transactions
python3 -c "import pyuvm; exec(open('transaction_example.py').read())"
```

**Conceptos clave:**
- **`uvm_sequence_item`**: Clase base para todas las transacciones
- **Campos de transacción**: Definir los campos de datos de la transacción
- **Métodos de transacción**: Implementar métodos útiles (copy, compare, convert)
- **Restricciones**: Definir restricciones de randomización
- **Serialización**: pack/unpack para comunicación

#### Prueba: Test del agente completo (`module4/tests/pyuvm_tests/test_complete_agent.py`)

**Lo que demuestra:**
- Banco de pruebas UVM completo con todos los componentes
- Integración de driver, monitor, sequencer y scoreboard
- Ejecución de secuencias
- Conexiones de puertos de análisis
- Flujo completo de la prueba

**Ejecución:**
```bash
# Usando el script orquestador
./scripts/module4.sh --pyuvm-tests

# O manualmente
cd module4/tests/pyuvm_tests
make SIM=verilator TEST=test_complete_agent
```

**Estructura de la prueba:**
- `InterfaceTransaction`: Transacción para la prueba de interfaz
- `InterfaceSequence`: Genera vectores de prueba
- `InterfaceDriver`: Conduce transacciones hacia el DUT
- `InterfaceMonitor`: Monitorea las salidas del DUT
- `InterfaceScoreboard`: Verifica resultados
- `InterfaceAgent`: Contiene driver, monitor y sequencer
- `InterfaceEnv`: Contiene el agente y el scoreboard
- `CompleteAgentTest`: Clase de test de nivel superior

### Módulos del Design Under Test (DUT)

#### Interfaz simple (`module4/dut/interfaces/simple_interface.v`)
- **Propósito**: Interfaz simple con handshaking valid/ready
- **Usada en**: Test del agente completo
- **Características**: Operación sincronizada con reloj, reset, buses de datos/dirección, salida de resultado

## Ejercicios

1. **Implementación del driver**
   - Crear la clase driver
   - Implementar la conducción de señales
   - Manejar transacciones
   - **Ubicación**: Extender `module4/examples/drivers/driver_example.py`
   - **Pista**: Añadir conducción de señales específica del protocolo con temporización

2. **Implementación del monitor**
   - Crear la clase monitor
   - Muestrear señales
   - Difundir transacciones
   - **Ubicación**: Extender `module4/examples/monitors/monitor_example.py`
   - **Pista**: Añadir muestreo de señales consciente del protocolo

3. **Creación de secuencias**
   - Crear elementos de secuencia
   - Crear secuencias
   - Ejecutar secuencias
   - **Ubicación**: Extender `module4/examples/sequencers/sequencer_example.py`
   - **Pista**: Crear secuencias aleatorias con restricciones

4. **Construcción de agentes**
   - Construir un agente completo
   - Integrar componentes
   - Probar el agente
   - **Ubicación**: Extender `module4/examples/agents/agent_example.py`
   - **Pista**: Añadir configuración para modos activo/pasivo

5. **Implementación de scoreboard**
   - Crear scoreboard
   - Conectar puertos de análisis
   - Implementar comprobaciones
   - **Ubicación**: Extender `module4/examples/scoreboards/scoreboard_example.py`
   - **Pista**: Añadir un modelo de referencia para calcular el valor esperado

## Evaluación

- [ ] Entiende la arquitectura de agentes
- [ ] Puede implementar drivers
- [ ] Puede implementar monitores
- [ ] Puede implementar sequencers
- [ ] Puede crear secuencias
- [ ] Puede usar puertos de análisis
- [ ] Puede implementar scoreboards
- [ ] Puede construir agentes completos
- [ ] Puede integrar agentes
- [ ] Puede ejecutar secuencias

## Próximos pasos

Después de completar este módulo, continúa con [Módulo 5: Conceptos avanzados de UVM](MODULE5.md) para aprender características avanzadas de UVM.

## Recursos adicionales

- **Documentación de pyuvm**: https://pyuvm.readthedocs.io/
- **Guía del usuario de UVM 1.2**: Accellera Systems Initiative
- **The UVM Primer**: Ray Salemi
- **Ejemplos de pyuvm**: https://github.com/pyuvm/pyuvm/tree/main/examples

## Solución de problemas

### Problemas comunes

**Problema: error "pyuvm not found"**
```bash
# Solución: Instalar pyuvm
./scripts/install_pyuvm.sh --pip --venv .venv
# O
./scripts/module0.sh
```

**Problema: el driver no recibe transacciones**
```bash
# Solución: verificar la conexión driver-sequencer
# Asegúrate de que: driver.seq_item_port.connect(sequencer.seq_item_export)
# Verifica que la secuencia se inicie en el sequencer correcto
```

**Problema: el monitor no difunde transacciones**
```bash
# Solución: verificar la conexión del puerto de análisis
# Asegúrate de que: monitor.ap.connect(scoreboard.ap)
# Verifica que el método write() esté implementado en el scoreboard
```

**Problema: la secuencia no se ejecuta**
```bash
# Solución: verificar que la secuencia se inicie en el sequencer
# Asegúrate de que: await seq.start(sequencer)
# Verifica que el sequencer esté conectado al driver
```

**Problema: el scoreboard no recibe transacciones**
```bash
# Solución: verificar las conexiones de los puertos de análisis
# Asegúrate de que: monitor.ap.connect(scoreboard.ap)
# Verifica que el scoreboard tenga uvm_analysis_imp con un método write()
```

### Obtener ayuda

- Revisa los comentarios del código de ejemplo para obtener explicaciones detalladas
- Consulta `module4/README.md` para ver la estructura del directorio
- Ejecuta los ejemplos individualmente para entender cada componente
- Estudia la comunicación driver-sequencer en `driver_example.py`
- Revisa el uso de puertos de análisis en `monitor_example.py` y `scoreboard_example.py`