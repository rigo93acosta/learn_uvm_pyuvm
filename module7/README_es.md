# Módulo 7: Aplicaciones del Mundo Real

Este directorio contiene todos los ejemplos, ejercicios y casos de prueba para el Módulo 7, enfocado en aplicaciones de verificación del mundo real incluyendo verificación DMA, verificación de protocolos (UART, SPI, I2C), desarrollo de VIP y mejores prácticas.

## Estructura del Directorio

```
module7/
├── examples/              # Ejemplos de pyuvm para cada tema
│   ├── dma/              # Ejemplos de verificación DMA
│   │   └── dma_example.py
│   ├── protocols/        # Ejemplos de verificación de protocolos (UART, SPI, I2C)
│   │   ├── uart_example.py
│   │   ├── spi_example.py
│   │   └── i2c_example.py
│   ├── vip/              # Ejemplos de desarrollo VIP
│   │   └── vip_example.py
│   └── best_practices/   # Ejemplos de mejores prácticas
│       └── best_practices_example.py
├── dut/                   # Módulos Verilog Design Under Test
│   ├── dma/              # Controlador DMA
│   │   └── simple_dma.v
│   └── protocols/        # Módulos de protocolo
│       └── uart.v
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # Testbenches pyuvm
│       └── test_real_world.py
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

## Ejemplos del Mundo Real

### 1. Verificación DMA (`examples/dma/dma_example.py`)

Demuestra un entorno completo de verificación de controlador DMA:

**Conceptos Clave:**
- Transacciones de transferencia DMA
- Interfaz de registros DMA
- Monitoreo de transferencias DMA
- Verificación con scoreboard DMA
- Recolección de cobertura DMA
- Transferencias simples y scatter-gather

**Componentes DMA:**

1. **DMATransaction**
   - Transacción para transferencias DMA
   - Campos: `src_addr`, `dst_addr`, `length`, `channel`, `transfer_type`
   - Soporta tipos de transferencia SIMPLE y SCATTER_GATHER
   - Identificación de canal

2. **DMARegisterDriver**
   - Driver para la interfaz de registros DMA
   - Configura registros DMA (origen, destino, longitud)
   - Inicia transferencias DMA
   - Maneja transacciones de registros DMA

3. **DMAMonitor**
   - Monitor para transferencias DMA
   - Monitorea la finalización de transferencias DMA
   - Crea transacciones a partir de transferencias monitoreadas
   - Transmite a través del puerto de análisis

4. **DMAScoreboard**
   - Scoreboard para verificación DMA
   - Rastrea transferencias esperadas y reales
   - Coincide transferencias por origen, destino y longitud
   - Reporta discrepancias de transferencias

5. **DMACoverage**
   - Modelo de cobertura para verificación DMA
   - Rastrea canales utilizados
   - Rastrea tipos de transferencia
   - Rastrea rangos de longitud de transferencia (pequeño, mediano, grande)

**Tipos de Transferencia DMA:**

**Transferencia Simple:**
- Un solo origen a un solo destino
- Transferencia de longitud fija
- Operación de un solo canal

**Transferencia Scatter-Gather:**
- Múltiples pares origen/destino
- Transferencias de longitud variable
- Operación de múltiples canales

**Flujo de Verificación DMA:**
```python
# 1. Agregar transferencia esperada
txn = DMATransaction()
txn.src_addr = 0x1000
txn.dst_addr = 0x2000
txn.length = 256
self.env.scoreboard.add_expected(txn)

# 2. Iniciar secuencia DMA
seq = DMASequence.create("seq")
await seq.start(self.env.agent.seqr)

# 3. El monitor valida la transferencia
# 4. El scoreboard compara esperado vs real
```

**Ejecutar el ejemplo:**

```bash
# Mediante el script del módulo
./scripts/module7.sh --dma

