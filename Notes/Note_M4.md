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

## Conclusiones sobre TLM, Scoreboards y FIFOs de Análisis

La discusión sobre scoreboards termina conectando tres ideas que suelen aparecer separadas cuando uno aprende UVM: `uvm_subscriber`, `uvm_scoreboard` y las FIFOs TLM usadas como buffers entre monitores y lógica de comparación. La conclusión práctica es que no existe una única forma correcta para todos los casos; existe un nivel de complejidad adecuado para cada tipo de verificación.

La frase que resume el patrón más robusto es:

```text
El monitor publica sin bloquear.
El FIFO almacena.
El scoreboard decide cuándo consumir y comparar.
```

Esa separación es importante porque evita que el orden exacto y el instante exacto en que se llama a `write()` determinen toda la arquitectura del scoreboard. El monitor debe observar y publicar. El scoreboard debe comparar. El FIFO permite que ambos no dependan rígidamente uno del otro.

### `uvm_subscriber` vs `uvm_scoreboard`

`uvm_subscriber` y `uvm_scoreboard` se parecen porque ambos pueden terminar siendo usados como scoreboards, pero conceptualmente responden a preguntas distintas.

`uvm_subscriber` responde a:

```text
Como recibo transactions desde un analysis_port?
```

`uvm_scoreboard` responde a:

```text
Donde pongo la logica de comparacion, prediccion y chequeo?
```

Un `uvm_subscriber` ya trae un `analysis_export` preparado para conectarse directamente a un `uvm_analysis_port`. Por eso es muy cómodo para ejemplos simples:

```python
class SimpleScoreboard(uvm_subscriber):
    def build_phase(self):
        self.mismatches = []

    def write(self, txn):
        expected = self.model_predict(txn.data)
        if txn.result != expected:
            self.mismatches.append((txn, expected))
```

Y en el environment:

```python
self.agent.monitor.ap.connect(self.scoreboard.analysis_export)
```

Este patrón es directo y pedagógico:

```text
Monitor.ap -> Scoreboard.analysis_export -> write(txn)
```

Funciona bien cuando hay una sola fuente de datos, la comparación es inmediata y no hace falta coordinar múltiples streams. En el ejemplo actual del `InterfaceScoreboard`, esto tiene sentido: el monitor publica una tupla con lo observado y el scoreboard calcula el resultado esperado al vuelo usando `model_predict()`.

`uvm_scoreboard`, en cambio, es más apropiado cuando el scoreboard necesita tener arquitectura propia: varias entradas, FIFOs internas, modelos de referencia, matching por ID, comparación fuera de orden, acumulación temporal o lógica de reordenamiento. Si se hereda de `uvm_scoreboard`, normalmente se deben declarar explícitamente las entradas TLM que recibirán datos desde los monitores.

La regla importante es:

```text
El monitor tiene el analysis_port.
El scoreboard tiene el lado receptor: analysis_export, analysis_imp o analysis_fifo.
El env conecta ambos en connect_phase().
```

No conviene decir que el scoreboard declara `analysis_port` para recibir. En UVM, el `analysis_port` vive en quien publica; el receptor tiene un export, imp o FIFO con `analysis_export`.

### Por qué no comparar siempre dentro de `write()`

Comparar dentro de `write()` es simple, pero tiene una limitación: `write()` se ejecuta en el instante en que llega una transaction desde un monitor. Si hay dos monitores, por ejemplo uno de entrada y otro de salida, cada llamada llega por separado. El scoreboard puede recibir primero una entrada, después una salida, o incluso varias entradas antes de la primera salida si el DUT tiene latencia.

Con un scoreboard sencillo, uno suele escribir algo como:

```text
input_monitor.ap  -> scoreboard.write_input(txn)
output_monitor.ap -> scoreboard.write_output(txn)
```

Internamente, el scoreboard mantiene colas o diccionarios:

```python
self.expected.append(expected_txn)
self.actual.append(actual_txn)
```

Esto funciona, pero la lógica puede ensuciarse rápido. Además, si el emparejamiento depende solo del orden de llegada, una transaction espuria, un ciclo idle mal muestreado o una diferencia de latencia puede desalinear todo el scoreboard.

Por eso aparece el patrón con FIFO de análisis.

### El patrón observado: `uvm_tlm_analysis_fifo`

El patrón que aparece en muchos testbenches más elaborados es este:

```text
monitor.ap
   |
   v
scoreboard.<nombre>_fifo.analysis_export
   |
   v
cola interna de transactions
   |
   v
scoreboard.run_phase consume con get(), try_get() o peek()
```

