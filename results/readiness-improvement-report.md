# Repository Readiness Improvement Report — ADA-08

## Executive Summary
This report analyzes the transformation of the Customer Search codebase from a traditional functional repository (ADA-05 baseline) into an **Agent-Ready Repository** (ADA-08). 

- **BEFORE Readiness Score**: 45 / 100
- **AFTER Readiness Score**: 94 / 100
- **Net Delta**: **+49 points** (exceeds the required +15 threshold and 80/100 target)

---

## Comparative Indicator Matrix

| Indicator | BEFORE | AFTER |
|---|---|---|
| **Clarification Questions** | 0 requested directly, but high implicit uncertainty requiring trial-and-error discovery. | 0 questions needed; 100% discoverable through repo contracts. |
| **Failed / Unknown Commands** | 2 failed commands (`ruff` not installed, unconfigured `flake8` failing on line lengths). | 0 failed commands; standard `./scripts/verify_repo.sh` executed cleanly. |
| **Incorrect Assumptions** | Assumed linter availability and test command locations without explicit guidance. | 0 incorrect assumptions; explicit commands in `AGENTS.md`. |
| **Out-of-Scope Files Modified** | 0 committed, but high risk of mutating `data/customers.json` or specs. | 0 out-of-scope modifications; protected paths strictly enforced. |
| **Validations Executed Correctly** | Partial; only `pytest` executed manually in terminal without repo integrity or linting checks. | Complete; tests, linter, and repository contract validated in one deterministic step. |
| **Final Result** | **PARTIAL** | **PASS** |
| **Discoverability** | Low; agent required file listing and exploration to discover entry points and tests. | High; `docs/REPO_MAP.md` and `AGENTS.md` provided immediate routing. |
| **Implicit Knowledge** | Documented in `results/implicit-knowledge.md` (test command, seed fixtures, layering, line lengths). | Fully explicit in `AGENTS.md`, `REPO_MAP.md`, and deterministic scripts. |
| **Clasificación de Mejoras** | Uncategorized ad-hoc documentation. | Categorized into Context, Navigation, Executable Knowledge, Guardrails, and CI Checks. |
| **CI / Shared Checks** | None; verification was isolated to developer machine. | Shared verification contract via `.github/workflows/verify.yml` and `./scripts/verify_repo.sh`. |

---

## Improvements Catalog

### Improvement I-01
- **Category**: Navigation
- **Problem**: The agent had to list directories and read arbitrary source files to understand the entry point and where tests were located.
- **Change**: Created `docs/REPO_MAP.md` detailing entry points, test mappings, change guides, and protected paths.
- **Evidence**: `docs/REPO_MAP.md` exists and is referenced directly in `AGENTS.md`.

### Improvement I-02
- **Category**: Context & Operational Contract
- **Problem**: `AGENTS.md` only had 25 lines of generic rules with no commands, stop conditions, or explicit sources of truth.
- **Change**: Upgraded `AGENTS.md` to include Read First sequence, Sources of Truth hierarchy, Repository Map, Standard Commands, Change Rules, Stop Conditions, and verifiable Definition of Done.
- **Evidence**: `AGENTS.md` now specifies exact commands: `pytest -q`, `flake8 src tests --max-line-length=130 --ignore=W391`, and `./scripts/verify_repo.sh`.

### Improvement I-03
- **Category**: Executable Knowledge
- **Problem**: Verification required knowing and running separate commands sequentially, with no guarantee that linting or contract rules were checked.
- **Change**: Created executable script `scripts/verify_repo.sh` bundling tests, linting, and repo contract validation into a single command with unified exit codes.
- **Evidence**: `./scripts/verify_repo.sh` executes with exit code 0 and logs `VERIFY_REPO: PASS`.

### Improvement I-04
- **Category**: Guardrail
- **Problem**: Critical files (`AGENTS.md`, `SPEC.md`, `REQUIREMENTS.md`, `docs/REPO_MAP.md`, `data/customers.json`) could be accidentally removed or renamed by an agent without immediate failure.
- **Change**: Created `scripts/check_repo_contract.py` which verifies presence of all contract files and directories deterministically.
- **Evidence**: `python scripts/check_repo_contract.py` outputs `REPO_CONTRACT: PASS`.

### Improvement I-05
- **Category**: CI Shared Check
- **Problem**: Verification was local and dependent on the agent's active session.
- **Change**: Added `.github/workflows/verify.yml` calling `./scripts/verify_repo.sh` to ensure humans, agents, and CI run the identical contract.
- **Evidence**: Workflow configuration file created in `.github/workflows/verify.yml`.

---

## Individual Reflection (Section 26)

### 1. ¿Cuál fue el principal obstáculo para el agente en la ejecución BEFORE?
El principal obstáculo fue la **falta de discoverability operativa**. Aunque el código funcional de ADA-05 era correcto y los tests existían, no había ningún comando unificado ni mapa del repositorio. El agente tuvo que inferir cómo ejecutar las pruebas, adivinar qué linter utilizar (intentando `ruff` que no estaba instalado) y descifrar la estructura navegando a ciegas entre directorios.

### 2. ¿Qué información tuvo que inferir el agente que un desarrollador experimentado ya conocía?
Tuvo que inferir:
1. Que el test runner era `pytest` ejecutado desde la raíz.
2. Que `data/customers.json` contiene el dataset semilla fijo y no debe modificarse.
3. Que los tests toleran nombres largos de funciones (hasta 130 caracteres) y que correr `flake8` con la longitud por defecto (79) producía falsos positivos.
4. El flujo arquitectónico estricto `CLI -> SearchService -> Repository`.

