# Section: Triggers

En el mundo de la simulación con **cocotb**, el trigger `ReadOnly` es fundamental para evitar lo que en hardware llamamos "condiciones de carrera" (race conditions) entre el testbench y el simulador.

### ¿Qué hace exactamente `ReadOnly`?

En una simulación digital, el tiempo no avanza de forma continua, sino por **pasos de tiempo** (time steps). Dentro de un mismo nanosegundo, ocurren muchas operaciones lógicas en diferentes "deltas".

Cuando usas `await ReadOnly()`:

1.  **Detiene el testbench:** Le dice a Python que espere hasta que el simulador de Verilog/VHDL haya terminado de propagar todas las señales y cálculos lógicos del paso de tiempo actual.
2.  **Entra en modo "Solo Lectura":** El simulador garantiza que no habrá más cambios en los valores de las señales en ese instante exacto.
3.  **Garantiza consistencia:** Te permite leer el valor de una salida (como `dut.q`) con la total seguridad de que es el valor final y estable, después de que toda la lógica combinacional se haya resuelto.

---

### El Ciclo de Vida del Simulador
Para entenderlo mejor, imagina el orden en que ocurren las cosas cuando llega un flanco de reloj:

1.  **Active Phase:** El reloj sube. El diseño (DUT) reacciona y las señales empiezan a cambiar.
2.  **NBA (Non-Blocking Assignment) Phase:** Se actualizan los registros (flip-flops).
3.  **Post-Update:** Aquí es donde entra `ReadOnly`. Es el último suspiro del paso de tiempo.



---

### ¿Por qué es necesario en tu ejemplo?

Mira esta parte de tu código:

```python
await dut.clk.rising_edge  # 1. Llega el flanco
await ReadOnly()           # 2. Esperamos a que la lógica se estabilice
cocotb.log.info(...)       # 3. Leemos el resultado real
```

Si intentaras leer `dut.q` **inmediatamente** después de `await dut.clk.rising_edge` sin el `ReadOnly`, podrías encontrarte con un problema: **Python podría ser más rápido que el simulador**. 

Podrías leer el valor "viejo" de la señal antes de que el simulador termine de calcular el nuevo valor que debería tener tras el flanco de reloj. Al usar `ReadOnly`, te aseguras de que el log muestre el valor real que quedó "impreso" en el hardware.

---

### Una regla de oro
* **Para escribir (Drive):** Usa los flancos de reloj (`rising_edge`).
* **Para leer y verificar (Monitor/Sample):** Usa `ReadOnly` para asegurarte de que no estás leyendo basura o valores transitorios.

> **Dato importante:** Al igual que con los otros triggers, en versiones muy recientes de cocotb, se prefiere a veces usar `await NextTimeStep()` o simplemente confiar en el modelo de programación asíncrona, pero `ReadOnly` sigue siendo el estándar de oro para muestreo seguro de señales.

# Section: Reset

El archivo `reset_patterns_example.py` contiene ejemplos prácticos de patrones de reset implementados con **cocotb**. A continuación, se resumen los principales aspectos:

- **Reset Asíncrono (`async_reset`)**: Implementa una secuencia de reset asíncrono que asegura la estabilización del DUT tras desactivar el reset. Incluye parámetros configurables como la duración del reset y el retraso de propagación.
- **Reset Síncrono (`sync_reset`)**: Demuestra un patrón de reset síncrono, manteniendo el reset durante un número específico de ciclos de reloj. Aunque el DUT utiliza un reset asíncrono, este ejemplo ilustra cómo aplicar un reset síncrono.
- **Pruebas de Reset**:
  - `test_async_reset`: Verifica que el reset asíncrono inicialice correctamente el DUT.
  - `test_sync_reset`: Valida el comportamiento del reset síncrono, asegurando que el DUT se reinicie y mantenga el estado esperado.
  - `test_reset_verification`: Comprueba el comportamiento del DUT durante y después de aplicar un reset, incluyendo la aceptación de nuevos datos tras liberar el reset.
  - `test_reset_initialization`: Garantiza que el DUT se inicialice correctamente después de un reset.

