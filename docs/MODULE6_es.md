# Módulo 6: Testbenches Complejos

**Objetivo**: Construir testbenches multi-agente complejos con verificación de protocolo

## Resumen

Este módulo se enfoca en construir entornos de verificación complejos con múltiples agentes, verificación de protocolo, arquitectura avanzada de testbench y técnicas de depuración. Aprenderás patrones de la industria y mejores prácticas.

### Ejemplos y Estructura de Código

Este módulo incluye ejemplos completos y testbenches ubicados en el directorio `module6/`:

```
module6/
├── examples/              # Ejemplos de pyuvm para cada tema
│   ├── multi_agent/      # Ejemplos de entorno multi-agente
│   ├── protocol/         # Ejemplos de verificación de protocolo
│   ├── protocol_checkers/# Ejemplos de verificadores de protocolo
│   ├── scoreboards/      # Ejemplos de scoreboard multi-canal
│   └── architecture/     # Ejemplos de arquitectura de testbench
├── dut/                   # Módulos Verilog Design Under Test
│   └── protocols/        # Módulos de protocolo para pruebas
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # Testbenches pyuvm
└── README.md             # Documentación del Módulo 6
```

### Inicio Rápido

**Ejecutar todos los ejemplos usando el script orquestador:**
```bash
# Ejecutar todos los ejemplos
./scripts/module6.sh

# Ejecutar ejemplos específicos
./scripts/module6.sh --multi-agent
./scripts/module6.sh --protocol
./scripts/module6.sh --protocol-checkers
./scripts/module6.sh --scoreboards
./scripts/module6.sh --architecture
./scripts/module6.sh --pyuvm-tests
```

**Ejecutar ejemplos individualmente:**
```bash
# Activar entorno virtual (si usas uno)
source .venv/bin/activate

# Ejecutar pruebas pyuvm
cd module6/tests/pyuvm_tests
make SIM=verilator TEST=test_complex_testbench

# Los ejemplos son ejemplos estructurales de pyuvm
# Se pueden importar y usar en tus testbenches
```

## Temas Cubiertos

### 1. Entornos Multi-Agente

- **Arquitectura del Entorno**
  - Coordinación de múltiples agentes
  - Comunicación entre agentes
  - Jerarquía del entorno
  - Patrones de entorno

- **Coordinación de Agentes**
  - Agentes maestro-esclavo
  - Agentes peer-to-peer
  - Agentes multi-canal
  - Sincronización de agentes

- **Patrones de Entorno**
  - Entornos en capas
  - Entornos jerárquicos
  - Entornos planos
  - Entornos mixtos

### 2. Verificación de Protocolo

- **Resumen de Verificación de Protocolo**
  - ¿Qué es la verificación de protocolo?
  - Cumplimiento de protocolo
  - Verificación de protocolo
  - Cobertura de protocolo

- **Verificación de Protocolo AXI**
  - Conceptos básicos del protocolo AXI
  - Agente AXI4-Lite
  - Agente AXI4
  - Verificador de protocolo AXI

- **Verificación de Protocolo Personalizado**
  - Definición de protocolo
  - Creación de agente de protocolo
  - Implementación de verificador de protocolo
  - Cobertura de protocolo

- **Verificadores de Protocolo**
  - Implementación del verificador
  - Verificación de reglas de protocolo
  - Detección de errores
  - Cumplimiento de protocolo

### 3. Patrones de Arquitectura de Testbench

- **Testbench en Capas**
  - Capas de abstracción
  - Comunicación entre capas
  - Organización de capas
  - Patrones de capas

- **Componentes Reutilizables**
  - Diseño de componentes
  - Reutilización de componentes
  - Librerías de componentes
  - Patrones de componentes

- **Plantillas de Testbench**
  - Plantillas estándar
  - Personalización de plantillas
  - Patrones de plantillas
  - Mejores prácticas de plantillas