La clase clave es `uvm_tlm_analysis_fifo`. Es una FIFO TLM especializada para recibir transactions desde un `analysis_port`. Combina dos mundos:

- Por el lado de entrada, expone `analysis_export`, por lo que un monitor puede conectarse directamente con `monitor.ap.connect(fifo.analysis_export)`.
- Por dentro, almacena cada transaction en una cola.
- Por el lado de consumo, se comporta como FIFO: permite `get()`, `try_get()`, `peek()`, `try_peek()` y consultas tipo `can_get()`/`can_peek()`.

Esto convierte un broadcast no bloqueante de análisis en una fuente consumible por el scoreboard:

```text
analysis_port.write(txn) -> analysis_fifo.analysis_export -> FIFO interna -> scoreboard consume
```

Ejemplo conceptual:

```python
class RobustScoreboard(uvm_scoreboard):
    def build_phase(self):
        self.expected_fifo = uvm_tlm_analysis_fifo("expected_fifo", self)
        self.actual_fifo = uvm_tlm_analysis_fifo("actual_fifo", self)
        self.mismatches = []

    async def run_phase(self):
        while True:
            expected = await self.expected_fifo.get()
            actual = await self.actual_fifo.get()

            if not self.compare(expected, actual):
                self.mismatches.append((expected, actual))
                self.logger.error(
                    f"Mismatch: expected={expected}, actual={actual}"
                )
```

Y en el environment:

```python
self.input_monitor.ap.connect(self.scoreboard.expected_fifo.analysis_export)
self.output_monitor.ap.connect(self.scoreboard.actual_fifo.analysis_export)
```

El scoreboard deja de depender de que `write_input()` y `write_output()` hagan toda la lógica. Los monitores publican. Las FIFOs acumulan. El `run_phase()` del scoreboard decide cuándo hay suficiente información para comparar.

### Utilidad de `uvm_tlm_analysis_fifo`

`uvm_tlm_analysis_fifo` es útil cuando:

- Hay múltiples monitores publicando streams distintos.
- El DUT tiene latencia.
- El producer y el consumer no avanzan al mismo ritmo.
- El scoreboard debe esperar a tener una transaction esperada y una real.
- Se quiere evitar lógica pesada dentro de `write()`.
- Se necesita controlar el orden de consumo desde el `run_phase()` del scoreboard.
- Se desea desacoplar observación y comparación.

No significa que la sincronía desaparece. La sincronía se encapsula en la FIFO. Si el scoreboard hace `await fifo.get()` y no hay datos, solo se bloquea esa corrutina, no todo el entorno. Si se usa `try_get()`, el scoreboard puede preguntar sin bloquear.

Comparación mental:

```text
Sin FIFO:
Monitor llama write() y obliga al scoreboard a reaccionar inmediatamente.

Con analysis FIFO:
Monitor deposita transaction y sigue observando.
Scoreboard consume cuando su algoritmo lo necesita.
```

### `uvm_tlm_fifo` vs `uvm_tlm_analysis_fifo`

Ambas son FIFOs TLM, pero se usan en lugares distintos.

`uvm_tlm_fifo` es la FIFO general de put/get:

```text
Producer.put_port -> fifo.put_export
Consumer.get_port -> fifo.get_export
```

Ejemplo:

```python
self.fifo = uvm_tlm_fifo("fifo", self)
self.producer.put_port.connect(self.fifo.put_export)
self.consumer.get_port.connect(self.fifo.get_export)
```

Es ideal cuando los dos extremos son componentes activos que usan puertos TLM explícitos: uno hace `put()` y otro hace `get()`.

`uvm_tlm_analysis_fifo` está pensada para el caso de monitores:

```text
Monitor.analysis_port -> fifo.analysis_export
Scoreboard consume desde fifo
```

Ejemplo:

```python
self.actual_fifo = uvm_tlm_analysis_fifo("actual_fifo", self)
self.monitor.ap.connect(self.scoreboard.actual_fifo.analysis_export)
```

La diferencia de intención es clara:

```text
uvm_tlm_fifo:
  producer/consumer directo con put/get.

uvm_tlm_analysis_fifo:
  adaptador entre analysis_port.write(txn) y consumo tipo FIFO.
```

Para scoreboards conectados a monitores, `uvm_tlm_analysis_fifo` suele ser más natural que `uvm_tlm_fifo`, porque el monitor ya publica con `analysis_port.write(txn)`.

