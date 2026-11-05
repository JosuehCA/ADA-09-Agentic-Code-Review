# AI Usage Log

### Entry 01 - Requirements Redefiniton
- **Stage**: Requirements.
- **Prompt/goal**: Redefine system's FR and NFR, looking for ambiguities.
- **AI Contribution**: 
      Suggested: 
        1. For FR-02, specifying whether a partial search is done over the whole full name and not just "the name".
        2. For FR-04, changing the word "tilde" to "diacritic", since a tilde in English is a different character from the Spanish tilde.
        3. For FR-06, proposing using a creation ID instead of date/time data to not have to rely on extra functionality.
        4. For NFR-02, stating that protection from injection attacks is out of scope (no in memory database).
- **Student Decision**: Accepted all observations except the third one, since that's part of the SPEC.md file. Still used that observation to change it to a more general phrasing. Refined requirements to be more accurate.
- **Impact**: REQUIREMENTS.md updated.

### Entry 02 - Specification Drafting
- **Stage**: Specification.
- **Prompt/goal**: Help define the SPEC.md contents based on the REQUIREMENTS.md file.
- **AI Contribution**: Provided a draft SPEC.md, cross referencing the REQUIREMENTS.md file and using a best practices context file as base of knowledge.
- **Student Decision**: Accepted. Stripped away samples from bullet points and changed some text formatting to match the desired view.
- **Impact**: SPEC.md updated.

### Entry 03 - Architecture Building
- **Stage**: Architecture.
- **Prompt/goal**: Build the architecture file and compare it against the SPEC.md file.
- **AI Contribution**: Provided a draft ARCHITECTURE.md, based on the SPEC.md file, and using a best practices context file as base of knowledge. Then suggested additional changes and the addition of a mermaid diagram.
- **Student Decision**: Accepted.
- **Impact**: ARCHITECTURE.md updated.

### Entry 04 - Tasks Definition
- **Stage**: Tasks.
- **Prompt/goal**: Build the unit tasks from the base of knowledge comprising REQUIREMENTS.md, SPEC.md, and ARCHITECTURE.md.
- **AI Contribution**: Provided the definition of 6 tasks regarding project setup -> domain model -> search logic -> validation and errors -> tests -> documentation.
- **Student Decision**: Accepted. Added README definition to T-06, and mock data definition for testing to T-05.
- **Impact**: TASKS.md updated.

### Entry 05 - Initial Readiness Audit (ADA-08)
- **Stage**: Audit / Assessment.
- **Prompt/goal**: Evaluate the ADA-05 repository against the 8 repository readiness dimensions and establish the BEFORE score.
- **AI Contribution**: Identified low readiness in Entry Point & Navigation (2/5), Agent Instructions (2/5), Automation & Guardrails (1/5), and Build/Run/Test (2/5), calculating an initial baseline score of 45/100.
- **Student Decision**: Validated the audit findings. Confirmed that while code quality was solid, the repo lacked operational discoverability and deterministic guardrails.
- **Impact**: Created `REPOSITORY_READINESS_AUDIT.md` (BEFORE section) and logged top 3 friction points.

### Entry 06 - AGENTS.md Contract Design (ADA-08)
- **Stage**: Agent Instructions / Contract Design.
- **Prompt/goal**: Upgrade `AGENTS.md` into an operational contract incorporating Read First ordering, Sources of Truth, Standard Commands, Change Rules, and Stop Conditions.
- **AI Contribution**: Proposed adding full CLI execution commands (`python -m src.cli`, `pytest -q`, `./scripts/verify_repo.sh`) and explicit Stop Conditions (conflict, destructive action, boundary change). Suggested separating tool adaptors into `GEMINI.md`.
- **Student Decision**: Accepted all recommendations and rejected any duplication of business requirements inside `AGENTS.md` to prevent split-brain drift.
- **Impact**: `AGENTS.md` and `GEMINI.md` authored and aligned with project constraints.

### Entry 07 - Deterministic Guardrail & Executable Knowledge (ADA-08)
- **Stage**: Guardrails & Verification Automation.
- **Prompt/goal**: Transform natural-language rules about essential files, test execution, and formatting into executable software checks.
- **AI Contribution**: Designed `scripts/check_repo_contract.py` to deterministically verify existence of required documentation and protected datasets (`data/customers.json`). Authored `scripts/verify_repo.sh` to execute tests, linters, and contract verification in a single command.
- **Student Decision**: Accepted. Configured `flake8` with `--max-line-length=130 --ignore=W391` to accommodate expressive unit test naming conventions without false positives.
- **Impact**: Created `scripts/verify_repo.sh` and `scripts/check_repo_contract.py`.

### Entry 08 - Discoverability & Implicit Knowledge Remediation (ADA-08)
- **Stage**: Navigation & Knowledge Externalization.
- **Prompt/goal**: Extract implicit tribal knowledge discovered during the BEFORE run and convert it into structured navigation.
- **AI Contribution**: Authored `results/implicit-knowledge.md` documenting test commands, protected seed fixtures, layer boundaries, and lint configs. Drafted `docs/REPO_MAP.md` mapping entry points, test suites, change guides, and protected paths.
- **Student Decision**: Accepted. Ensured `docs/REPO_MAP.md` explicitly lists `data/customers.json` under "Do Not Edit Directly".
- **Impact**: Created `docs/REPO_MAP.md` and `results/implicit-knowledge.md`.

### Entry 09 - AFTER Run Execution & Improvement Analysis (ADA-08)
- **Stage**: Evaluation & Comparative Verification.
- **Prompt/goal**: Execute the controlled task under the improved repository, compare BEFORE vs. AFTER metrics, and compute the delta.
- **AI Contribution**: Ran the verification pipeline `./scripts/verify_repo.sh`, demonstrating zero clarification questions, zero command failures, and deterministic PASS with score rising from 45/100 to 94/100 (+49 delta).
- **Student Decision**: Validated metrics against the rubric and authored comprehensive responses to the 13 reflection questions in `results/readiness-improvement-report.md`.
- **Impact**: Created `results/after-agent-run.md`, `results/readiness-improvement-report.md`, and finalized `REPOSITORY_READINESS_AUDIT.md`.

### Entry 10 - CI Pipeline & Shared Contract (ADA-08)
- **Stage**: Continuous Integration.
- **Prompt/goal**: Ensure verification is not dependent on local developer sessions by establishing a shared CI workflow.
- **AI Contribution**: Created `.github/workflows/verify.yml` that invokes `./scripts/verify_repo.sh` directly, establishing an identical verification contract between humans, coding agents, and CI runners.
- **Student Decision**: Accepted without modification.
- **Impact**: Created `.github/workflows/verify.yml`.