### 4. Depuración y Análisis

- **Técnicas de Depuración UVM**
  - Depuración de fases
  - Depuración de componentes
  - Depuración de transacciones
  - Depuración de configuración

- **Grabación de Transacciones**
  - Logging de transacciones
  - Trazado de transacciones
  - Reproducción de transacciones
  - Análisis de transacciones

- **Análisis de Formas de Onda**
  - Generación de VCD/FST
  - Visualización de formas de onda
  - Trazado de señales
  - Análisis temporal

- **Análisis de Logs**
  - Análisis de logs
  - Análisis de errores
  - Análisis de rendimiento
  - Análisis de cobertura

### 5. Verificación Multi-Canal

- **Coordinación de Canales**
  - Múltiples canales
  - Sincronización de canales
  - Independencia de canales
  - Patrones de canales

- **Interfaces Bidireccionales**
  - Interfaces maestro-esclavo
  - Agentes bidireccionales
  - Coordinación de interfaces
  - Patrones de interfaces

### 6. Verificación de Rendimiento

- **Monitoreo de Rendimiento**
  - Métricas de rendimiento
  - Recolección de rendimiento
  - Análisis de rendimiento
  - Reporte de rendimiento

- **Análisis de Throughput**
  - Medición de throughput
  - Análisis de ancho de banda
  - Medición de latencia
  - Optimización de rendimiento

### 7. Inyección de Errores y Recuperación

- **Inyección de Errores**
  - Escenarios de error
  - Mecanismos de inyección de errores
  - Patrones de error
  - Pruebas de error

- **Pruebas de Recuperación**
  - Escenarios de recuperación
  - Verificación de recuperación
  - Patrones de recuperación
  - Pruebas de recuperación

### 8. Integración de Testbench

- **Integración de Componentes**
  - Estrategias de integración
  - Pruebas de integración
  - Patrones de integración
  - Mejores prácticas de integración

- **Integración de Sistema**
  - Integración a nivel de sistema
  - Verificación de integración
  - Patrones de integración
  - Desafíos de integración

### 9. Scoreboarding Avanzado

- **Scoreboards Multi-Canal**
  - Verificación de múltiples canales
  - Coordinación de canales
  - Patrones de scoreboard
  - Optimización de scoreboard

- **Coincidencia Basada en Tiempo**
  - Coincidencia temporal
  - Ventanas de tiempo
  - Algoritmos de coincidencia
  - Patrones de coincidencia

### 10. Mantenimiento de Testbench

- **Organización de Código**
  - Organización de archivos
  - Organización de clases
  - Gestión de namespaces
  - Documentación

- **Control de Versiones**
  - Flujos de trabajo Git
  - Estrategias de branching
  - Revisión de código
  - Gestión de releases

## Resultados de Aprendizaje

Al final de este módulo, deberías ser capaz de:

- Diseñar entornos multi-agente
- Implementar verificación de protocolo
- Aplicar patrones de arquitectura de testbench
- Depurar testbenches complejos
- Analizar resultados de simulación
- Coordinar múltiples canales
- Monitorear rendimiento
- Integrar componentes
- Mantener testbenches
- Aplicar mejores prácticas de la industria

## Casos de Prueba

### Caso de Prueba 6.1: Entorno Multi-Agente
**Objetivo**: Crear entorno con múltiples agentes

**Temas**:
- Múltiples agentes
- Coordinación de agentes
- Estructura del entorno

#### Ejemplo 6.1: Entorno Multi-Agente (`module6/examples/multi_agent/multi_agent_example.py`)

**Qué demuestra:**
- **Instanciación de Múltiples Agentes**: Creando múltiples agentes en el entorno
- **Coordinación de Agentes**: Coordinando secuencias a través de múltiples agentes
- **Secuencia Virtual**: Usando secuencia virtual para coordinar agentes
- **Scoreboard Multi-Canal**: Scoreboard recibiendo de múltiples agentes
- **Jerarquía del Entorno**: Organizando múltiples agentes en el entorno
- **Ejecución Paralela de Agentes**: Ejecutando secuencias en múltiples agentes concurrentemente

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module6.sh --multi-agent

