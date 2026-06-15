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
> A futuro, los sequences puede ser complejos pueden tener agentes que gestionen que tipos de sequencias se van a enviar al dut.

## TLM (Transaction-Level Modeling)

En pyuvm, las clases `uvm_put_export`, `uvm_get_export`, etc., esperan recibir como segundo argumento (parent) un objeto que implemente los métodos exactamente como funciones normales (def), o bien que se herede directamente de la clase export. Con esto, pyuvm confía plenamente en el componente y te permite ejecutar tus tareas asíncronas (async def put) sin que salte el sistema de seguridad de tipos.

### El Núcleo de la Filosofía TLM: Iniciativa vs. Dirección del Dato

El error conceptual más común al aprender TLM es confundir el camino físico que recorre un paquete de datos con el componente de software que inicia la transferencia. TLM resuelve esto dividiendo el problema en dos ejes independientes: la **Intención** (el verbo que define quién tiene el control del tiempo) y el **Mapeo de Software** (quién inicia la llamada y quién proporciona el código).

Independientemente de la interfaz utilizada, existe una regla física inmutable en los tres modelos principales: **los datos siempre viajan desde el componente que actúa como Productor hacia el componente que actúa como Consumidor**. Lo que cambia de manera radical es cuál de los dos extremos es el "dueño" del hilo de ejecución en la simulación.

### La Simplificación de la Arquitectura en `pyuvm`

A diferencia del estándar tradicional de UVM en SystemVerilog, donde los puertos, exports e implementations (`imp`) son entidades abstractas completamente desconectadas de los componentes jerárquicos, `pyuvm` simplifica la estructura eliminando los puertos `imp` mediante el uso estratégico de la herencia de Python.

En `pyuvm`, las clases base de llegada (como `uvm_put_export`, `uvm_get_export` o `uvm_transport_export`) **heredan directamente de `uvm_component**`. Esto otorga una doble identidad a los receptores: siguen integrándose de forma nativa en el árbol estructural del testbench, participan en las fases estándar (como `build_phase` o `connect_phase`) y poseen herramientas de reporte de errores (`self.logger`), pero simultáneamente **se convierten en el puerto de destino físico**.

Debido a esta arquitectura, el componente receptor no necesita instanciar sub-puertos internos; simplemente sobreescribe directamente en su propio cuerpo los métodos requeridos por el protocolo.

### Desglose de las Tres Interfaces Principales

#### 1. El Modelo Put: Productor Activo, Consumidor Pasivo

En este escenario, el control del tiempo y la iniciativa de la simulación residen en el Productor. Este componente se define como un `uvm_component` genérico y aloja internamente una instancia de salida llamada `uvm_put_port`. Al estar activo, ejecuta un bucle en su `run_phase` y decide de manera autónoma cuándo generar y "empujar" un paquete.

Por otro lado, el Consumidor adopta un rol completamente reactivo. Hereda directamente de `uvm_put_export`, lo que lo obliga a implementar en su estructura los métodos `put()`, `try_put()` y `can_put()`. El Consumidor no controla cuándo le llega la información; simplemente permanece a la espera, y cuando el Productor invoca de manera asíncrona un `await puerto.put()`, el framework de `pyuvm` redirige la ejecución para activar instantáneamente el código escrito en el Consumidor.

#### 2. El Modelo Get: Consumidor Activo, Productor Pasivo

Este modelo invierte por completo la dinámica del control temporal. Aquí, el Consumidor es el actor proactivo encargado de gobernar la `run_phase` y gestionar las objeciones del test. Al extender de `uvm_component`, aloja un `uvm_get_port` que utiliza para "estirar la mano" y solicitar transacciones bajo su propio criterio de tiempos mediante la instrucción `txn = await puerto.get()`.

En el otro extremo, el Productor se transforma en un almacén pasivo o un servidor de datos reactivo. Hereda de `uvm_get_export` y carece por completo de una `run_phase` propia. En su lugar, prepara las transacciones en memoria durante las fases de configuración y se queda "dormido". Solo se despierta delta-instantes cuando el Consumidor jala del cable de comunicación, ejecutando de forma remota las funciones `get()`, `try_get()` o `can_get()` para servir el paquete solicitado y volver a quedar en reposo.

#### 3. El Modelo Transport: Petición y Respuesta en una Operación Atómica

Cuando el flujo de verificación exige un intercambio de ida y vuelta inmediato (por ejemplo, al modelar transacciones de lectura/escritura en un bus de microcontrolador), los modelos unidireccionales individuales se quedan cortos. La interfaz Transport unifica el comportamiento de un `Put` y un `Get` en una única llamada de software atómica.

El componente maestro (activo) realiza una llamada enviando un objeto de petición (`request`) y detiene su ejecución en un punto de bloqueo esperando una respuesta (`response`). El componente esclavo hereda de `uvm_transport_export` (asumiendo el rol de puerto destino) e implementa el método `transport()`. Este recibe la pregunta, interactúa con el modelo o el hardware si es necesario, y retorna la respuesta. La gran ventaja es que la ida y la vuelta ocurren en el mismo hilo de ejecución, eliminando la necesidad de coordinar dos canales independientes.


### El Desacoplamiento Perfecto: `uvm_tlm_fifo`

A pesar de la elegancia de las conexiones directas "boca a boca", estas obligan a que un extremo sea estrictamente pasivo (reactivo) frente al otro. Para lograr que tanto el Productor como el Consumidor mantengan vidas independientes con bucles concurrentes activos en sus respectivas fases de ejecución, se introduce la FIFO TLM (`uvm_tlm_fifo`) como un elemento intermediario.

Al implementar una FIFO en el entorno, se rompe la conexión directa y se aplican las reglas de coincidencia de interfaces en ambos lados de manera independiente:

En el lado izquierdo, el Productor mantiene un `uvm_put_port` activo y se conecta al `put_export` de la FIFO. El productor "empuja" datos cuando su lógica lo dicta. Si la FIFO se llena, la corrutina asíncrona de su puerto se bloquea automáticamente mediante `await`, pausando al productor sin congelar el resto del entorno.

En el lado derecho, el Consumidor mantiene un `uvm_get_port` activo y se conecta al `get_export` de la misma FIFO. El consumidor "extrae" datos al ritmo que sus unidades de procesamiento lo demanden. Si la FIFO se queda vacía, su instrucción `await` suspende el hilo del consumidor hasta que el productor inyecte un nuevo elemento.

La FIFO actúa como un amortiguador y un sincronizador implícito de eventos. Logra que ambos actores interactúen de manera descentralizada y asíncrona, eliminando la necesidad de banderas lógicas globales o eventos manuales de sincronización en `cocotb`.