# O directamente desde el directorio del ejemplo
cd module7/examples/dma
make SIM=verilator TEST=dma_example
```

**Salida Esperada:**
- Configuración de transferencia DMA
- Ejecución de transferencia DMA
- Monitoreo de transferencia DMA
- Verificación con scoreboard DMA
- Recolección de cobertura DMA

### 2. Verificación de Protocolo UART (`examples/protocols/uart_example.py`)

Demuestra un agente de verificación de protocolo UART:

**Conceptos Clave:**
- Manejo de transacciones UART
- Protocolo de transmisión UART
- Monitoreo de recepción UART
- Configuración de baud rate
- Manejo de paridad y bits de parada

**Componentes UART:**

1. **UARTTransaction**
   - Transacción para operaciones UART
   - Campos: `data`, `baud_rate`, `parity`, `stop_bits`
   - Soporta diferentes baud rates
   - Soporta tipos de paridad: NONE, EVEN, ODD

2. **UARTDriver**
   - Implementa el protocolo de transmisión UART
   - Transmite: Bit de inicio → Bits de datos → Paridad → Bit(s) de parada
   - Maneja la temporización del baud rate
   - Genera la trama UART

3. **UARTMonitor**
   - Monitorea la recepción UART
   - Detecta el bit de inicio
   - Muestrea los bits de datos
   - Detecta el(los) bit(s) de parada
   - Crea transacciones a partir de los datos recibidos

4. **UARTSequence**
   - Genera secuencias de prueba UART
   - Crea patrones de datos de prueba
   - Configura baud rate y paridad
   - Prueba varios valores de datos

**Protocolo UART:**

**Estructura de la Trama:**
- Bit de inicio (0) → 8 bits de datos → Bit de paridad (opcional) → Bit(s) de parada (1)

**Transmisión:**
- Línea inactiva en alto (1)
- El bit de inicio pone la línea en bajo (0)
- Los bits de datos se transmiten LSB primero
- El bit de parada devuelve la línea a alto (1)

**Ejecutar el ejemplo:**

```bash
./scripts/module7.sh --uart
# o
cd module7/examples/protocols
make SIM=verilator TEST=uart_example
```

**Salida Esperada:**
- Transmisión de trama UART
- Recepción de trama UART
- Manejo de baud rate
- Verificación de paridad

### 3. Verificación de Protocolo SPI (`examples/protocols/spi_example.py`)

Demuestra la verificación de protocolo SPI con coordinación maestro-esclavo:

**Conceptos Clave:**
- Manejo de transacciones SPI
- Coordinación maestro-esclavo
- Configuración de modo SPI
- Manejo de chip select
- Sincronización de reloj y datos

**Componentes SPI:**

1. **SPITransaction**
   - Transacción para operaciones SPI
   - Campos: `data`, `mode`, `cs`, `is_master`
   - Soporta modos SPI 0-3
   - Identificación de chip select
   - Rol maestro/esclavo

2. **SPIDriver**
   - Implementa el protocolo de transmisión SPI
   - Transmite: CS bajo → Reloj con datos → CS alto
   - Maneja la temporización del modo SPI
   - Transmite MSB o LSB primero (según el modo)

3. **SPIMonitor**
   - Monitorea la recepción SPI
   - Detecta la activación de CS
   - Muestrea datos en los flancos del reloj
   - Crea transacciones a partir de los datos recibidos

4. **SPIEnv**
   - Entorno con agentes maestro y esclavo
   - Coordina la comunicación maestro-esclavo
   - Demuestra verificación de protocolo multi-agente

**Protocolo SPI:**

**Líneas de Señal:**
- `sclk` - Reloj serie
- `mosi` - Master Out Slave In
- `miso` - Master In Slave Out
- `cs` - Chip select (activo en bajo)

**Transmisión:**
- CS activado (bajo) → Reloj con datos → CS desactivado (alto)
- Datos transmitidos sincrónicamente con el reloj
- El modo SPI determina la polaridad y fase del reloj

**Ejecutar el ejemplo:**

```bash
./scripts/module7.sh --spi
# o
cd module7/examples/protocols
make SIM=verilator TEST=spi_example
```

**Salida Esperada:**
- Transmisión maestro SPI
- Recepción esclavo SPI
- Coordinación maestro-esclavo
- Manejo de modo SPI

### 4. Verificación de Protocolo I2C (`examples/protocols/i2c_example.py`)

Demuestra la verificación de protocolo I2C con soporte multi-maestro:

**Conceptos Clave:**
- Manejo de transacciones I2C
- Soporte multi-maestro
- Manejo de condiciones START/STOP
- Transmisión de dirección y datos
- Manejo de ACK/NACK

**Componentes I2C:**

1. **I2CTransaction**
   - Transacción para operaciones I2C
   - Campos: `address`, `data[]`, `is_write`, `is_start`, `is_stop`
   - Soporta direccionamiento de 7 y 10 bits
   - Soporta operaciones de lectura y escritura
   - Banderas de condición START y STOP

2. **I2CDriver**
   - Implementa el protocolo de transmisión I2C
   - Transmite: START → Dirección → R/W → ACK → Datos → ACK → STOP
   - Maneja condiciones START y STOP
   - Transmite bits de dirección y datos
   - Maneja respuestas ACK/NACK

3. **I2CMonitor**
   - Monitorea la recepción I2C
   - Detecta condición START
   - Muestrea bits de dirección y datos
   - Detecta condición STOP
   - Crea transacciones a partir de las tramas recibidas

4. **I2CEnv**
   - Entorno con múltiples maestros y esclavo
   - Soporta escenarios multi-maestro
   - Demuestra arbitraje I2C (conceptual)

**Protocolo I2C:**

**Líneas de Señal:**
- `sda` - Datos serie (bidireccional, drenador abierto)
- `scl` - Reloj serie (bidireccional, drenador abierto)

**Estructura de la Trama:**
- Condición START → Dirección de 7 bits → bit R/W → ACK → Bytes de datos → ACK → Condición STOP

**Ejecutar el ejemplo:**

```bash
./scripts/module7.sh --i2c
# o
cd module7/examples/protocols
make SIM=verilator TEST=i2c_example
```

**Salida Esperada:**
- Condiciones START/STOP I2C
- Transmisión de dirección I2C
- Transmisión de datos I2C
- Soporte multi-maestro

### 5. Desarrollo de VIP (`examples/vip/vip_example.py`)

Demuestra la creación de IP de verificación reutilizable:

**Conceptos Clave:**
- Estructura y componentes VIP
- Configuración VIP (activo/pasivo)
- Patrones de reutilización VIP
- Verificación de protocolo VIP
- Recolección de cobertura VIP

**Componentes VIP:**

1. **VIPAgent**
   - Estructura completa de agente VIP
   - Contiene: driver, monitor, secuenciador, verificador, cobertura
   - Soporta modos activo y pasivo
   - Configurable mediante ConfigDB
   - Reutilizable entre proyectos

2. **VIPDriver**
   - Driver para el protocolo VIP
   - Maneja transacciones hacia el DUT
   - Implementación de protocolo configurable

3. **VIPMonitor**
   - Monitor para el protocolo VIP
   - Muestrea señales del DUT
   - Crea transacciones a partir de datos monitoreados
   - Transmite a través del puerto de análisis

4. **VIPChecker**
   - Verificador de protocolo para VIP
   - Valida el cumplimiento del protocolo
   - Reporta violaciones de protocolo
   - Extiende `uvm_subscriber`

5. **VIPCoverage**
   - Modelo de cobertura para VIP
   - Recolecta cobertura funcional
   - Rastrea cobertura de transacciones
   - Reporta estadísticas de cobertura

**Configuración VIP:**

**Modo Activo:**
- Crea driver y secuenciador
- Puede generar y manejar transacciones
- Adecuado para verificación activa

**Modo Pasivo:**
- Sin driver ni secuenciador
- Solo monitor, verificador y cobertura
- Adecuado para monitoreo y verificación

**Reutilización VIP:**
```python
# VIP puede usarse en múltiples entornos
class VIPEnv(uvm_env):
    def build_phase(self):
        # Crear VIP con configuración
        self.vip = VIPAgent.create("vip", self)
        
        # Configurar VIP (activo/pasivo)
        ConfigDB().set(None, "", "env.vip.active", True)