# O directamente (verificación de sintaxis)
cd module6/examples/multi_agent
python3 -c "import pyuvm; exec(open('multi_agent_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Multi-Agent Environment Example Test
============================================================
Building MultiAgentEnv
Building agent 0
Building agent 1
Building agent 2
[VirtualSequence] Starting multi-agent coordination
[seq_agent_0] Starting sequence for agent 0
[seq_agent_1] Starting sequence for agent 1
[seq_agent_2] Starting sequence for agent 2
...
[VirtualSequence] Multi-agent coordination completed
```

**Conceptos Clave:**
- **Múltiples Agentes**: Crear múltiples instancias de agentes en el entorno
- **Coordinación de Agentes**: Usar secuencias virtuales para coordinar agentes
- **Secuencia Virtual**: Secuencia que coordina múltiples secuenciadores
- **Scoreboard Multi-Canal**: Scoreboard con múltiples puertos de análisis
- **Organización del Entorno**: Estructurar el entorno para múltiples agentes
- **Ejecución Paralela**: Ejecutar secuencias en múltiples agentes concurrentemente

### Caso de Prueba 6.2: Agente AXI4-Lite
**Objetivo**: Crear agente de verificación AXI4-Lite

**Temas**:
- Protocolo AXI
- Agente de protocolo
- Verificador de protocolo

#### Ejemplo 6.2: Verificación de Protocolo (`module6/examples/protocol/protocol_example.py`)

**Qué demuestra:**
- **Protocolo AXI4-Lite**: Implementando protocolos de escritura y lectura AXI4-Lite
- **Driver de Protocolo**: Driver implementando handshaking AXI4-Lite
- **Monitor de Protocolo**: Monitor muestreando señales AXI4-Lite
- **Protocolo de Escritura**: Canales de dirección, datos y respuesta de escritura
- **Protocolo de Lectura**: Canales de dirección y datos de lectura
- **Agente de Protocolo**: Agente completo para verificación AXI4-Lite

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module6.sh --protocol

# O directamente
cd module6/examples/protocol
python3 -c "import pyuvm; exec(open('protocol_example.py').read())"
```

**Salida Esperada:**
```
============================================================
AXI4-Lite Protocol Example Test
============================================================
Building AXI4LiteEnv
Building AXI4-Lite agent
[driver] Building AXI4-Lite driver
[monitor] Building AXI4-Lite monitor
[driver] Starting AXI4-Lite driver
[driver] AXI4-Lite Write: WRITE: addr=0x00001000, data=0xDEADBEEF
[driver] Write address channel: addr=0x00001000
[driver] Write data channel: data=0xDEADBEEF
[driver] Write response: OKAY
```

**Conceptos Clave:**
- **Protocolo AXI4-Lite**: Protocolo AXI simplificado con 5 canales
- **Canales de Escritura**: AW (dirección), W (datos), B (respuesta)
- **Canales de Lectura**: AR (dirección), R (datos)
- **Handshaking**: Handshaking valid/ready en cada canal
- **Implementación de Protocolo**: Implementar temporización de protocolo en driver
- **Monitoreo de Protocolo**: Muestrear señales de protocolo en monitor

### Caso de Prueba 6.3: Verificador de Protocolo
**Objetivo**: Implementar verificador de cumplimiento de protocolo

**Temas**:
- Reglas de protocolo
- Implementación del verificador
- Detección de errores

#### Ejemplo 6.3: Verificador de Protocolo (`module6/examples/protocol_checkers/protocol_checker_example.py`)

