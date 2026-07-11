# Module 5: Conceptos Avanzados de UVM

## Secuencias Virtuales

### Idea central
Una **secuencia virtual** no genera transacciones propias. Es una capa de **orquestación** que coordina secuencias reales corriendo en múltiples secuenciadores distintos (útil cuando el DUT tiene varias interfaces que deben estimularse de forma coordinada).

### Componentes

| Componente | Rol |
|---|---|
| **VirtualSequencer** | Extiende `uvm_sequencer`. Solo contiene referencias a otros sequencers (`master_seqr`, `slave_seqr`), inicializadas en `None` en `build_phase()`. **No tiene `connect_phase`** — no le corresponde a él llenarlas. |
| **VirtualSequence** | Extiende `uvm_sequence`. Obtiene las referencias a los sequencers reales a través de `self.sequencer` (el sequencer sobre el que fue arrancada), no de atributos seteados a mano |
| **ChannelSequence** | Secuencia "normal" que genera transacciones para un canal específico. Se reutiliza para simular distintos roles (master/slave) cambiando el atributo `channel` |

### El cambio clave: `self.sequencer` en vez de cableado manual

**Antes (con bug):** el `VirtualSequencer` intentaba resolver sus propias referencias:
```python
# ❌ Roto: el sequencer no tiene acceso a self.env
def connect_phase(self):
    self.master_seqr = self.env.master_agent.seqr
```
Esto lanzaba `AttributeError` porque un `uvm_sequencer` no tiene noción de `env`.

**Ahora:** el `VirtualSequencer` solo declara y expone los slots:
```python
class VirtualSequencer(uvm_sequencer):
    def build_phase(self):
        self.master_seqr = None
        self.slave_seqr = None
```

Es el **env** —que sí conoce a todos los agentes— quien llena las referencias:
```python
class VirtualEnv(uvm_env):
    def connect_phase(self):
        self.virtual_seqr.master_seqr = self.master_agent.seqr
        self.virtual_seqr.slave_seqr = self.slave_agent.seqr
```

Y la `VirtualSequence` ya no recibe nada por atributos externos. Cuando se arranca sobre el virtual sequencer (`await virtual_seq.start(self.env.virtual_seqr)`), pyuvm setea `self.sequencer = virtual_seqr` automáticamente. Entonces el `body()` simplemente lee:
```python
async def body(self):
    master_seqr = self.sequencer.master_seqr
    slave_seqr = self.sequencer.slave_seqr
```

Esto es el equivalente pyuvm de `p_sequencer` en SystemVerilog/UVM: la secuencia obtiene el sequencer "tipado" sobre el que corre, sin que nadie tenga que pasarle nada a mano desde afuera.

### Patrones de ejecución 

**Paralelo:**
```python
master_task = cocotb.start_soon(master_seq.start(master_seqr))
slave_task = cocotb.start_soon(slave_seq.start(slave_seqr))
await master_task
await slave_task
```

**Secuencial:**
```python
await seq1.start(master_seqr)
await seq2.start(slave_seqr)
```

### Test — arranque simplificado
```python
virtual_seq = VirtualSequence(name="virtual_seq")
await virtual_seq.start(self.env.virtual_seqr)
```
Sin copiar referencias a mano antes de arrancar. El único cableado manual que queda es el del **env**, que es donde corresponde (es el único componente que conoce a todos los agentes).

### Flujo resultante
```
VirtualEnv.connect_phase        →  llena virtual_seqr.master_seqr / .slave_seqr
        │
virtual_seq.start(virtual_seqr) →  self.sequencer = virtual_seqr
        │
VirtualSequence.body()          →  lee self.sequencer.master_seqr / .slave_seqr
```

![Flujo de ejecución de secuencias virtuales](./images/virtualseq.png)


### Qué se corrigió respecto a la primera versión
- ❌ `AttributeError` por acceder a `self.env` desde el sequencer → ✅ eliminado.
- ❌ Cableado manual duplicado en el test → ✅ eliminado, el test solo arranca la secuencia.
- ✅ El `VirtualSequencer` ahora cumple su función real: único punto de referencias, consultado vía `self.sequencer` — el patrón correcto de `p_sequencer` en pyuvm.


