# Módulo 0: Instalación y Configuración

**Objetivo**: Configurar el entorno de desarrollo y verificar la instalación

## Resumen

Este módulo cubre la configuración completa de tu entorno de verificación, incluyendo todas las herramientas y dependencias requeridas. Al final de este módulo, deberías tener un entorno funcional capaz de ejecutar testbenches de pyuvm.

### Scripts de Instalación Automatizados

Este proyecto incluye scripts de instalación automatizados para simplificar el proceso de configuración. Puedes usar estos scripts para instalar todas las herramientas automáticamente, o instalarlas manualmente usando las instrucciones en cada sección.

**Inicio Rápido (Instalación Todo-en-Uno)**:
```bash
# Hacer scripts ejecutables (Linux/Mac/WSL)
chmod +x scripts/*.sh

# Instalar todas las herramientas con configuración por defecto
./scripts/module0.sh

# O instalar con opciones personalizadas
./scripts/module0.sh --verilator-mode submodule --cocotb-mode pip --pyuvm-mode pip
```

**Instalación de Herramientas Individuales**:
- Verilator: `./scripts/install_verilator.sh [--from-submodule|--system|--source]`
- cocotb: `./scripts/install_cocotb.sh [--pip|--from-submodule] [--venv DIR]`
- pyuvm: `./scripts/install_pyuvm.sh [--pip|--from-submodule] [--venv DIR]`

**Desinstalación**:
- Desinstalar todo: Usa los scripts de desinstalación individuales o elimina las herramientas manualmente
- Verilator: `./scripts/uninstall_verilator.sh [--system] [--keep-submodule]`
- cocotb: `./scripts/uninstall_cocotb.sh [--venv DIR] [--keep-submodule]`
- pyuvm: `./scripts/uninstall_pyuvm.sh [--venv DIR] [--keep-submodule]`

Para uso detallado de cada script, consulta las secciones de instalación correspondientes a continuación.

## Temas Cubiertos

### 1. Requisitos del Sistema y Prerrequisitos

- **Soporte de Sistema Operativo**
  - Linux (Ubuntu/Debian, CentOS/RHEL, Fedora)
  - macOS (Intel y Apple Silicon)
  - Windows (WSL2 recomendado)
  
- **Requisitos de Hardware**
  - Mínimo 4GB RAM (8GB+ recomendado)
  - 10GB de espacio libre en disco
  - Procesador multi-núcleo recomendado

- **Prerrequisitos de Software**
  - Python 3.8+ (3.10+ recomendado)
  - Git
  - Compilador C/C++ (GCC, Clang o MSVC)
  - Sistema de compilación Make o Ninja

### 2. Configuración del Entorno Python

- **Instalación de Python**
  - Instalando Python 3.10+ en Linux
  - Instalando Python 3.10+ en macOS
  - Instalando Python 3.10+ en Windows/WSL2
  - Verificando la instalación de Python

- **Gestión de Entornos Virtuales**
  - Usando `venv` (integrado en Python)
  - Usando `conda` (Anaconda/Miniconda)
  - Usando `uv` o `rye` (gestores de paquetes Python modernos)
  - Mejores prácticas para entornos virtuales

- **Gestión de Paquetes**
  - Conceptos básicos de pip
  - Gestión de requirements.txt
  - Resolución de dependencias

### 3. Instalación de Verilator

- **¿Qué es Verilator?**
  - Simulador Verilog/SystemVerilog de código abierto
  - Compilación y simulación rápidas
  - Integración con cocotb

- **Instalación Automatizada (Recomendada)**
  - **Usando el script de instalación**:
    ```bash
    # Instalar desde git submodule (por defecto - compila desde fuente)
    ./scripts/install_verilator.sh --from-submodule
    
    # Instalar desde el gestor de paquetes del sistema
    ./scripts/install_verilator.sh --system
    
    # Compilar desde fuente (clona si el submodule no existe)
    ./scripts/install_verilator.sh --source
    ```
  - El script automáticamente:
    - Verifica instalaciones existentes
    - Instala dependencias del sistema (herramientas de compilación, librerías)
    - Configura el git submodule en `tools/verilator/`
    - Compila e instala Verilator
    - Verifica la instalación

- **Métodos de Instalación Manual**
  - **Instalación en Linux**
    - Ubuntu/Debian: `sudo apt-get install verilator`
    - CentOS/RHEL: `sudo yum install verilator` o `sudo dnf install verilator`
    - Fedora: `sudo dnf install verilator`
    - Compilando desde fuente (últimas características)
  
  - **Instalación en macOS**
    - Instalación con Homebrew: `brew install verilator`
    - Instalación con MacPorts (alternativa)
    - Compilando desde fuente
  
  - **Instalación en Windows/WSL2**
    - Instalando en WSL2 Ubuntu: `sudo apt-get install verilator`
    - Compilando desde fuente en WSL2
    - Verificando la instalación