**Qué demuestra:**
- **Reglas de Protocolo**: Definiendo reglas de cumplimiento de protocolo
- **Verificación de Reglas**: Verificando reglas de protocolo en tiempo real
- **Detección de Errores**: Detectando violaciones de protocolo
- **Detección de Advertencias**: Detectando advertencias de protocolo
- **Reporte de Cumplimiento**: Reportando estado de cumplimiento de protocolo
- **Seguimiento de Estado**: Rastreando estado del protocolo para verificación de reglas

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module6.sh --protocol-checkers

# O directamente
cd module6/examples/protocol_checkers
python3 -c "import pyuvm; exec(open('protocol_checker_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Protocol Checker Example Test
============================================================
Building ProtocolEnv
[checker] Checking: valid=False, ready=False, data=0x00
[checker] Warning: valid asserted without ready at time 10
[checker] Protocol OK: Valid handshake, data=0xBB
[checker] Warning: valid asserted without ready at time 40
[checker] Protocol OK: Valid handshake, data=0xEE
============================================================
[checker] Protocol Checker Report
============================================================
Total errors: 0
Total warnings: 2
✓ Protocol compliance: PASSED
```

**Conceptos Clave:**
- **Reglas de Protocolo**: Definir reglas para cumplimiento de protocolo
- **Seguimiento de Estado**: Rastrear estado anterior para verificación de reglas
- **Detección de Errores**: Detectar y reportar violaciones de protocolo
- **Detección de Advertencias**: Detectar y reportar advertencias de protocolo
- **Verificación de Cumplimiento**: Verificar cumplimiento en tiempo real
- **Reporte de Cumplimiento**: Reportar cumplimiento en check_phase

### Caso de Prueba 6.4: Scoreboard Multi-Canal
**Objetivo**: Implementar scoreboard multi-canal

**Temas**:
- Múltiples canales
- Coordinación de canales
- Patrones de scoreboard

#### Ejemplo 6.4: Scoreboard Multi-Canal (`module6/examples/scoreboards/multi_channel_scoreboard_example.py`)

**Qué demuestra:**
- **Múltiples Canales**: Scoreboard manejando múltiples canales
- **Puertos de Análisis Específicos por Canal**: Puertos de análisis separados para cada canal
- **Coordinación de Canales**: Coordinando la verificación a través de canales
- **Coincidencia Específica por Canal**: Coincidiendo esperado vs real por canal
- **Estadísticas por Canal**: Reportando estadísticas por canal
- **Patrones Multi-Canal**: Patrones para scoreboarding multi-canal

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module6.sh --scoreboards

# O directamente
cd module6/examples/scoreboards
python3 -c "import pyuvm; exec(open('multi_channel_scoreboard_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Multi-Channel Scoreboard Example Test
============================================================
[scoreboard] Building multi-channel scoreboard (3 channels)
[monitor_channel_0] Starting monitor for channel 0
[monitor_channel_1] Starting monitor for channel 1
[monitor_channel_2] Starting monitor for channel 2
[scoreboard] Received from channel 0: channel=0, data=0x00, ...
[scoreboard] Channel 0 match: expected=0x00, actual=0x00
============================================================
[scoreboard] Multi-Channel Scoreboard Check
============================================================
Channel 0:
  Expected: 0 remaining
  Actual: 5
  Matches: 5
  Mismatches: 0
...
✓ All channels: PASSED
```

**Conceptos Clave:**
- **Múltiples Canales**: Manejar transacciones de múltiples canales
- **Puertos Específicos por Canal**: Crear puertos de análisis para cada canal
- **Coincidencia por Canal**: Coincidir esperado vs real por canal
- **Estadísticas por Canal**: Rastrear estadísticas por canal
- **Coordinación de Canales**: Coordinar la verificación a través de canales
- **Patrones Multi-Canal**: Patrones reutilizables para scoreboarding multi-canal

#### Ejemplo 6.5: Arquitectura de Testbench (`module6/examples/architecture/architecture_example.py`)

