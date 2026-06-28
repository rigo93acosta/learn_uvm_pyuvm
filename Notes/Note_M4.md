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


| Port name | Direction |	Type	      | 
| ---       |   ---     |   ---        |
| clk	      | input     | 	wire        |  
| rst_n	   | input	   |   wire       |	
| valid	   | input	   |   wire       |
| ready	   | output    |		         |
| data      | input     |	wire [7:0]	|
| address   | input     |	wire [15:0]	|
| result    | output    |	[7:0]	      |

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


## Scoreboard

Precaución con esta línea:
```
self.env.scoreboard = ReferenceModelScoreboard.create("ref_scoreboard", self)
```
Al intentar asignar el scoreboard directamente desde el `Test`, el `Environment (env)` aún no ha ejecutado su propia fase de construcción. Aunque se forzara la creación en ese instante, cuando PyUVM pase automáticamente a construir el Environment, la línea interna `self.scoreboard = SimpleScoreboard.create(...)` se terminaría ejecutando igual, sobrescribiendo y destruyendo cualquier objeto que el Test hubiera intentado asignar a la fuerza.

El método set_type_override_by_type funciona porque no crea ningún objeto de inmediato, sino que registra una regla de sustitución:

   - El Test le avisa al Factory: "Si alguien te pide un `SimpleScoreboard`, entrégale un `ReferenceModelScoreboard`".

   - Cuando el Environment ejecuta su fase de construcción más tarde y llama a `SimpleScoreboard.create()`, el Factory intercepta la solicitud y genera el componente modificado de forma automática, respetando el flujo nativo de las fases de UVM.

Soluciones para prescindir del Factory y declarar el tipo de scoreboard de forma explícita al construir el Environment, existen dos alternativas sencillas:

   - Configuración por Inicialización (Vía Argumentos): Consiste en modificar el constructor `__init__` de tu `ScoreboardEnv` para que acepte un parámetro (por ejemplo, `scoreboard_cls=SimpleScoreboard`). Al instanciar el entorno en la build_phase del Test, se le pasa la clase `ReferenceModelScoreboard` como argumento. De esta manera, el Environment guarda la referencia y utiliza esa variable de clase al ejecutar su método `.create()`.

   - Configuración Dinámica (Vía `ConfigDB`): Consiste en utilizar la base de datos de configuración de UVM. En la `build_phase` del Test, guardas la clase del scoreboard deseado usando `uvm_config_db().set()`. Posteriormente, dentro de la build_phase del Environment, recuperas esa clase con `uvm_config_db().get()`. Si la base de datos encuentra un tipo específico lo utiliza para la instanciación; de lo contrario, recurre al scoreboard base por defecto.

En la verificación funcional con UVM y PyUVM, cuando los diseños de hardware (DUT) se vuelven grandes o procesan datos de forma compleja, un scoreboard simple que solo compara una entrada con una salida en orden estricto deja de ser útil.

### 1. Scoreboards Multicanal

En sistemas reales, los componentes suelen tener múltiples interfaces de entrada y salida (por ejemplo, un switch de red con 4 puertos de entrada y 4 de salida, o un bloque DMA con varios canales de datos).

- **Qué hace:** Un scoreboard avanzado implementa múltiples puertos de análisis (`uvm_analysis_imp`) para recibir transacciones de diferentes monitores simultáneamente.
- **Cómo se gestiona:** Para evitar que los datos de un canal se mezclen con los de otro, se utilizan macros especiales o estructuras de datos indexadas (como diccionarios o colas independientes por cada canal/puerto) para almacenar y clasificar el tráfico de forma ordenada antes de comparar.

### 2. Emparejamiento Basado en Tiempo (Time-based Matching)

A veces, el orden en el que salen las transacciones del DUT no es estrictamente el mismo en el que entraron (procesamiento desordenado o *Out-of-Order*), o el hardware tiene latencias variables.

- **Qué hace:** En lugar de usar una cola simple tipo FIFO (donde el primer dato que entra debe ser el primero que sale), el scoreboard busca coincidencias utilizando marcas de tiempo (*timestamps*) o ventanas de tiempo tolerables.
- **Cómo funciona:** Cuando llega un dato real del monitor de salida, el scoreboard calcula si llegó dentro del rango de ciclos de reloj o tiempo de simulación simulado esperado (`cocotb.triggers.Timer` o marcas de tiempo del sistema) respecto a cuando se generó el estímulo. Si llega muy temprano o muy tarde, se reporta un error de protocolo de tiempo.

### 3. Lógica de Comparación Compleja

Un scoreboard básico hace un `if actual != expected:`. Sin embargo, los bloques de hardware avanzados procesan datos de formas que no se pueden evaluar con una igualdad matemática simple.

- **Comparaciones parciales:** El scoreboard puede ignorar ciertos campos de una transacción (como bits de relleno, identificadores dinámicos o flags de estado variables) y concentrarse solo en la carga útil (*payload*).
- **Predicción fuera de orden:** Si el DUT procesa datos en paralelo, las respuestas pueden salir en cualquier orden. La lógica compleja busca el dato recibido dentro de un "pool" o bolsa de transacciones esperadas acumuladas, verificando si existe una coincidencia válida sin importar la posición de llegada.
- **Scoreboards con modelos de referencia avanzados:** El scoreboard se conecta a un modelo de comportamiento en Python (como una biblioteca de procesamiento de señales o un modelo C/C++ embebido) para calcular algoritmos matemáticos complejos en tiempo real.

### 4. Optimización de Rendimiento

A medida que la simulación avanza y se envían millones de transacciones, los scoreboards mal programados pueden ralentizar drásticamente la simulación (haciendo que el entorno de Python consuma demasiada memoria o CPU).

