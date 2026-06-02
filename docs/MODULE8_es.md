# Módulo 8: Utilidades Misceláneas de UVM

**Objetivo**: Dominar las clases de utilidad UVM y funciones auxiliares

## Resumen

Este módulo cubre las utilidades misceláneas proporcionadas por UVM que soportan entornos de verificación. Estas utilidades incluyen procesamiento de línea de comandos, comparadores, grabadores, pools de objetos, colas y varias clases auxiliares que hacen la verificación más eficiente y organizada.

### Ejemplos y Estructura de Código

Este módulo incluye ejemplos completos y testbenches ubicados en el directorio `module8/`:

```
module8/
├── examples/              # Ejemplos de utilidades pyuvm
│   ├── clp/              # Ejemplos de procesador de línea de comandos
│   ├── comparators/      # Ejemplos de comparadores
│   ├── recorders/        # Ejemplos de grabadores
│   ├── pools/            # Ejemplos de pools
│   ├── queues/           # Ejemplos de colas
│   ├── string_utils/     # Ejemplos de utilidades de cadenas
│   ├── math_utils/       # Ejemplos de utilidades matemáticas
│   ├── random_utils/     # Ejemplos de utilidades aleatorias
│   └── integration/      # Ejemplos de integración de utilidades
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # Testbenches pyuvm
└── README.md             # Documentación del Módulo 8
```

### Inicio Rápido

**Ejecutar todos los ejemplos usando el script orquestador:**
```bash
# Ejecutar todos los ejemplos
./scripts/module8.sh

# Ejecutar ejemplos específicos
./scripts/module8.sh --clp
./scripts/module8.sh --comparators
./scripts/module8.sh --recorders
./scripts/module8.sh --pools
./scripts/module8.sh --queues
./scripts/module8.sh --string-utils
./scripts/module8.sh --math-utils
./scripts/module8.sh --random-utils
./scripts/module8.sh --integration
./scripts/module8.sh --pyuvm-tests
```

**Ejecutar ejemplos individualmente:**
```bash
# Activar entorno virtual (si usas uno)
source .venv/bin/activate

# Ejecutar pruebas pyuvm
cd module8/tests/pyuvm_tests
make SIM=verilator TEST=test_utilities

# Los ejemplos son ejemplos estructurales de pyuvm
# Se pueden importar y usar en tus testbenches
```

## Temas Cubiertos

### 1. Procesador de Línea de Comandos UVM (CLP)

- **Resumen del Procesador de Línea de Comandos**
  - ¿Qué es CLP?
  - ¿Por qué usar CLP?
  - Beneficios de CLP
  - CLP vs análisis manual de argumentos

- **Uso de CLP**
  - Obteniendo argumentos de línea de comandos
  - Tipos de argumentos (string, int, bit, time)
  - Valores por defecto
  - Validación de argumentos

- **Métodos CLP**
  - `get_arg_value()` - Obtener valor de argumento
  - `get_arg_values()` - Obtener múltiples valores
  - `get_arg_count()` - Obtener conteo de argumentos
  - `has_arg()` - Verificar si existe argumento

- **Patrones CLP**
  - Configuración de pruebas via línea de comandos
  - Control de depuración via línea de comandos
  - Control de simulación via línea de comandos
  - Mejores prácticas

### 2. Comparadores UVM

- **Resumen de Comparadores**
  - ¿Qué son los comparadores?
  - Propósito de los comparadores
  - Cuándo usar comparadores
  - Tipos de comparadores

- **Comparadores Integrados**
  - `uvm_in_order_comparator` - Comparación en orden
  - `uvm_algorithmic_comparator` - Comparación algorítmica
  - Características de los comparadores
  - Selección de comparadores

- **Comparador en Orden**
  - Comparación secuencial
  - Coincidencia de transacciones
  - Lógica de comparación
  - Reporte de errores

- **Comparador Algorítmico**
  - Algoritmos de comparación personalizados
  - Coincidencia flexible
  - Funciones de comparación
  - Casos de uso

