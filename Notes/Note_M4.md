# Componentes UVM

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

## Interfaz


| Port name | Direction |	Type	     | 
| ---       |   ---     |   ---          |
| clk	    | input     | 	wire         |  
| rst_n	    | input	    |   wire         |	
| valid	    | input	    |   wire         |
| ready	    | output    |		         |
| data      | input     |	wire [7:0]	 |
| address   | input     |	wire [15:0]	 |
| result    | output    |	[7:0]	     |

## Transacción

En esta parte no hay mucho que aportar es la manera en que empaquetamos las transacciones; es decir, se establece que colocamos o leemos de cada pin del DUT. Es como una encapsulacion de la informacion que procesa el DUT.

## Driver

**Flujo del Driver:**
1. `build_phase()` - Crea `seq_item_port`, ya viene creado por default
2. `connect_phase()` - Conecta al sequencer
3. `run_phase()` - Bucle principal del driver:
   - `get_next_item()` - Obtiene la transacción del sequencer
   - `drive_transaction()` - Conduce señales hacia el DUT -> Implementar
   - `item_done()` - Señala la finalización

**Conceptos clave:**
- **`uvm_driver`**: Clase base para todos los drivers
- **`seq_item_port`**: Puerto para recibir transacciones desde el sequencer
- **`get_next_item()`**: Obtener la siguiente transacción del sequencer
- **`item_done()`**: Señalar la finalización de la transacción al sequencer
- **`run_phase()`**: Bucle principal del driver
- **Implementación del protocolo**: Conducir señales según la temporización del protocolo

## Monitors

Topico fundamental los puertos de analisis y la creacion de transacciones a partir de las señales del DUT.

**Flujo del Monitor:**
1. `build_phase()` - Crea `analysis_port`
2. `run_phase()` - Bucle principal del monitor:
   - `sample_signals()` - Muestra señales del DUT
   - Crea una transacción a partir de los datos muestreados
   - `ap.write()` - Difunde mediante analysis port

Muestrear los datos del DUT puede ser complejo dependiendo del protocolo, es importante entender la temporización y las condiciones de muestreo. Para ganar en readabilidad, es recomendable encapsular la lógica de muestreo en funciones auxiliares; en el caso del codigo que vemos se encapsula en funciones `sample_signals()` y `sample_protocol_signals()`.

> En el `run_phase`, antes de entrar al bucle infinito while True, asegúrate de esperar a que el reset del sistema se desactive (ej. `await FallingEdge(self.dut.rst_n)`).

## Sequencer 

Lo importante es enteder la estructura general

**Flujo de Secuencia:**
1. `body()` - Método de ejecución de la secuencia
2. `start_item(txn)` - Solicita una transacción al sequencer
3. `finish_item(txn)` - Envía la transacción al driver
4. La secuencia termina cuando `body()` retorna, de ser necesario, algún objeto. 

> `uvm_sequence_item` / `uvm_sequence`: Son objetos dinámicos. Se crean, se ejecutan y se destruyen sobre la marcha. Como no forman parte de la estructura jerárquica fija del testbench, `pyuvm` no les asigna automáticamente un logger en su inicialización de la misma manera que a un componente.

```Python
if not hasattr(self, "logger"):
   import logging
   self.logger = logging.getLogger(f"{self.__class__.__name__}.{self.get_name()}")
   self.logger.setLevel(logging.INFO)
```

> Nota:
> A futuro, los sequences puede ser complejos