```

**Ejecutar el ejemplo:**

```bash
./scripts/module7.sh --vip
# o
cd module7/examples/vip
make SIM=verilator TEST=vip_example
```

**Salida Esperada:**
- Creación de agente VIP
- Configuración VIP (activo/pasivo)
- Verificación de protocolo VIP
- Recolección de cobertura VIP

**Beneficios VIP:**
- Reutilizable entre proyectos
- Configurable para diferentes casos de uso
- Solución de verificación autocontenida
- Estructura estándar de la industria

### 6. Mejores Prácticas (`examples/best_practices/best_practices_example.py`)

Demuestra organización de código, documentación y mejores prácticas:

**Conceptos Clave:**
- Organización clara del código
- Documentación exhaustiva
- Reutilización de componentes
- Manejo de errores
- Registro y reporte

**Mejores Prácticas:**

1. **Mejores Prácticas de Transacciones:**
   - Nombres de clase claros
   - Docstrings exhaustivos
   - Type hints (en código real)
   - Nombres de campo claros
   - Método `__str__` para depuración

2. **Mejores Prácticas de Componentes:**
   - Nombres de componente claros
   - Docstrings exhaustivos
   - Métodos organizados
   - Registro claro
   - Manejo de errores

3. **Mejores Prácticas de Reutilización:**
   - Parameterización
   - Soporte de configuración
   - Interfaces claras
   - Documentación
   - Ejemplo de uso

4. **Mejores Prácticas de Organización:**
   - Estructura clara
   - Agrupación lógica
   - Nomenclatura clara
   - Documentación

**Ejemplo de Mejores Prácticas:**
```python
class BestPracticesComponent(uvm_component):
    """
    Component demonstrating best practices.
    
    Best Practices:
    - Clear component name
    - Comprehensive docstring
    - Organized methods
    - Clear logging
    - Error handling
    """
    
    def build_phase(self):
        """
        Build phase with clear documentation.
        
        Best Practices:
        - Document what is built
        - Use clear variable names
        - Organize code logically
        """
        self.logger.info(f"[{self.get_name()}] Building component")