- **Implementación de Comparadores**
  - Creando comparadores
  - Conectando comparadores
  - Configurando comparadores
  - Usando comparadores en scoreboards

### 3. Grabadores UVM

- **Resumen de Grabadores**
  - ¿Qué son los grabadores?
  - Propósito de los grabadores
  - Grabación de transacciones
  - Beneficios de la grabación

- **Tipos de Grabadores**
  - `uvm_text_recorder` - Grabación de texto
  - `uvm_tr_database` - Base de datos de transacciones
  - Formatos de grabación
  - Selección de grabadores

- **Uso de Grabadores**
  - Habilitando grabación
  - Grabando transacciones
  - Configuración de grabación
  - Análisis de grabación

- **Grabación de Transacciones**
  - Grabando ítems de secuencia
  - Grabando transacciones
  - Grabando temporización
  - Grabando relaciones

- **Implementación de Grabadores**
  - Creando grabadores
  - Conectando grabadores
  - Configurando grabadores
  - Analizando grabaciones

### 4. Pools UVM

- **Resumen de Pools de Objetos**
  - ¿Qué son los pools?
  - Propósito de los pools
  - Reutilización de objetos
  - Beneficios de rendimiento

- **Tipos de Pools**
  - `uvm_pool` - Pool genérico de objetos
  - Características de los pools
  - Operaciones de pools
  - Casos de uso de pools

- **Uso de Pools**
  - Creando pools
  - Agregando objetos a pools
  - Obteniendo objetos de pools
  - Gestión de pools

- **Implementación de Pools**
  - Creación de pools
  - Asignación de objetos
  - Desasignación de objetos
  - Limpieza de pools

- **Patrones de Pools**
  - Pooling de transacciones
  - Pooling de ítems de secuencia
  - Optimización de rendimiento
  - Gestión de memoria

### 5. Colas UVM

- **Resumen de Colas**
  - ¿Qué son las colas?
  - Propósito de las colas
  - Cola vs lista
  - Beneficios de las colas

- **Tipos de Colas**
  - `uvm_queue` - Cola genérica
  - Características de las colas
  - Operaciones de colas
  - Casos de uso de colas

- **Uso de Colas**
  - Creando colas
  - Agregando ítems a colas
  - Eliminando ítems de colas
  - Gestión de colas

- **Implementación de Colas**
  - Creación de colas
  - Operaciones de colas
  - Iteración de colas
  - Limpieza de colas

- **Patrones de Colas**
  - Colas de transacciones
  - Colas de scoreboard
  - Colas de buffer
  - Mejores prácticas de colas

### 6. Utilidades de Cadenas UVM

- **Resumen de Utilidades de Cadenas**
  - Necesidades de manipulación de cadenas
  - Utilidades de cadenas UVM
  - Beneficios de las utilidades
  - Cuándo usar utilidades

- **Operaciones de Cadenas**
  - Formateo de cadenas
  - Conversión de cadenas
  - Manipulación de cadenas
  - Comparación de cadenas

- **Métodos de Utilidades de Cadenas**
  - Operaciones comunes de cadenas
  - Funciones de formateo
  - Funciones de conversión
  - Patrones de utilidades

### 7. Utilidades Matemáticas UVM

- **Resumen de Utilidades Matemáticas**
  - Operaciones matemáticas
  - Utilidades matemáticas UVM
  - Beneficios de las utilidades
  - Cuándo usar utilidades

- **Operaciones Matemáticas**
  - Generación de números aleatorios
  - Funciones estadísticas
  - Utilidades matemáticas
  - Patrones matemáticos

- **Métodos de Utilidades Matemáticas**
  - Operaciones matemáticas comunes
  - Funciones aleatorias
  - Funciones estadísticas
  - Patrones de utilidades

### 8. Utilidades Aleatorias UVM

- **Resumen de Utilidades Aleatorias**
  - Generación de números aleatorios
  - Utilidades aleatorias UVM
  - Soporte de aleatorización
  - Patrones aleatorios