- **Limpieza de memoria:** Un scoreboard avanzado no acumula transacciones infinitamente. En cuanto una transacción coincide y pasa la verificación, se elimina inmediatamente de las colas de memoria.
- **Estructuras de búsqueda eficientes:** En lugar de usar listas de Python comunes para buscar transacciones (lo cual obliga al procesador a recorrer toda la lista elemento por elemento), se utilizan tablas Hash, diccionarios indexados por ID de transacción (`tags`) o sets para que las búsquedas e inserciones sean instantáneas.
- **Verificación al vuelo vs. Post-procesamiento:** Para optimizar, gran parte de la lógica pesada se procesa "al vuelo" (en cuanto llega el dato), o se delega el vaciado de reportes masivos únicamente a la `check_phase` o `report_phase` final de UVM, evitando sobrecargar los logs de salida durante la simulación activa.

## Agent

- Integración de componentes (driver, monitor, sequencer)
- Configuración del agente mediante ConfigDB

- **Estructura del agente**
  - Componente driver
  - Componente monitor
  - Componente sequencer
  - Contenedor del agente

- **Agente Activo**: Contiene driver, sequencer y monitor
  - Se usa para verificación activa

- **Agente Pasivo**: Contiene solo el monitor
  - Observa únicamente el DUT
  - Se usa para monitoreo pasivo o verificación de referencia

El AgentSequece toma el dato encapsulado y lo envia al sequencer. El AgentDriver recive el dato desde el sequencer y lo envia al DUT. Luego el monitor obtiene signals que envia mediante un ap. 

Todo esto se puede englobar en un agentCompleto.

## DUT a revisar

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

- Se reinicia a ceros cuando `rst_n` está en bajo
- Cuando `valid` se afirma, establece `ready` y calcula `result = data + 1`
- Protocolo simple de handshaking (valid/ready)
- Demuestra una interfaz básica para pruebas de componentes UVM


#### 1. El Objeto de Transacción (`InterfaceTransaction`)

- **Propósito:** Actúa como el contenedor de datos transitorios de la simulación. Almacena de forma abstracta los valores que fluyen por el bus.
- **Refactorización:** Se purificó el objeto removiendo campos que pertenecían al software de predicción. Ahora solo contiene la estructura del bus físico (`data`, `address`) y hereda las bondades nativas de `uvm_sequence_item` como la visualización mediante `__str__`.

#### 2. La Secuencia (`InterfaceSequence`)

- **Propósito:** Es la encargada de generar los vectores de prueba de manera matemática o aleatoria.
- **Refactorización:** Se eliminaron las referencias cruzadas invasivas (antipatrón de inyección directa). La secuencia ya no sabe que existe un Scoreboard ni intenta depositar valores en él mediante búsquedas en el árbol jerárquico. Su único rol es inyectar ítems de secuencia hacia el secuenciador de forma abstracta y reutilizable.

#### 3. El Conductor Síncrono (`InterfaceDriver`)

- **Propósito:** Traduce los objetos abstractos de software en variaciones físicas de voltaje sobre las señales de entrada del DUT.
- **Refactorización:** Se reemplazaron los temporizadores asíncronos (`Timer(10, "ns")`) por disparadores síncronos de hardware utilizando `FallingEdge(self.dut.clk)`. Al modular las señales en el flanco de bajada, se elimina cualquier riesgo de violación de tiempos de establecimiento (*setup*) y retención (*hold*) en el diseño, respetando el ciclo de reloj real del hardware.

#### 4. El Monitor Pasivo (`InterfaceMonitor`)

- **Propósito:** Observa de forma no intrusiva los pines de salida y control del DUT.
- **Refactorización:** También se migró a un dominio síncrono controlado por `RisingEdge(self.dut.clk)`. Su activación lógica es gobernada por la señal de handshake del diseño (`if self.dut.ready.value == 1`). Cuando detecta una transacción válida, captura tanto el estímulo de entrada (`data`) como el resultado obtenido por el hardware (`result`) y los empaqueta en una tupla de Python para enviarlos por el puerto de análisis TLM (`self.ap.write`).

#### 5. El Tablero de Resultados con Modelo de Referencia Integrado (`InterfaceScoreboard`)

- **Propósito:** Actúa como el componente de evaluación y auditoría matemática de la simulación.
- **Refactorización:** Hereda de `uvm_subscriber` y aprovecha el tipado flexible de Python para capturar la tupla generada por el monitor de forma instantánea ("al vuelo" u *on-the-fly*).
- Integra internamente el **Golden Model** mediante la función `model_predict()`, replicando fielmente la especificación matemática esperada del hardware (incluyendo el comportamiento ante desbordamientos mediante la máscara de 8 bits `& 0xFF`).
- En lugar de arrastrar listas duplicadas que ralentizan la simulación o confunden el flujo temporal, compara la predicción directamente contra el valor extraído del RTL en cada llamada a `write()`.
- Incorpora la fase automática `check_phase()`, la cual imprime métricas consolidadas del testbench (`Matches`, `Mismatches`) y levanta una excepción crítica de software si el silicio arrojó algún dato inválido.

#### 6. El Orquestador del Test (`CompleteAgentTest`)

- **Propósito:** Inicializa el árbol jerárquico y gobierna los tiempos de reset y simulación global.
- **Refactorización:** Se habilitó el generador de reloj concurrente nativo de cocotb (`Clock(self.dut.clk, 10, units="ns").start()`), lo que permite que el tiempo virtual del simulador avance. Aplica un reset inicial controlado síncronamente antes de arrancar la secuencia mediante el uso seguro de objeciones UVM (`raise_objection` / `drop_objection`), garantizando que la simulación no finalice de manera prematura mientras haya transacciones en el bus.