### 3. ¿Qué mejora produjo el mayor impacto y por qué?
El script unificado de verificación **`scripts/verify_repo.sh` junto con `scripts/check_repo_contract.py`**. Convirtió el proceso de validación de un ejercicio de suposiciones en un único comando determinista con código de salida binario (0 o 1). Esto reduce drásticamente la incertidumbre del agente y elimina la posibilidad de declarar una tarea terminada cuando faltan artefactos o el código viola el estilo.

### 4. ¿Qué información pertenece en AGENTS.md y qué información NO debería vivir ahí?
- **Pertenece en AGENTS.md**: Orden de lectura (`Read First`), jerarquía de fuentes de verdad, mapa general de rutas, comandos estándar reproducibles, reglas de cambio (límites y exclusiones), condiciones de parada (`Stop Conditions`) y Criterios de Aceptación/Definition of Done.
- **NO debería vivir ahí**: Requerimientos de negocio detallados (deben residir en `REQUIREMENTS.md`), especificaciones técnicas completas (pertenecen a `SPEC.md`), explicaciones arquitectónicas profundas (pertenecen a `ARCHITECTURE.md`) o código fuente. AGENTS.md debe ser un contrato operativo y de enrutamiento, no un monolito duplicado.

### 5. ¿Qué regla convertiste en software/hook/script en lugar de dejarla como instrucción?
La regla *"El repositorio debe mantener intactos sus documentos normativos, directorios esenciales y datos semilla"* se convirtió en el script **`scripts/check_repo_contract.py`**. Si un agente borra o renombra accidentalmente `SPEC.md`, `REPO_MAP.md` o `data/customers.json`, el script falla de inmediato con código de salida `1`, impidiendo que el Verification Gate pase.

### 6. ¿Qué diferencia observaste entre 'más contexto' y 'mejor contexto'?
- *Más contexto* significa saturar al agente volcando archivos gigantescos, prompts redundantes y especificaciones duplicadas en `AGENTS.md` o `README.md`, lo cual agota la ventana de contexto, incrementa el costo en tokens y genera alucinaciones o directrices contradictorias.
- *Mejor contexto* significa información estructurada, modular y accesible bajo demanda (`Progressive Disclosure`). `docs/REPO_MAP.md` le dice al agente exactamente a dónde ir sin necesidad de leer todo el código de antemano.

### 7. ¿Qué riesgo aparece cuando CLAUDE.md/GEMINI.md/copilot instructions duplican información del proyecto?
Aparece el riesgo de **divergencia y desincronización de fuentes de verdad** (Split-Brain). Si un requerimiento o comando cambia en `SPEC.md` o `AGENTS.md` pero no se actualiza en el archivo específico del asistente, los diferentes agentes implementarán comportamientos incompatibles o ejecutarán comandos obsoletos. Los archivos tool-specific deben actuar únicamente como adaptadores que apuntan a `AGENTS.md`.

### 8. ¿Qué checks comparten ahora el agente, el desarrollador humano y CI?
Comparten exactamente el mismo contrato ejecutable: **`./scripts/verify_repo.sh`**, el cual ejecuta de forma idéntica en los tres entornos:
1. Suite de pruebas unitarias e integración (`pytest -q`).
2. Linter estático de código (`flake8 src tests`).
3. Verificación de integridad de contrato de repositorio (`python scripts/check_repo_contract.py`).

### 9. ¿Qué parte del proceso sigue requiriendo decisión humana?
El **juicio de negocio y autorización de cambios**:
- Definir y autorizar el alcance de un `Change Request` o `TASK_UNDER_TEST`.
- Evaluar si un cambio en los requisitos justifica alterar la especificación.
- Decidir la resolución ante conflictos no contemplados (Stop Conditions).
- Autorizar la integración a producción (Human Gate).

### 10. ¿Qué evidencia demuestra que el AFTER es realmente mejor?
- Cero comandos fallidos o desconocidos.
- Cero preguntas de clarificación requeridas.
- Tiempo y pasos de navegación reducidos a lecturas directas orientadas por `docs/REPO_MAP.md`.
- Verificación con un solo comando determinista (`./scripts/verify_repo.sh`) con resultado PASS reproducible en terminal y en CI.
- Score de readiness incrementado de 45 a 94 (+49 puntos).

### 11. ¿Qué mejora realizada para el agente también beneficia a un desarrollador que entra por primera vez al proyecto?
`docs/REPO_MAP.md` y `scripts/verify_repo.sh`. Un nuevo ingeniero de software a menudo pasa horas descubriendo qué comando correr para validar o cuál archivo es el entry point. Con `REPO_MAP.md` y `verify_repo.sh`, el onboarding se vuelve instantáneo tanto para humanos como para IAs.

### 12. ¿Qué variable no controlada podría afectar tu comparación BEFORE/AFTER?
La variabilidad estocástica y temperatura inherente del modelo de lenguaje, o si se ejecutaran las pruebas con distintas versiones de Python o librerías del entorno. Para controlar esto, se mantuvo idéntico el modelo (Gemini 3.8 Flash), la máquina (macOS Sonoma, Python 3.12.7) y el baseline funcional (`ada08-baseline`).

### 13. ¿Qué elementos de este ADA conservarás como base para tu proyecto final?
1. La estructura de **`AGENTS.md` como contrato operativo** con comandos estandarizados y condiciones de parada.
2. El archivo de navegación **`docs/REPO_MAP.md`** con la guía de cambios por capa.
3. El script de verificación única **`scripts/verify_repo.sh`** compartido con CI.
4. El script determinista de contrato **`scripts/check_repo_contract.py`** como guardrail infalible.