- **Operaciones Aleatorias**
  - Generación de valores aleatorios
  - Aleatorio restringido
  - Semillas aleatorias
  - Control aleatorio

- **Métodos de Utilidades Aleatorias**
  - Generación de números aleatorios
  - Gestión de semillas
  - Estado aleatorio
  - Patrones de utilidades

### 9. Primitivas UVM

- **Resumen de Primitivas**
  - ¿Qué son las primitivas?
  - Propósito de las primitivas
  - Tipos de primitivas
  - Casos de uso de primitivas

- **Tipos de Primitivas**
  - Primitivas comunes
  - Operaciones de primitivas
  - Características de primitivas
  - Selección de primitivas

- **Uso de Primitivas**
  - Usando primitivas
  - Patrones de primitivas
  - Mejores prácticas de primitivas
  - Ejemplos de primitivas

### 10. Macros UVM (Contexto Python)

- **Resumen de Macros**
  - Macros en SystemVerilog vs Python
  - Alternativas en Python
  - Funciones de utilidad
  - Decoradores auxiliares

- **Equivalencias en Python**
  - Alternativas a macros
  - Funciones de utilidad
  - Patrones de decoradores
  - Clases auxiliares

### 11. Integración de Utilidades

- **Usando Utilidades en Testbenches**
  - Cuándo usar utilidades
  - Selección de utilidades
  - Integración de utilidades
  - Patrones de utilidades

- **Mejores Prácticas de Utilidades**
  - Directrices de uso de utilidades
  - Consideraciones de rendimiento
  - Gestión de memoria
  - Organización de utilidades

- **Patrones Comunes de Utilidades**
  - Configuración via línea de comandos
  - Comparación de transacciones
  - Grabación de transacciones
  - Gestión de objetos

## Resultados de Aprendizaje

Al final de este módulo, deberías ser capaz de:

- Usar el Procesador de Línea de Comandos UVM
- Implementar y usar comparadores
- Usar grabadores para grabación de transacciones
- Usar pools para gestión de objetos
- Usar colas para estructuras de datos
- Usar utilidades de cadenas y matemáticas
- Usar utilidades aleatorias efectivamente
- Integrar utilidades en testbenches
- Aplicar mejores prácticas de utilidades
- Elegir utilidades apropiadas para tareas

## Casos de Prueba

### Caso de Prueba 8.1: Procesador de Línea de Comandos
**Objetivo**: Usar CLP para configuración de pruebas

**Temas**:
- Uso de CLP
- Análisis de argumentos
- Configuración via línea de comandos

#### Ejemplo 8.1: Procesador de Línea de Comandos (`module8/examples/clp/clp_example.py`)

**Qué demuestra:**
- **Análisis de Argumentos de Línea de Comandos**: Analizar argumentos de línea de comandos para configuración de pruebas
- **Uso de CLP**: Obtener argumentos usando sys.argv de Python (equivalente CLP en pyuvm)
- **Configuración de Pruebas**: Configurar comportamiento de pruebas via línea de comandos
- **Tipos de Argumentos**: Argumentos de tipo string, entero y booleano
- **Valores por Defecto**: Valores por defecto de argumentos

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --clp

# O directamente con argumentos
cd module8/examples/clp
python3 clp_example.py +test_mode=stress +debug_level=2 +num_transactions=20 +seed=12345
```

**Salida Esperada:**
```
============================================================
Command Line Processor Example Test
============================================================
Building CLP Environment
CLP Configuration:
  test_mode: stress
  debug_level: 2
  num_transactions: 20
  seed: 12345