**Qué demuestra:**
- **Arquitectura en Capas**: Implementando arquitectura de testbench en capas
- **Comunicación entre Capas**: Comunicación entre capas de abstracción
- **Componentes Reutilizables**: Creando componentes reutilizables y parametrizados
- **Patrones de Componentes**: Patrones para reutilización de componentes
- **Patrones de Arquitectura**: Patrones estándar de arquitectura de testbench

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module6.sh --architecture

# O directamente
cd module6/examples/architecture
python3 -c "import pyuvm; exec(open('architecture_example.py').read())"
```

**Conceptos Clave:**
- **Arquitectura en Capas**: Organizar testbench en capas de abstracción
- **Comunicación entre Capas**: Usar puertos de análisis para comunicación entre capas
- **Componentes Reutilizables**: Diseñar componentes para reutilización
- **Parametrización de Componentes**: Usar configuración para personalización de componentes
- **Patrones de Arquitectura**: Aplicar patrones de arquitectura estándar

#### Prueba: Prueba de Testbench Complejo (`module6/tests/pyuvm_tests/test_complex_testbench.py`)

**Qué demuestra:**
- Estructura completa de testbench complejo
- Integración multi-agente
- Verificación de protocolo
- Integración de scoreboard
- Flujo de prueba completo

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module6.sh --pyuvm-tests

# O manualmente
cd module6/tests/pyuvm_tests
make SIM=verilator TEST=test_complex_testbench
```

**Estructura de la Prueba:**
- `ComplexTransaction`: Transacción para testbench complejo
- `ComplexSequence`: Genera vectores de prueba
- `ComplexDriver`: Maneja transacciones
- `ComplexMonitor`: Monitorea DUT
- `ComplexScoreboard`: Verifica resultados
- `ComplexAgent`: Contiene driver, monitor, secuenciador
- `ComplexEnv`: Contiene agente y scoreboard
- `ComplexTestbenchTest`: Clase de prueba de nivel superior

### Módulos Design Under Test (DUT)

#### Esclavo AXI4-Lite (`module6/dut/protocols/axi4_lite_slave.v`)
- **Propósito**: Esclavo AXI4-Lite para verificación de protocolo
- **Usado en**: Ejemplos de verificación de protocolo
- **Características**: Implementación AXI4-Lite completa con los 5 canales, interfaz de memoria

## Ejercicios

1. **Entorno Multi-Agente**
   - Diseñar entorno
   - Implementar agentes
   - Coordinar agentes
   - **Ubicación**: Extiende `module6/examples/multi_agent/multi_agent_example.py`
   - **Pista**: Agrega más agentes y coordínalos con secuencias virtuales

2. **Verificación de Protocolo**
   - Elegir protocolo
   - Crear agente
   - Implementar verificador
   - **Ubicación**: Extiende `module6/examples/protocol/protocol_example.py`
   - **Pista**: Agrega más reglas de protocolo e implementa protocolo AXI4-Lite completo

3. **Arquitectura de Testbench**
   - Diseñar arquitectura
   - Implementar patrones
   - Organizar código
   - **Ubicación**: Extiende `module6/examples/architecture/architecture_example.py`
   - **Pista**: Agrega más capas e implementa librería de componentes reutilizables

4. **Depuración**
   - Agregar depuración
   - Analizar resultados
   - Corregir problemas
   - **Ubicación**: Agregar a ejemplos existentes
   - **Pista**: Agrega logging de transacciones y generación de formas de onda

5. **Análisis de Rendimiento**
   - Monitorear rendimiento
   - Analizar métricas
   - Optimizar
   - **Ubicación**: Crear nuevo ejemplo
   - **Pista**: Agrega componentes de monitoreo de rendimiento

## Evaluación