```

**Ejecutar el ejemplo:**

```bash
./scripts/module7.sh --best-practices
# o
cd module7/examples/best_practices
make SIM=verilator TEST=best_practices_example
```

**Salida Esperada:**
- Estructura de código bien organizada
- Documentación clara
- Componentes reutilizables
- Registro y reporte claros

**Beneficios de las Mejores Prácticas:**
- Mantenibilidad mejorada
- Mejor reutilización de código
- Depuración más fácil
- Documentación más clara

## Design Under Test (DUT)

### Controlador DMA Simple (`dut/dma/simple_dma.v`)

Un controlador DMA simple para verificación.

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

**Características:**
- Implementación DMA simplificada
- Operación síncrona con reset asíncrono
- Máquina de estados de transferencia básica
- Adecuado para verificación DMA

**Protocolo:**
- Configuración basada en registros
- Transferencias disparadas por inicio
- Indicación de finalización
- Operación basada en canales

### Transmisor/Receptor UART (`dut/protocols/uart.v`)

Un UART simple para verificación de protocolo.

**Interfaz del Módulo:**
```verilog
module uart (
    input  wire       clk,       // Señal de reloj
    input  wire       rst_n,     // Reset activo en bajo
    output reg        tx,        // Línea de datos de transmisión
    input  wire       rx,        // Línea de datos de recepción
    input  wire [7:0] tx_data,   // Dato a transmitir (8-bit)
    input  wire       tx_start,  // Iniciar transmisión
    output reg        tx_busy,   // Transmisión en curso
    output reg  [7:0] rx_data,   // Dato recibido (8-bit)
    output reg        rx_ready   // Dato recibido listo
);
```

**Funcionalidad:**
- Comunicación UART full-duplex
- Máquina de estados del transmisor: IDLE → START → DATA → STOP
- Máquina de estados del receptor: IDLE → START → DATA → STOP
- Transmisión de datos de 8 bits
- Manejo de bits de inicio y parada

**Características:**
- Implementación UART simplificada
- Operación síncrona con reset asíncrono
- Transmisor y receptor separados
- Adecuado para verificación de protocolo UART

**Protocolo:**
- Bit de inicio (0) → 8 bits de datos → Bit de parada (1)
- Línea inactiva en alto (1)
- Datos transmitidos LSB primero

## Testbenches

### Pruebas pyuvm (`tests/pyuvm_tests/`)

#### Prueba de Aplicación del Mundo Real (`test_real_world.py`)

Testbench UVM completo que demuestra escenarios de verificación del mundo real:

**Componentes UVM:**

1. **Transaction (`RealWorldTransaction`)**
   - Contiene campos `data` y `address`
   - Utilizado para pruebas del mundo real

2. **Sequence (`RealWorldSequence`)**
   - Genera transacciones de prueba
   - Crea vectores de prueba exhaustivos

3. **Driver (`RealWorldDriver`)**
   - Recibe transacciones del secuenciador
   - Maneja las entradas del DUT

4. **Monitor (`RealWorldMonitor`)**
   - Muestrea las salidas del DUT
   - Crea transacciones a partir de los datos muestreados
   - Transmite a través del puerto de análisis

5. **Scoreboard (`RealWorldScoreboard`)**
   - Extiende `uvm_subscriber`
   - Recibe transacciones del monitor
   - Rastrea transacciones recibidas

6. **Agent (`RealWorldAgent`)**
   - Contiene driver, monitor y secuenciador
   - Conecta componentes

7. **Environment (`RealWorldEnv`)**
   - Contiene agente y scoreboard
   - Conecta el monitor con el scoreboard

8. **Test (`RealWorldTest`)**
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
./scripts/module7.sh --pyuvm-tests

# Directamente desde el directorio de pruebas
cd module7/tests/pyuvm_tests
make SIM=verilator TEST=test_real_world
```