Running CLP test
Running in stress mode
Stress test mode: Running extended test
Generating 20 transactions based on CLP configuration
```

**Conceptos Clave:**
- **CLP en pyuvm**: Usar sys.argv o argparse de Python en lugar de CLP UVM
- **Análisis de Argumentos**: Analizar formato +arg=value
- **Configuración de Pruebas**: Configurar pruebas via línea de comandos
- **Valores por Defecto**: Proporcionar valores por defecto para argumentos opcionales
- **Tipos de Argumentos**: Soporte para tipos string, int y boolean

### Caso de Prueba 8.2: Comparadores
**Objetivo**: Implementar comparador para scoreboard

**Temas**:
- Creación de comparadores
- Conexión de comparadores
- Lógica de comparación

#### Ejemplo 8.2: Comparadores (`module8/examples/comparators/comparator_example.py`)

**Qué demuestra:**
- **Comparador en Orden**: Comparar transacciones en orden de llegada
- **Comparador Algorítmico**: Algoritmos de comparación personalizados
- **Coincidencia de Transacciones**: Coincidir transacciones esperadas y reales
- **Lógica de Comparación**: Implementar funciones de comparación
- **Reporte de Errores**: Reportar discrepancias

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --comparators

# O directamente
cd module8/examples/comparators
python3 -c "import pyuvm; exec(open('comparator_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Comparator Example Test
============================================================
Building Comparator Environment
Building Comparator Scoreboard
[comparator] Expected: data=0x00, addr=0x0000, ts=0
[comparator] Actual: data=0x00, addr=0x0000, ts=0
[comparator] Match: data=0x00, addr=0x0000, ts=0
```

**Conceptos Clave:**
- **Comparador en Orden**: Comparación secuencial de transacciones
- **Comparador Algorítmico**: Algoritmos de coincidencia flexibles
- **Igualdad de Transacciones**: Implementar __eq__ para transacciones
- **Lógica de Comparación**: Funciones de comparación personalizadas
- **Integración con Scoreboard**: Usar comparadores en scoreboards

### Caso de Prueba 8.3: Grabadores
**Objetivo**: Grabar transacciones para análisis

**Temas**:
- Creación de grabadores
- Grabación de transacciones
- Análisis de grabaciones

#### Ejemplo 8.3: Grabadores (`module8/examples/recorders/recorder_example.py`)

**Qué demuestra:**
- **Grabador de Texto**: Grabar transacciones en archivo de texto
- **Grabador JSON**: Grabar transacciones en archivo JSON
- **Base de Datos de Transacciones**: Base de datos en memoria para transacciones
- **Formatos de Grabación**: Diferentes formatos de grabación
- **Análisis de Grabaciones**: Analizar transacciones grabadas

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --recorders

# O directamente
cd module8/examples/recorders
python3 -c "import pyuvm; exec(open('recorder_example.py').read())"
```

**Salida Esperada:**
```
============================================================
Recorder Example Test
============================================================
Building Recorder Environment
[text_recorder] Building Text Recorder (file: transactions.txt)
[json_recorder] Building JSON Recorder (file: transactions.json)
[database] Building Transaction Database
Running recorder test
[text_recorder] Recorded: id=0, data=0x00, addr=0x0000, ts=0
[json_recorder] Recorded: id=0, data=0x00, addr=0x0000, ts=0
[database] Stored: id=0, data=0x00, addr=0x0000, ts=0
```

**Conceptos Clave:**
- **Grabación de Texto**: Grabación simple en archivo de texto
- **Grabación JSON**: Grabación estructurada en JSON
- **Base de Datos de Transacciones**: Almacenamiento y consulta en memoria
- **Formatos de Grabación**: Elegir el formato apropiado
- **Análisis de Grabaciones**: Consultar y analizar grabaciones

### Caso de Prueba 8.4: Pools y Colas
**Objetivo**: Usar pools y colas para gestión de objetos

**Temas**:
- Creación y uso de pools
- Creación y uso de colas
- Gestión de objetos

#### Ejemplo 8.4: Pools (`module8/examples/pools/pool_example.py`)

**Qué demuestra:**
- **Pooling de Objetos**: Reutilizar objetos para rendimiento
- **Gestión de Pools**: Asignar y desasignar objetos
- **Reutilización de Transacciones**: Reutilizar objetos de transacción
- **Optimización de Rendimiento**: Reducir asignación de memoria
- **Estadísticas del Pool**: Rastrear uso del pool

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --pools

# O directamente
cd module8/examples/pools
python3 -c "import pyuvm; exec(open('pool_example.py').read())"
```