- **Desinstalación**
  ```bash
  # Desinstalar y eliminar submodule
  ./scripts/uninstall_verilator.sh
  
  # Desinstalar pero mantener git submodule
  ./scripts/uninstall_verilator.sh --keep-submodule
  
  # Desinstalar también el paquete del sistema (si se instaló mediante gestor de paquetes)
  ./scripts/uninstall_verilator.sh --system
  ```

- **Pasos de Verificación**
  - Verificar versión de Verilator: `verilator --version`
  - Ejecutar prueba simple de Verilator
  - Verificar que la compilación funciona

### 4. Instalación y Verificación de cocotb

- **¿Qué es cocotb?**
  - Framework de testbench basado en corrutinas
  - Testbenches en Python para hardware
  - Capa de abstracción del simulador

- **Instalación Automatizada (Recomendada)**
  - **Usando el script de instalación**:
    ```bash
    # Instalar via pip en entorno virtual (por defecto)
    ./scripts/install_cocotb.sh --pip --venv .venv
    
    # Instalar desde git submodule (modo desarrollo/editable)
    ./scripts/install_cocotb.sh --from-submodule --editable --venv .venv
    
    # Instalar en Python del sistema (no recomendado)
    ./scripts/install_cocotb.sh --pip --no-venv
    ```
  - El script automáticamente:
    - Crea/usa entorno virtual (por defecto: `.venv`)
    - Configura git submodule en `tools/cocotb/` (si se usa modo submodule)
    - Instala dependencias
    - Instala cocotb (via pip o desde fuente)
    - Verifica la instalación