**Resultados Esperados:**
- 1 caso de prueba exitoso
- Todos los componentes creados y conectados
- Ejecución de secuencia demostrada
- Seguimiento de scoreboard demostrado
- Conceptos de verificación del mundo real integrados

## Ejecutar Ejemplos y Pruebas

### Usando el Script del Módulo

El script `module7.sh` proporciona una forma conveniente de ejecutar todos los ejemplos y pruebas:

```bash
# Ejecutar todo (todos los ejemplos + todas las pruebas)
./scripts/module7.sh

# Ejecutar solo ejemplos
./scripts/module7.sh --all-examples

# Ejecutar solo pruebas
./scripts/module7.sh --pyuvm-tests

# Ejecutar ejemplos específicos
./scripts/module7.sh --dma
./scripts/module7.sh --uart
./scripts/module7.sh --spi
./scripts/module7.sh --i2c
./scripts/module7.sh --vip
./scripts/module7.sh --best-practices

# Combinar opciones
./scripts/module7.sh --dma --uart --pyuvm-tests
```

### Ejecutar Ejemplos Individuales

#### Ejecución Directa desde el Directorio del Ejemplo

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio del ejemplo
cd module7/examples/dma

# Ejecutar ejemplo
make SIM=verilator TEST=dma_example

# Limpiar artefactos de compilación
make clean
```

#### Ejecutar Todos los Ejemplos Secuencialmente

```bash
cd module7/examples

# DMA
cd dma && make SIM=verilator TEST=dma_example && cd ..

# UART
cd protocols && make SIM=verilator TEST=uart_example && cd ..

# SPI
cd protocols && make SIM=verilator TEST=spi_example && cd ..

# I2C
cd protocols && make SIM=verilator TEST=i2c_example && cd ..

# VIP
cd vip && make SIM=verilator TEST=vip_example && cd ..

# Best practices
cd best_practices && make SIM=verilator TEST=best_practices_example && cd ..
```

### Ejecutar Pruebas pyuvm

```bash
# Activar entorno virtual
source .venv/bin/activate

# Cambiar al directorio de pruebas
cd module7/tests/pyuvm_tests

# Ejecutar prueba
make SIM=verilator TEST=test_real_world

# Limpiar artefactos de compilación
make clean
```

## Resultados de las Pruebas

Cuando las pruebas se completen exitosamente, deberías ver una salida similar a:

### Salida de Ejemplo de Prueba

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** dma_example.test_dma                           PASS         200.00           0.00     123456.78  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 200.00           0.00      12345.67  **
```

### Conteo Esperado de Pruebas

- **Ejemplo DMA**: 1 prueba
- **Ejemplo UART**: 1 prueba
- **Ejemplo SPI**: 1 prueba
- **Ejemplo I2C**: 1 prueba
- **Ejemplo VIP**: 1 prueba
- **Ejemplo de mejores prácticas**: 1 prueba
- **Prueba de aplicación del mundo real**: 1 prueba
- **Total**: 7 pruebas en todos los ejemplos y testbenches

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

#### 3. Problemas de Transferencia DMA

**Error:** Las transferencias DMA no se completan

**Solución:**
- Verifica la configuración de los registros DMA
- Comprueba la activación de la señal de inicio DMA
- Verifica el monitoreo de la señal de finalización DMA
- Asegúrate de que la longitud de transferencia sea válida
- Comprueba la selección de canal

#### 4. Problemas de Protocolo UART

**Error:** Las tramas UART no se reciben correctamente

**Solución:**
- Verifica la configuración del baud rate
- Comprueba la temporización de los bits de inicio/parada
- Verifica la configuración de paridad
- Asegúrate de la sincronización adecuada de la trama
- Comprueba el muestreo de señales

#### 5. Problemas de Protocolo SPI

**Error:** La comunicación maestro-esclavo SPI falla

**Solución:**
- Verifica la configuración del modo SPI
- Comprueba la temporización del chip select
- Verifica la sincronización de reloj y datos
- Asegúrate de la coordinación adecuada maestro-esclavo
- Comprueba las conexiones de señales

#### 6. Problemas de Protocolo I2C

**Error:** Las transacciones I2C fallan