**Conceptos Clave:**
- **Pooling de Objetos**: Pre-asignar objetos para reutilización
- **Operaciones del Pool**: Operaciones get() y put()
- **Reseteo de Objetos**: Resetear objetos antes de reutilizar
- **Rendimiento**: Reducir sobrecarga de asignación
- **Tamaño del Pool**: Gestionar tamaño del pool

#### Ejemplo 8.5: Colas (`module8/examples/queues/queue_example.py`)

**Qué demuestra:**
- **Cola de Transacciones**: Cola para gestión de transacciones
- **Cola de Prioridad**: Ordenamiento basado en prioridad
- **Operaciones de Cola**: Operaciones push, pop, peek
- **Gestión de Colas**: Límites de tamaño y manejo de desbordamiento
- **Estadísticas de Cola**: Rastrear uso de la cola

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --queues

# O directamente
cd module8/examples/queues
python3 -c "import pyuvm; exec(open('queue_example.py').read())"
```

**Conceptos Clave:**
- **Operaciones de Cola**: Operaciones de cola FIFO
- **Cola de Prioridad**: Ordenar por prioridad
- **Tamaño de Cola**: Gestionar límites de tamaño de cola
- **Manejo de Desbordamiento**: Manejar desbordamiento de cola
- **Estadísticas de Cola**: Rastrear métricas de cola

#### Ejemplo 8.6: Utilidades de Cadenas (`module8/examples/string_utils/string_utils_example.py`)

**Qué demuestra:**
- **Formateo de Cadenas**: Formatear cadenas para logging y reportes
- **Conversión de Cadenas**: Convertir valores a cadenas hex, binarias
- **Manipulación de Cadenas**: Operaciones de rutas, manipulación de cadenas
- **Comparación de Cadenas**: Comparación sensible e insensible a mayúsculas
- **Representación de Transacciones como Cadena**: Formatear transacciones como cadenas

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --string-utils

# O directamente
cd module8/examples/string_utils
python3 -c "import pyuvm; exec(open('string_utils_example.py').read())"
```

**Conceptos Clave:**
- **Formateo de Cadenas**: Usar f-strings y format()
- **Conversión de Cadenas**: Funciones hex(), bin(), str()
- **Operaciones de Cadenas**: Operaciones split, join, replace
- **Manipulación de Rutas**: Operaciones de rutas de archivos
- **Formateo de Transacciones**: Formatear transacciones para visualización

#### Ejemplo 8.7: Utilidades Matemáticas (`module8/examples/math_utils/math_utils_example.py`)

**Qué demuestra:**
- **Generación de Números Aleatorios**: Generar valores aleatorios
- **Funciones Estadísticas**: Media, mediana, desviación estándar
- **Operaciones Matemáticas**: Operaciones aritméticas y bitwise
- **Manipulación de Bits**: Establecer, limpiar, verificar bits
- **Operaciones de Rango**: Cálculos de min, max, rango

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --math-utils

# O directamente
cd module8/examples/math_utils
python3 -c "import pyuvm; exec(open('math_utils_example.py').read())"
```

**Conceptos Clave:**
- **Generación Aleatoria**: random.randint(), random.random()
- **Estadísticas**: statistics.mean(), statistics.median()
- **Operaciones de Bits**: AND, OR, XOR, desplazamientos bitwise
- **Manipulación de Bits**: Establecer/limpiar/verificar bits individuales
- **Operaciones de Rango**: min(), max(), cálculos de rango

#### Ejemplo 8.8: Utilidades Aleatorias (`module8/examples/random_utils/random_utils_example.py`)

**Qué demuestra:**
- **Gestión de Semillas Aleatorias**: Establecer y gestionar semillas aleatorias
- **Generación de Valores Aleatorios**: Generar enteros y flotantes aleatorios
- **Aleatorización Restringida**: Aleatorizar con restricciones
- **Elección Aleatoria**: Elegir de opciones aleatoriamente
- **Mezcla Aleatoria**: Mezclar secuencias

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --random-utils

# O directamente
cd module8/examples/random_utils
python3 -c "import pyuvm; exec(open('random_utils_example.py').read())"
```