- [ ] Puedo diseñar entornos multi-agente
- [ ] Puedo implementar verificación de protocolo
- [ ] Entiendo los patrones de arquitectura
- [ ] Puedo depurar testbenches complejos
- [ ] Puedo analizar resultados de simulación
- [ ] Puedo coordinar múltiples canales
- [ ] Puedo monitorear rendimiento
- [ ] Puedo integrar componentes
- [ ] Puedo mantener testbenches
- [ ] Entiendo las mejores prácticas

## Próximos Pasos

Después de completar este módulo, continúa con [Módulo 7: Aplicaciones del Mundo Real](MODULE7.md) para aplicar UVM a escenarios de verificación del mundo real.

## Recursos Adicionales

- **Documentación de pyuvm**: https://pyuvm.readthedocs.io/
- **Guía de Usuario de UVM 1.2**: Accellera Systems Initiative
- **UVM Avanzado**: Ray Salemi
- **Especificación de Protocolo AXI**: Especificación ARM AMBA
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

**Problema: La coordinación multi-agente no funciona**
```bash
# Solución: Asegurar que la secuencia virtual tenga referencias a todos los secuenciadores
# Establecer referencias de secuenciador: virtual_seq.agent_seqrs = [agent.seqr for agent in env.agents]
# Usar cocotb.start_soon() para ejecución paralela
```

**Problema: El verificador de protocolo no detecta violaciones**
```bash
# Solución: Verificar que las reglas de protocolo estén implementadas correctamente
# Asegurar que el seguimiento de estado sea correcto
# Verificar que el verificador reciba transacciones del monitor
```

**Problema: El scoreboard multi-canal no recibe de todos los canales**
```bash
# Solución: Verificar las conexiones del puerto de análisis
# Asegurar: monitor.ap.connect(scoreboard.analysis_exports[channel_id])
# Verificar que el método write() maneje el parámetro channel_id
```

**Problema: Errores de implementación del protocolo AXI**
```bash
# Solución: Revisar la especificación AXI4-Lite
# Asegurar handshaking adecuado en todos los canales
# Verificar temporización y secuenciación de señales
```

### Obteniendo Ayuda

- Revisa los comentarios del código de ejemplo para explicaciones detalladas
- Consulta el `module6/README.md` para la estructura del directorio
- Ejecuta ejemplos individualmente para entender cada patrón complejo
- Estudia la coordinación multi-agente en `multi_agent_example.py`
- Revisa la implementación de protocolo en `protocol_example.py`
- Consulta la especificación del protocolo AXI para detalles del protocolo

### Resumen de Ejemplos y Pruebas

**Ejemplos (ejemplos estructurales de pyuvm en `module6/examples/`):**
1. **Ejemplo 6.1: Entorno Multi-Agente** (`multi_agent/`) - Coordinación de múltiples agentes
2. **Ejemplo 6.2: Verificación de Protocolo** (`protocol/`) - Implementación de protocolo AXI4-Lite
3. **Ejemplo 6.3: Verificador de Protocolo** (`protocol_checkers/`) - Verificación de cumplimiento de protocolo
4. **Ejemplo 6.4: Scoreboard Multi-Canal** (`scoreboards/`) - Scoreboarding multi-canal
5. **Ejemplo 6.5: Arquitectura de Testbench** (`architecture/`) - Patrones en capas y reutilizables

**Testbenches (pruebas ejecutables en `module6/tests/pyuvm_tests/`):**
1. **Prueba de Testbench Complejo** (`test_complex_testbench.py`) - Testbench complejo completo

**Módulos DUT (en `module6/dut/`):**
1. **Esclavo AXI4-Lite** (`protocols/axi4_lite_slave.v`) - Esclavo AXI4-Lite para verificación de protocolo

**Cobertura:**
- ✅ Diseño de entorno multi-agente
- ✅ Verificación de protocolo (AXI4-Lite)
- ✅ Verificación de cumplimiento de protocolo
- ✅ Scoreboarding multi-canal
- ✅ Patrones de arquitectura de testbench
- ✅ Integración de testbench complejo