Estos ejemplos destacan la importancia de manejar correctamente los resets en simulaciones digitales, asegurando la consistencia y estabilidad del DUT en diferentes escenarios.

# Section: Common Patterns

> Mantener la buena de aplicar un reset async con retardo permitiendo la estabilizacion luego del reset.

Se implementa la clase `Scoreboard`, una forma sencilla de este tipo de estructura para la verificacion.

## test_sequential_pattern

Es un ejemplo sencillo de verificacion:
1. Aplico reset.
2. Activo la escritura.
3. Envio un conjunto de valores predeterminados de tests al DUT
4. Compruebo si a la salida tengo iguales valores.

## test_random_pattern

Igual que ejemplo anterior, pero en este caso el conjunto de valores es aleatorio. (Paso 3)

## test_scoreboard_pattern

Ejemplo sencillo igualmente pero en este caso empleando una clase que separa el dato enviado del recibido dentro de la misma estructura, desacomplando la verificacion de los datos del clock de reloj.

1. Aplico reset.
2. Activo la escritura.
3. Envio un conjunto de valores predeterminados de tests al DUT.
4. Recibo un conjunto de valore del DUT y los almaceno
5. Compruebo si ambos datos son iguales.

## test_reference_model

En lugar de simplemente probar valores "fijos" uno por uno, lo que haces es crear una versión en software de lo que debería hacer tu hardware (el DUT).

> El objetivo es asegurar que la salida del hardware (dut.q) sea exactamente igual a lo que nuestro modelo matemático o lógico en Python predice. Si el hardware se comporta distinto al modelo, el test falla.

En este caso, el diseño es un registro simple que guarda el valor de entrada. reference_q es nuestra variable de Python que "imitará" al registro físico.

## test_transaction_level

### Verificación Basada en Transacciones (TLM)

El test `test_transaction_level` implementa el concepto de **Transaction-Level Modeling (TLM)**. En lugar de manipular señales individuales (bits) de forma aislada, agrupamos los datos y el comportamiento esperado en un único objeto lógico.

#### 1. Clase de Transacción (`RegisterTransaction`)
Se define una clase que encapsula toda la información necesaria para una operación en el DUT. Sus atributos clave son:

* `self.enable`: Define si la operación debe realizar un cambio en el estado del hardware.
* `self.data`: El valor de entrada que se desea escribir.
* `self.expected_result`: Es la predicción. Se calcula en el momento de crear el objeto usando la lógica: `data if enable else None`.

#### 2. Ventajas de este enfoque

* Encapsulamiento: Toda la información necesaria (estímulo + resultado esperado) está contenida en un objeto, facilitando la administración de los casos de prueba.
* Abstracción: El testbench deja de pensar en "flancos de reloj" y empieza a pensar en "operaciones de registro", lo que hace el código más legible y mantenible.
* Auto-verificación (Self-checking): Al incluir el `expected_result` dentro de la transacción, el bucle de ejecución puede validar automáticamente si el DUT se comportó correctamente sin necesidad de lógica externa compleja.

### 3. Flujo de Ejecución

1.  Generación Se crea una lista de objetos `RegisterTransaction` (el "Plan de Prueba").
2.  Drive (Excitación): Un bucle recorre la lista y aplica los atributos del objeto a los pines del DUT (`dut.enable` y `dut.d`).
3.  Monitor & Check: Tras el flanco de reloj, se compara el valor real del DUT (`dut.q`) contra el `expected_result` almacenado en la transacción actual.

> En el código, cuando `enable` es 0, el `expected_result` se pone en `None`. Esto es una forma elegante de decirle al test: "En esta transacción no espero que el registro cambie, así que no verifiques nada (o verifica que mantuvo el valor anterior)".

# Test 

## Simple Register

En este modulo de test se verificaron los siguientes comportamientos para un registro simple:

* Reset
* Write
* Enable
* Secuencia de datos
* 

## Shift Register

En este modulo de test de un registro de desplazamiento simple:
* Reset
* Operacion del shift register
* Secuencia de datos
* Verificacion de la salida serial