**Conceptos Clave:**
- **Gestión de Semillas**: random.seed() para reproducibilidad
- **Generación Aleatoria**: random.randint(), random.random()
- **Aleatorio Restringido**: Aleatorizar dentro de restricciones
- **Elección Aleatoria**: random.choice() para selección
- **Mezcla Aleatoria**: random.shuffle() para secuencias

#### Ejemplo 8.9: Integración de Utilidades (`module8/examples/integration/integration_example.py`)

**Qué demuestra:**
- **Múltiples Utilidades**: Integrar CLP, pool, comparador, grabador
- **Coordinación de Utilidades**: Usar utilidades juntas
- **Optimización de Rendimiento**: Combinar utilidades para eficiencia
- **Testbench Completo**: Testbench completo con utilidades
- **Mejores Prácticas**: Patrones de integración de utilidades

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --integration

# O directamente con argumentos
cd module8/examples/integration
python3 integration_example.py +num_transactions=20 +seed=42 +use_pool=true
```

**Conceptos Clave:**
- **Integración de Utilidades**: Combinar múltiples utilidades
- **Configuración CLP**: Configurar via línea de comandos
- **Uso de Pool**: Usar pool para reutilización de transacciones
- **Integración de Comparador**: Usar comparador en scoreboard
- **Integración de Grabador**: Grabar transacciones para análisis

#### Prueba: Prueba de Utilidades (`module8/tests/pyuvm_tests/test_utilities.py`)

**Qué demuestra:**
- Testbench completo usando utilidades
- Integración de utilidades en la práctica
- Patrones de calidad de producción

**Ejecución:**
```bash
# Usando script orquestador
./scripts/module8.sh --pyuvm-tests