**Solución:**
- Verifica la temporización de las condiciones START/STOP
- Comprueba el formato de dirección (7 bits vs 10 bits)
- Verifica el manejo de ACK/NACK
- Asegúrate de la coordinación multi-maestro adecuada
- Comprueba las conexiones de señales (drenador abierto)

#### 7. Problemas de Configuración VIP

**Error:** El VIP no funciona en modo pasivo

**Solución:**
- Verifica la configuración VIP en ConfigDB
- Comprueba la configuración del modo activo/pasivo
- Asegúrate de que el monitor siempre se cree
- Verifica las conexiones de los componentes VIP
- Comprueba la validación de la configuración VIP

### Consejos de Depuración

1. **Verificar Transferencias DMA:**
   ```python
   # Verify DMA configuration
   self.logger.info(f"DMA config: src=0x{src_addr:08X}, dst=0x{src_addr:08X}, len={length}")
   ```

2. **Monitorear Transacciones de Protocolo:**
   ```python
   # Add logging in protocol drivers
   self.logger.info(f"Protocol transaction: {txn}")
   ```

3. **Verificar Configuración VIP:**
   ```python
   # Verify VIP mode
   self.logger.info(f"VIP mode: active={self.active}")
   ```

4. **Inspeccionar Cobertura:**
   ```python
   # Check coverage statistics
   self.logger.info(f"Coverage: {self.coverage_data}")
   ```

## Temas Cubiertos

1. **Verificación DMA** - Verificación completa de controlador DMA, tipos de transferencia, canales
2. **Verificación de Protocolo** - Verificación de protocolos UART, SPI, I2C, coordinación maestro-esclavo
3. **Mejores Prácticas** - Organización de código, reutilización, documentación
4. **Desarrollo VIP** - Creación de IP de verificación reutilizable, modos activo/pasivo
5. **Verificación a Nivel de Sistema** - Patrones de verificación de sistema y SoC
6. **Depuración Avanzada** - Técnicas complejas de depuración, análisis de protocolo
7. **Planificación de Pruebas** - Estrategia y planificación de verificación
8. **Patrones de la Industria** - Patrones de verificación comunes, estructuras VIP
9. **Optimización de Rendimiento** - Optimización de testbench, protocolos eficientes
10. **Cierre de Cobertura** - Estrategias y cierre de cobertura, cobertura funcional

## Próximos Pasos

Después de completar el Módulo 7, continúa con:

- **Módulo 8**: Utilidades Avanzadas - CLP, comparadores, pools, colas, grabadores

## Recursos Adicionales

- [Documentación de pyuvm](https://pyuvm.readthedocs.io/)
- [Guía de Usuario de UVM](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_1.2.pdf)
- [Diseño de Controlador DMA](https://en.wikipedia.org/wiki/Direct_memory_access)
- [Protocolo UART](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter)
- [Protocolo SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)
- [Protocolo I2C](https://en.wikipedia.org/wiki/I²C)
- [Documentación de cocotb](https://docs.cocotb.org/)
- [Documentación de Verilator](https://verilator.org/)

## Descripción de Archivos

### Ejemplos

| Archivo | Descripción | Pruebas |
|---------|-------------|---------|
| `dma_example.py` | Verificación de controlador DMA | 1 función de prueba |
| `uart_example.py` | Verificación de protocolo UART | 1 función de prueba |
| `spi_example.py` | Verificación de protocolo SPI | 1 función de prueba |
| `i2c_example.py` | Verificación de protocolo I2C | 1 función de prueba |
| `vip_example.py` | Desarrollo VIP | 1 función de prueba |
| `best_practices_example.py` | Demostración de mejores prácticas | 1 función de prueba |

### Módulos DUT

| Archivo | Descripción | Puertos |
|---------|-------------|---------|
| `simple_dma.v` | Controlador DMA simple | `clk`, `rst_n`, `dma_start`, `dma_done`, `dma_src_addr[31:0]`, `dma_dst_addr[31:0]`, `dma_length[15:0]`, `dma_channel[2:0]` |
| `uart.v` | Transmisor/receptor UART | `clk`, `rst_n`, `tx`, `rx`, `tx_data[7:0]`, `tx_start`, `tx_busy`, `rx_data[7:0]`, `rx_ready` |

### Testbenches

| Archivo | Framework | Descripción | Pruebas |
|---------|-----------|-------------|---------|
| `test_real_world.py` | pyuvm | Prueba de aplicación del mundo real | 1 prueba UVM |

---

Para preguntas o problemas, consulta el README principal del proyecto o revisa los registros de prueba para mensajes de error detallados.