### Utilidad de `uvm_nonblocking_get_port`

El nombre correcto en pyuvm es `uvm_nonblocking_get_port`. Es común escribirlo mal como `uvm_nonoblocking_get_port`, pero ese nombre contiene un typo.

Este puerto da acceso a métodos no bloqueantes de get:

```python
success, txn = self.get_port.try_get()
can_get = self.get_port.can_get()
```

Su utilidad principal es permitir que un componente pregunte si hay datos disponibles sin quedarse suspendido esperando. Esto es diferente de:

```python
txn = await fifo.get()
```

`await fifo.get()` bloquea la corrutina hasta que exista una transaction. Eso puede ser correcto si el algoritmo realmente necesita esperar. Pero en scoreboards más complejos, muchas veces se quiere revisar varias fuentes y actuar solo cuando existe una combinación válida.

Ejemplo conceptual:

```python
class MatchingScoreboard(uvm_scoreboard):
    def build_phase(self):
        self.actual_get_port = uvm_nonblocking_get_port("actual_get_port", self)
        self.expected_get_port = uvm_nonblocking_get_port("expected_get_port", self)

    def connect_phase(self):
        self.actual_get_port.connect(self.actual_fifo.nonblocking_get_export)
        self.expected_get_port.connect(self.expected_fifo.nonblocking_get_export)

    async def run_phase(self):
        while True:
            got_exp, expected = self.expected_get_port.try_get()
            got_act, actual = self.actual_get_port.try_get()

            if got_exp and got_act:
                self.compare(expected, actual)
            else:
                await Timer(1, units="ns")
```

La ventaja es que el scoreboard no queda atrapado obligatoriamente esperando una sola FIFO. Puede recorrer varias fuentes, priorizar canales, revisar timeouts, o implementar matching fuera de orden.

Si el scoreboard posee directamente las FIFOs, no siempre hace falta declarar puertos no bloqueantes. En pyuvm también se puede llamar directamente:

```python
success, txn = self.actual_fifo.try_get()
```

Entonces, ¿por qué algunos patrones declaran `uvm_nonblocking_get_port`? Por arquitectura. El puerto desacopla el algoritmo consumidor del objeto FIFO concreto. El scoreboard puede tener lógica que consume desde un endpoint TLM sin saber si detrás hay una FIFO, un modelo, un canal o algún adaptador.

### Utilidad de `uvm_nonblocking_peek_port`

El nombre correcto es `uvm_nonblocking_peek_port`.

`peek` permite mirar el próximo elemento sin removerlo de la FIFO. Su versión no bloqueante permite intentar mirar sin quedarse esperando:

```python
success, txn = self.peek_port.try_peek()
can_peek = self.peek_port.can_peek()
```

Esto es útil cuando el scoreboard necesita inspeccionar una transaction antes de decidir si la consume. Por ejemplo:

- Ver si el próximo item tiene el ID buscado.
- Comparar timestamps antes de sacar el dato.
- Evitar consumir un actual si todavía no existe su expected correspondiente.
- Implementar matching fuera de orden.
- Revisar cabeceras o tags sin alterar la cola.

Ejemplo conceptual:

```python
class ReorderScoreboard(uvm_scoreboard):
    def build_phase(self):
        self.actual_peek_port = uvm_nonblocking_peek_port("actual_peek_port", self)
        self.actual_get_port = uvm_nonblocking_get_port("actual_get_port", self)

    def connect_phase(self):
        self.actual_peek_port.connect(self.actual_fifo.nonblocking_peek_export)
        self.actual_get_port.connect(self.actual_fifo.nonblocking_get_export)

    async def run_phase(self):
        while True:
            can_see, actual = self.actual_peek_port.try_peek()

            if can_see and self.expected_exists_for(actual.id):
                ok, actual = self.actual_get_port.try_get()
                if ok:
                    expected = self.expected_by_id.pop(actual.id)
                    self.compare(expected, actual)
            else:
                await Timer(1, units="ns")
```

La diferencia clave entre `get` y `peek` es:

```text
get  -> mira y remueve.
peek -> mira sin remover.
```

Por eso `peek` es tan útil en scoreboards que no quieren destruir el orden de una cola hasta estar seguros de poder comparar.

### Por qué algunos scoreboards declaran varios puertos alrededor de cada FIFO

En ciertos diseños se ve que, por cada conexión con un monitor, el scoreboard declara una estructura con:

- un `uvm_tlm_analysis_fifo`, para recibir y almacenar lo que publica el monitor;
- un `uvm_nonblocking_get_port`, para intentar consumir sin bloquear;
- un `uvm_nonblocking_peek_port`, para mirar sin consumir;
- a veces también un puerto combinado tipo get/peek o exports renombrados para hacer el código más legible.

Esto puede parecer redundante al principio, porque el FIFO ya expone métodos y exports internos. Pero el objetivo no siempre es necesidad técnica mínima; muchas veces es claridad arquitectónica.

El patrón expresa una intención:

```text
analysis_fifo:
  recibe desde el monitor.

nonblocking_get_port:
  consume cuando el algoritmo decide que puede remover.

nonblocking_peek_port:
  inspecciona sin modificar el estado de la cola.
```

Se puede imaginar como una pequeña interfaz de entrada del scoreboard:

```text
monitor.ap
   |
   v
input_channel.analysis_fifo.analysis_export
   |
   +--> input_channel.peek_port.try_peek()  # mirar sin sacar
   |
   +--> input_channel.get_port.try_get()    # sacar cuando corresponde
```

Una forma conceptual de encapsularlo sería:

```python
class ScoreboardInput:
    def __init__(self, name, parent):
        self.fifo = uvm_tlm_analysis_fifo(f"{name}_fifo", parent)
        self.get_port = uvm_nonblocking_get_port(f"{name}_get_port", parent)
        self.peek_port = uvm_nonblocking_peek_port(f"{name}_peek_port", parent)

    def connect_phase(self):
        self.get_port.connect(self.fifo.get_export)
        self.peek_port.connect(self.fifo.peek_export)
```

No es redundante que el puerto sea no bloqueante y que se conecte contra `get_export` o `peek_export`. El tipo del puerto (`uvm_nonblocking_get_port` o `uvm_nonblocking_peek_port`) ya restringe la intención del acceso: usar `try_get()`/`can_get()` o `try_peek()`/`can_peek()`. En pyuvm, `get_export` y `peek_export` son exports compuestos que exponen la interfaz correspondiente. Por eso conectar de esta forma mantiene el código limpio y evita sobredocumentar la misma idea con nombres demasiado largos como `nonblocking_get_export`, salvo que se quiera ser extremadamente explícito por estilo de equipo.

Luego el environment conecta el monitor al FIFO:

```python
self.input_monitor.ap.connect(self.scoreboard.input_channel.fifo.analysis_export)
self.output_monitor.ap.connect(self.scoreboard.output_channel.fifo.analysis_export)
```

Y el scoreboard usa nombres semánticos:

```python
ok, actual = self.output_channel.peek_port.try_peek()
if ok and self.can_match(actual):
    ok, actual = self.output_channel.get_port.try_get()
```

La ganancia es que el scoreboard deja de pensar en detalles de almacenamiento y empieza a hablar en términos del algoritmo de verificación: mirar, decidir, consumir, comparar.

### Ejemplo de Nivel 3: `AvancedScoreboard` parametrizable

Una forma práctica y reusable de llevar este patrón al código es construir una clase base que reciba una lista de nombres de puertos lógicos. Cada nombre representa una entrada del scoreboard: `input`, `output`, `expected`, `actual`, `read`, `write`, `channel0`, etc. A partir de esos nombres, el scoreboard crea automáticamente tres estructuras por entrada:

- un `uvm_tlm_analysis_fifo`, que recibe transactions desde el monitor;
- un `uvm_nonblocking_get_port`, que consume transactions sin bloquear;
- un `uvm_nonblocking_peek_port`, que mira la próxima transaction sin removerla.

El modelo queda así:

```python
from pyuvm import *


class AvancedScoreboard(uvm_scoreboard):
    def __init__(self, name, parent, port_names: list[str]):
        super().__init__(name, parent)
        self.port_names = port_names

    def build_phase(self):
        port_names = self.port_names

        self.fifos = {
            p: uvm_tlm_analysis_fifo(f"{p}_fifo", self)
            for p in port_names
        }

        self.get_ports = {
            p: uvm_nonblocking_get_port(f"{p}_port", self)
            for p in port_names
        }

        self.peek_ports = {
            p: uvm_nonblocking_peek_port(f"{p}_peek_port", self)
            for p in port_names
        }

    def connect_phase(self):
        for p in self.port_names:
            self.get_ports[p].connect(self.fifos[p].get_export)
            self.peek_ports[p].connect(self.fifos[p].peek_export)
```