# O manualmente
cd module8/tests/pyuvm_tests
make SIM=verilator TEST=test_utilities
```

## Ejercicios

1. **Procesador de Línea de Comandos**
   - Crear configuración basada en CLP
   - Analizar argumentos de línea de comandos
   - Usar argumentos en pruebas
   - **Ubicación**: Extiende `module8/examples/clp/clp_example.py`
   - **Pista**: Agrega más tipos de argumentos y validación

2. **Implementación de Comparador**
   - Crear comparador
   - Conectar a scoreboard
   - Probar lógica de comparación
   - **Ubicación**: Extiende `module8/examples/comparators/comparator_example.py`
   - **Pista**: Agrega funciones de comparación personalizadas y manejo de errores

3. **Uso de Grabadores**
   - Crear grabador
   - Grabar transacciones
   - Analizar grabaciones
   - **Ubicación**: Extiende `module8/examples/recorders/recorder_example.py`
   - **Pista**: Agrega funciones de consulta y capacidades de análisis

4. **Uso de Pools y Colas**
   - Crear pool para transacciones
   - Crear cola para scoreboard
   - Gestionar objetos eficientemente
   - **Ubicación**: Extiende `module8/examples/pools/pool_example.py` y `module8/examples/queues/queue_example.py`
   - **Pista**: Agrega estadísticas de pool y manejo de desbordamiento de cola

5. **Integración de Utilidades**
   - Integrar múltiples utilidades
   - Aplicar patrones de utilidades
   - Optimizar uso de utilidades
   - **Ubicación**: Extiende `module8/examples/integration/integration_example.py`
   - **Pista**: Agrega más utilidades y optimiza rendimiento

## Evaluación

- [ ] Puedo usar el Procesador de Línea de Comandos
- [ ] Puedo implementar y usar comparadores
- [ ] Puedo usar grabadores efectivamente
- [ ] Puedo usar pools para gestión de objetos
- [ ] Puedo usar colas para estructuras de datos
- [ ] Puedo usar utilidades de cadenas y matemáticas
- [ ] Puedo usar utilidades aleatorias
- [ ] Puedo integrar utilidades en testbenches
- [ ] Entiendo las mejores prácticas de utilidades
- [ ] Puedo elegir utilidades apropiadas

## Próximos Pasos

Después de completar este módulo, tienes cobertura completa de todas las secciones del estándar IEEE 1800.2. Ahora puedes:
- Aplicar todos los conceptos UVM a proyectos reales
- Usar utilidades efectivamente
- Construir testbenches de calidad de producción
- Continuar aprendiendo mediante la práctica

## Recursos Adicionales

- **Documentación de pyuvm**: https://pyuvm.readthedocs.io/
- **Guía de Usuario de UVM 1.2**: Accellera Systems Initiative
- **Estándar IEEE 1800.2**: Estándar IEEE para UVM
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

**Problema: Los argumentos CLP no se analizan correctamente**
```bash
# Solución: Verificar el formato del argumento
# Usar formato +arg=value
python3 example.py +test_mode=stress +num_transactions=20
```

**Problema: El comparador no coincide transacciones**
```bash
# Solución: Verificar la implementación de igualdad de transacciones
# Asegurar que el método __eq__ esté implementado correctamente
# Verificar que los campos de transacción coincidan
```

**Problema: El rendimiento del pool no mejora**
```bash
# Solución: Verificar el tamaño del pool
# Asegurar que los objetos se devuelvan al pool
# Verificar la tasa de reutilización del pool
```

**Problema: Desbordamiento de cola**
```bash
# Solución: Aumentar el tamaño de la cola
# Agregar manejo de desbordamiento
# Verificar la tasa de consumo de la cola
```

### Obteniendo Ayuda

- Revisa los comentarios del código de ejemplo para explicaciones detalladas
- Consulta el `module8/README.md` para la estructura del directorio
- Ejecuta ejemplos individualmente para entender cada utilidad
- Estudia el uso de CLP en `clp_example.py`
- Revisa las implementaciones de comparadores en `comparator_example.py`
- Consulta el uso de pools y colas en los ejemplos respectivos
- Revisa la integración de utilidades en `integration_example.py`

### Resumen de Ejemplos y Pruebas

**Ejemplos (ejemplos estructurales de pyuvm en `module8/examples/`):**
1. **Ejemplo 8.1: Procesador de Línea de Comandos** (`clp/`) - Uso de CLP para configuración de pruebas
2. **Ejemplo 8.2: Comparadores** (`comparators/`) - Comparación de transacciones
3. **Ejemplo 8.3: Grabadores** (`recorders/`) - Grabación de transacciones
4. **Ejemplo 8.4: Pools** (`pools/`) - Pooling de objetos para rendimiento
5. **Ejemplo 8.5: Colas** (`queues/`) - Estructuras de datos de cola
6. **Ejemplo 8.6: Utilidades de Cadenas** (`string_utils/`) - Manipulación de cadenas
7. **Ejemplo 8.7: Utilidades Matemáticas** (`math_utils/`) - Operaciones matemáticas
8. **Ejemplo 8.8: Utilidades Aleatorias** (`random_utils/`) - Generación de números aleatorios
9. **Ejemplo 8.9: Integración de Utilidades** (`integration/`) - Múltiples utilidades juntas

**Testbenches (pruebas ejecutables en `module8/tests/pyuvm_tests/`):**
1. **Prueba de Utilidades** (`test_utilities.py`) - Testbench completo usando utilidades

**Cobertura:**
- ✅ Uso del Procesador de Línea de Comandos
- ✅ Implementación y uso de comparadores
- ✅ Implementación y uso de grabadores
- ✅ Gestión de pools y colas
- ✅ Utilidades de cadenas, matemáticas y aleatorias
- ✅ Patrones de integración de utilidades
- ✅ Uso de utilidades de calidad de producción
