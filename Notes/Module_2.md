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

