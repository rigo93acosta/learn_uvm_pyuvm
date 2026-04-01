# MODULE 3: UVM Fundamentals

Focusing on UVM (Universal Verification Methodology) fundamentals including class hierarchy, phases, reporting, configuration database, factory pattern, and objection mechanism.

En esto módulo se profundiza en los siguientes temas:
- Class Hierarchy
- Phases
- Reporting
- Configuration Database
- Factory Pattern
- Objection Mechanism

> Debe quedar claro: `uvm_agent` - Agent (driver, monitor, sequencer)

Relaciones entre clases:
  - Inheritance hierarchy: `uvm_component` -> `uvm_agent` -> `uvm_driver`, `uvm_monitor`, `uvm_sequencer`
  - Composition patterns: `uvm_env` contiene agentes, `uvm_test` contiene ambientes, etc.
  - Factory pattern: `uvm_factory` para crear objetos de manera flexible y configurable.

A partir de aca voy a eliminar este wrapper que ya no es necasario:
```python
# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_class_hierarchy(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ClassHierarchyTest"] = ClassHierarchyTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ClassHierarchyTest")
```

Esto se puede eliminar colocondo el decorador `@pyuvm.test()` directamente en la clase de test, lo cual es más limpio y directo.

## Class Hierarchy example code

* Primero creamos un objeto de tipo transaction (`MyTransaction`), el cual tiene dos campos: `data` y `address`. Esta clase extiende de `uvm_sequence_item`, lo que la hace compatible con el mecanismo de secuencias y drivers de UVM.
* Luego, creamos un driver (`MyDriver`) que extiende de `uvm_driver`. En su `build_phase`, se crea un puerto de tipo `uvm_seq_item_port` (esto ya se hace por default, descrito en los errores de esta sección) para recibir transacciones. Hay una fase de `connect_phase` donde se podrían conectar puertos a otros componentes (como por ejemplo conectar el puerto del driver al puerto del sequencer), pero en este ejemplo no se hace nada específico. En el `run_phase`, el driver espera a recibir una transacción a través del puerto, y luego la procesa (en este caso, simplemente imprime sus campos).
* Luego, creamos un monitor (`MyMonitor`) que extiende de `uvm_monitor`. En su `build_phase` crea un `uvm_analysis_port` para enviar información a otros componentes (como por ejemplo a un scoreboard o un suscriber). En el `run_phase` simula la generación de transacciones (en este caso, simplemente crea una transacción con valores fijos y la imprime) y luego la envía a través del `analysis_port`.
* Lo siguiente es crear un agente (`MyAgent`) que extiende de `uvm_agent`. En su `build_phase` crea instancias del driver, el monitor y el sequencer. En este ejemplo se conecta el puerto del driver al puerto del sequencer, pero no se hace nada con el monitor.
* Luego, se crea un ambiente (`MyEnv`) que extiende de `uvm_env`. En su `build_phase` crea una instancia del agente. En su `connect_phase` se podrían conectar los puertos del agente a otros componentes del ambiente, pero en este ejemplo no se hace nada específico.
* Finalmente, se crea una clase de test (`ClassHierarchyTest`) que extiende de `uvm_test`. En su `build_phase` crea una instancia del ambiente. En su `connect_phase` se podrían conectar los puertos del ambiente a otros componentes del test, pero en este ejemplo no se hace nada específico. Solo crear un transaction. 

> Este ejemplo es muy básico y no hace nada funcional, pero sirve para ilustrar la estructura de clases y fases en UVM.

### Cambios realizados (Class Hierarchy)

#### Error 1
- **Error:** `RuntimeWarning: coroutine 'ClassHierarchyTest.build_phase/connect_phase' was never awaited`
- **Por que sucede:** En pyuvm, `build_phase` y `connect_phase` se ejecutan de forma sincronica (sin `await`). Si se definen como `async def`, al invocarlas como metodos normales se crea una corrutina que no se espera, y Python lanza ese warning.
- **Como se arreglo:** Cambiar esas fases en `ClassHierarchyTest` de `async def` a `def`.

#### Error 2
- **Error:** `NameError: name 'uvm_seq_item_pull_port' is not defined`
- **Por que sucede:** En esta version de pyuvm no existe `uvm_seq_item_pull_port`; la API valida es `uvm_seq_item_port`.
- **Como se arreglo:** Se reemplazo por `uvm_seq_item_port`.

#### Error 3
- **Error:** `already has a child named seq_item_port`
- **Por que sucede:** `uvm_driver` ya trae `seq_item_port` por defecto. Al crearlo otra vez en `build_phase`, se duplica el hijo con el mismo nombre.
- **Como se arreglo:** Se elimino la creacion manual de `seq_item_port` en el driver.