Este diseño encaja muy bien con la conclusión anterior porque separa explícitamente las tres responsabilidades de cada entrada:

```text
fifos[p]
  recibe y almacena lo que publica el monitor.

get_ports[p]
  remueve una transaction solo cuando el algoritmo quiere consumirla.

peek_ports[p]
  inspecciona la próxima transaction sin modificar la cola.
```

La conexión desde el environment queda limpia y semántica:

```python
self.input_monitor.ap.connect(self.scoreboard.fifos["input"].analysis_export)
self.output_monitor.ap.connect(self.scoreboard.fifos["output"].analysis_export)
```

Luego una clase concreta puede heredar de `BaseScoreboard` y concentrarse solo en la política de comparación:

```python
class InterfaceScoreboard(BaseScoreboard):
    def __init__(self, name, parent):
        super().__init__(name, parent, ["expected", "actual"])
        self.mismatches = []

    async def run_phase(self):
        while True:
            has_exp, expected = self.peek_ports["expected"].try_peek()
            has_act, actual = self.peek_ports["actual"].try_peek()

            if has_exp and has_act and self.can_compare(expected, actual):
                _, expected = self.get_ports["expected"].try_get()
                _, actual = self.get_ports["actual"].try_get()
                self.compare(expected, actual)
            else:
                await Timer(1, units="ns")
```

La ventaja de mirar primero con `peek` es que el scoreboard no destruye el orden de ninguna FIFO hasta saber que puede comparar. Si todavía no existe la pareja correspondiente, la transaction permanece almacenada y puede ser revisada de nuevo en otro ciclo del algoritmo.

Este patrón da muy buen resultado porque transforma el scoreboard en una pieza reusable. La estructura de entrada se define con nombres; la política de matching vive en la clase hija. Así se evita reescribir boilerplate cada vez que aparece un nuevo monitor o una nueva stream de verificación.

### Cuando usar este patrón y cuando no

Para ejemplos simples del módulo, el patrón con `uvm_subscriber` es suficiente y más fácil de leer:

```text
Monitor.ap -> Scoreboard.analysis_export -> write(txn)
```

Conviene cuando:

- hay un solo stream;
- la comparación es inmediata;
- no hay latencia variable;
- no hay reordenamiento;
- el objetivo es enseñar el camino básico del `analysis_port`.

Para scoreboards más serios, el patrón con `uvm_scoreboard + uvm_tlm_analysis_fifo` es más robusto:

```text
input_monitor.ap  -> expected_fifo.analysis_export
output_monitor.ap -> actual_fifo.analysis_export

scoreboard.run_phase:
    expected = await expected_fifo.get()
    actual   = await actual_fifo.get()
    compare(expected, actual)
```

Y si además se necesitan decisiones no bloqueantes:

```text
try_peek() -> miro sin sacar
try_get()  -> saco solo cuando puedo comparar
```

Conviene cuando:

- hay múltiples monitores;
- el DUT tiene latencia;
- las respuestas pueden llegar fuera de orden;
- se necesita matching por ID, timestamp o ciclo;
- se deben revisar timeouts;
- no se quiere bloquear esperando una sola fuente;
- se quiere separar recepción, almacenamiento y comparación.

### Conclusión práctica

La arquitectura más limpia depende de la escala del problema:

```text
Nivel 1 - Scoreboard simple:
Monitor.ap -> uvm_subscriber.analysis_export -> write(txn)

Nivel 2 - Scoreboard con buffering:
Monitor.ap -> uvm_tlm_analysis_fifo.analysis_export
Scoreboard consume con get() / try_get()

Nivel 3 - Scoreboard avanzado:
Monitor.ap -> analysis_fifo
Scoreboard usa nonblocking_get_port y nonblocking_peek_port
Matching por ID, tiempo, orden parcial o modelo de referencia.
```

No hay que usar FIFO TLM para absolutamente todo. Pero cuando aparece la necesidad de desacoplar tiempos, comparar múltiples fuentes o evitar que `write()` haga demasiado trabajo, el patrón con `uvm_tlm_analysis_fifo` es una de las soluciones más sensatas.

La idea final es no confundir simplicidad con robustez. `uvm_subscriber` es ideal para aprender y para scoreboards pequeños. `uvm_scoreboard` con FIFOs de análisis es mejor cuando la verificación empieza a parecerse a un sistema real: monitores independientes, latencias variables, comparaciones complejas y necesidad de controlar explícitamente cuándo una transaction se mira, se consume y se compara.