- **Métodos de Instalación Manual**
  - **Instalación con pip (recomendada)**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    pip install cocotb
    ```
  - Instalación de desarrollo desde fuente
  - Fijación de versión para estabilidad: `pip install cocotb==2.0.0`

- **Desinstalación**
  ```bash
  # Desinstalar del entorno virtual (por defecto)
  ./scripts/uninstall_cocotb.sh --venv .venv
  
  # Desinstalar de Python del sistema
  ./scripts/uninstall_cocotb.sh --no-venv
  
  # Mantener git submodule
  ./scripts/uninstall_cocotb.sh --keep-submodule
  ```

- **Configuración del Simulador**
  - Configuración de Verilator
  - Configuración de Icarus Verilog (alternativa)
  - Configuración de ModelSim/QuestaSim (si está disponible)
  - Configuración de GHDL (soporte VHDL)

- **Variables de Entorno**
  - `COCOTB_REDUCED_LOG_FMT`
  - `MODULE` y `TESTCASE`
  - `SIM` para selección de simulador

- **Pasos de Verificación**
  - Importar cocotb exitosamente: `python3 -c "import cocotb; print(cocotb.__version__)"`
  - Ejecutar prueba simple de cocotb
  - Verificar integración con el simulador

### 5. Instalación y Verificación de pyuvm

- **¿Qué es pyuvm?**
  - Implementación en Python de UVM 1.2
  - Funciona con cocotb
  - Soporte completo de metodología UVM

- **Instalación Automatizada (Recomendada)**
  - **Usando el script de instalación**:
    ```bash
    # Instalar via pip en entorno virtual (por defecto)
    ./scripts/install_pyuvm.sh --pip --venv .venv
    
    # Instalar desde git submodule (modo desarrollo/editable)
    ./scripts/install_pyuvm.sh --from-submodule --editable --venv .venv
    
    # Instalar en Python del sistema (no recomendado)
    ./scripts/install_pyuvm.sh --pip --no-venv
    ```
  - El script automáticamente:
    - Crea/usa entorno virtual (por defecto: `.venv`)
    - Configura git submodule en `tools/pyuvm/` (si se usa modo submodule)
    - Instala dependencias
    - Instala pyuvm (via pip o desde fuente)
    - Verifica la instalación

- **Métodos de Instalación Manual**
  - **Instalación con pip**:
    ```bash
    source .venv/bin/activate  # Activar entorno virtual
    pip install pyuvm
    ```
  - Instalación desde fuente (desarrollo)
  - Selección y compatibilidad de versiones: `pip install pyuvm==2.9.0`

- **Desinstalación**
  ```bash
  # Desinstalar del entorno virtual (por defecto)
  ./scripts/uninstall_pyuvm.sh --venv .venv
    
  # Desinstalar de Python del sistema
  ./scripts/uninstall_pyuvm.sh --no-venv
    
  # Mantener git submodule
  ./scripts/uninstall_pyuvm.sh --keep-submodule
  ```

- **Dependencias**
  - Entendiendo las dependencias de pyuvm
  - Resolviendo conflictos de dependencias
  - Actualizando pyuvm

- **Pasos de Verificación**
  - Importar pyuvm exitosamente: `python3 -c "import pyuvm; print(pyuvm.__version__)"`
  - Verificar versión de pyuvm
  - Ejecutar prueba simple de pyuvm
  - Verificar clases UVM disponibles

### 6. Configuración del IDE

- **IDEs Recomendados**
  - VS Code con extensión Python
  - PyCharm (Community o Professional)
  - Vim/Neovim con LSP
  - Emacs con soporte Python

- **Configuración de VS Code**
  - Configuración de la extensión Python
  - Configuración de Pylance/Pyright
  - Configuración de depuración
  - Configuración de ejecutor de tareas para simulaciones
  - Recomendaciones de extensiones

- **Configuración de PyCharm**
  - Configuración del intérprete Python
  - Configuración del entorno virtual
  - Configuraciones de ejecución para pruebas
  - Configuración de depuración

- **Configuración del Editor**
  - Formateo Python (Black, Ruff)
  - Linting (pylint, flake8, ruff)
  - Verificación de tipos (mypy, pyright)
  - Formateo de código al guardar

### 7. Configuración de la Estructura del Proyecto

- **Estructura de Directorios**
  - Organización del código fuente
  - Estructura de directorios de pruebas
  - Organización del DUT (Design Under Test)
  - Archivos de configuración
  - Directorio `tools/` para git submodules (Verilator, cocotb, pyuvm)

- **Gestión de Git Submodules**
  - Las herramientas se gestionan como git submodules en el directorio `tools/`
  - Inicializar submodules: `./scripts/init_submodules.sh` o `git submodule update --init --recursive`
  - Actualizar submodules: `./scripts/update_submodules.sh` o `git submodule update --remote`
  - Agregar nuevo submodule: `./scripts/add_submodule.sh <repo_url> <path>`
  - Eliminar submodule: `./scripts/remove_submodule.sh <path>`

- **Makefile/Configuración**
  - Makefile simple para ejecutar pruebas
  - Configuración de pytest
  - Configuración de Makefile de cocotb
  - Gestión de variables de entorno

- **Control de Versiones**
  - Inicialización de Git
  - .gitignore para Python y simulación (incluir `.venv/`, `__pycache__/`, artefactos de compilación)
  - Estructura del commit inicial
  - Git submodules en archivo `.gitmodules`

### 8. Primera Prueba de Verificación "Hello World"

- **Prerrequisitos**
  - Asegurar que todas las herramientas estén instaladas: `./scripts/module0.sh --verify-only`
  - Activar entorno virtual: `source .venv/bin/activate` (si usas venv)
  - Verificar que las herramientas sean accesibles

- **Creación de DUT Simple**
  - Módulo Verilog básico (ej. puerta AND)
  - Estructura simple de testbench

- **Prueba cocotb**
  - Estructura básica de prueba cocotb
  - Generación de reloj
  - Lectura y escritura de señales
  - Ejecutar la prueba (requiere Verilator y cocotb instalados)

- **Prueba pyuvm**
  - Primera clase de prueba UVM
  - Fases UVM básicas
  - Ejecutar prueba pyuvm (requiere cocotb y pyuvm instalados)
  - Entendiendo la salida

### 9. Solución de Problemas Comunes

- **Problemas de Python**
  - Conflictos de versión de Python
  - Problemas de activación del entorno virtual
  - Fallos de instalación de paquetes

- **Problemas de Verilator**
  - Errores de compilación
  - Dependencias faltantes
  - Compatibilidad de versiones
  - Problemas de ruta

- **Problemas de cocotb**
  - Simulador no encontrado
  - Errores de importación
  - Problemas de variables de entorno
  - Problemas de carga de módulos

- **Problemas de pyuvm**
  - Errores de importación
  - Compatibilidad de versiones
  - Conflictos de dependencias

- **Problemas del IDE**
  - Intérprete Python no encontrado
  - Problemas de resolución de importaciones
  - Depuración no funciona

### 10. Lista de Verificación

- [ ] Python 3.10+ instalado y funcionando
- [ ] Entorno virtual creado y activado (o usar `./scripts/module0.sh` que lo crea automáticamente)
- [ ] Verilator instalado y verificado
  - Usando script: `./scripts/install_verilator.sh --from-submodule`
  - Verificar: `verilator --version`
- [ ] cocotb instalado y verificado
  - Usando script: `./scripts/install_cocotb.sh --pip --venv .venv`
  - Verificar: `python3 -c "import cocotb; print(cocotb.__version__)"`
- [ ] pyuvm instalado y verificado
  - Usando script: `./scripts/install_pyuvm.sh --pip --venv .venv`
  - Verificar: `python3 -c "import pyuvm; print(pyuvm.__version__)"`
- [ ] Todas las herramientas verificadas juntas: `./scripts/module0.sh --verify-only`
- [ ] IDE configurado y funcionando
- [ ] Primera prueba ejecutada exitosamente
- [ ] Puedo crear y ejecutar un testbench simple
- [ ] Entiendo la estructura básica del proyecto
- [ ] Sé cómo obtener ayuda cuando me quedo atascado

## Resultados de Aprendizaje

Al final de este módulo, deberías ser capaz de:

- Instalar y configurar todas las herramientas requeridas
- Configurar un entorno virtual Python
- Instalar y verificar Verilator
- Instalar y verificar cocotb
- Instalar y verificar pyuvm
- Configurar tu IDE para trabajo de verificación
- Crear una estructura básica de proyecto
- Ejecutar una prueba de verificación simple
- Solucionar problemas comunes de instalación

## Ejercicios

1. **Verificación de Instalación**
   - Usa `./scripts/module0.sh --verify-only` para verificar todas las instalaciones
   - O verifica cada herramienta independientemente:
     - Verilator: `verilator --version`
     - cocotb: `python3 -c "import cocotb; print(cocotb.__version__)"`
     - pyuvm: `python3 -c "import pyuvm; print(pyuvm.__version__)"`
   - Documenta cualquier problema encontrado

2. **Configuración del Entorno**
   - Opción A (Automatizada): Ejecuta `./scripts/module0.sh` para instalar todo
   - Opción B (Manual):
     - Crea un entorno virtual: `python3 -m venv .venv`
     - Actívalo: `source .venv/bin/activate`
     - Instala las herramientas individualmente usando los scripts o manualmente
   - Crea un archivo requirements.txt con los paquetes instalados:
     ```bash
     source .venv/bin/activate
     pip freeze > requirements.txt
     ```

3. **Primera Prueba**
   - Crea un módulo Verilog simple
   - Escribe una prueba cocotb para él
   - Ejecuta la prueba exitosamente

4. **Configuración del IDE**
   - Configura tu IDE preferido
   - Configura el intérprete Python para usar `.venv/bin/python`
   - Prueba la funcionalidad de depuración

5. **Estructura del Proyecto**
   - Crea una estructura de proyecto bien organizada
   - Configura control de versiones (los git submodules para herramientas ya están gestionados)
   - Crea documentación inicial
   - Entiende la estructura del directorio `tools/` (git submodules)

## Evaluación

- [ ] Puedo instalar todas las herramientas requeridas independientemente
- [ ] Puedo configurar un entorno virtual Python
- [ ] Puedo verificar la instalación de Verilator
- [ ] Puedo verificar la instalación de cocotb
- [ ] Puedo verificar la instalación de pyuvm
- [ ] Puedo configurar el IDE para trabajo de verificación
- [ ] Puedo crear y ejecutar una prueba simple
- [ ] Puedo solucionar problemas comunes
- [ ] Entiendo las mejores prácticas de estructura de proyecto

## Próximos Pasos

Después de completar este módulo, continúa con [Módulo 1: Fundamentos de Python y Verificación](MODULE1.md) para aprender los conceptos fundamentales necesarios para la verificación.

## Recursos Adicionales

- **Scripts de Instalación**:
  - Todos los scripts están en el directorio `scripts/`
  - Ejecuta `./scripts/module0.sh --help` para uso detallado
  - Ayuda de script individual: `./scripts/install_<tool>.sh --help`
  
- **Documentación de Verilator**: https://verilator.org/
- **Guía de Instalación de cocotb**: https://docs.cocotb.org/en/stable/install.html
- **Guía de Instalación de pyuvm**: https://pyuvm.readthedocs.io/en/latest/installation.html
- **Entornos Virtuales Python**: https://docs.python.org/3/tutorial/venv.html
- **Git Submodules**: https://git-scm.com/book/en/v2/Git-Tools-Submodules
