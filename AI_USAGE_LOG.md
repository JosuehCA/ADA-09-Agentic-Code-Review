### Entry 01 - Initial Readiness Audit
- **Stage**: Audit / Assessment.
- **Prompt/goal**: Evaluate the ADA-05 repository against the 8 repository readiness dimensions and establish the BEFORE score.
- **AI Contribution**: Identified low readiness in Entry Point & Navigation (2/5), Agent Instructions (2/5), Automation & Guardrails (1/5), and Build/Run/Test (2/5), calculating an initial baseline score of 45/100.
- **Student Decision**: Validated the audit findings. Confirmed that while code quality was solid, the repo lacked operational discoverability and deterministic guardrails.
- **Impact**: Created `REPOSITORY_READINESS_AUDIT.md` (BEFORE section) and logged top 3 friction points.

### Entry 02 - AGENTS.md Contract Design
- **Stage**: Agent Instructions / Contract Design.
- **Prompt/goal**: Upgrade `AGENTS.md` into an operational contract incorporating Read First ordering, Sources of Truth, Standard Commands, Change Rules, and Stop Conditions.
- **AI Contribution**: Proposed adding full CLI execution commands (`python -m src.cli`, `pytest -q`, `./scripts/verify_repo.sh`) and explicit Stop Conditions (conflict, destructive action, boundary change). Suggested separating tool adaptors into `GEMINI.md`.
- **Student Decision**: Accepted all recommendations and rejected any duplication of business requirements inside `AGENTS.md` to prevent split-brain drift.
- **Impact**: `AGENTS.md` and `GEMINI.md` authored and aligned with project constraints.

### Entry 03 - Deterministic Guardrail & Executable Knowledge
- **Stage**: Guardrails & Verification Automation.
- **Prompt/goal**: Transform natural-language rules about essential files, test execution, and formatting into executable software checks.
- **AI Contribution**: Designed `scripts/check_repo_contract.py` to deterministically verify existence of required documentation and protected datasets (`data/customers.json`). Authored `scripts/verify_repo.sh` to execute tests, linters, and contract verification in a single command.
- **Student Decision**: Accepted. Standardized on `ruff check .` with project-level `ruff.toml` (line-length = 130) to provide fast, modern deterministic linting matching the course specification example.
- **Impact**: Created `scripts/verify_repo.sh` and `scripts/check_repo_contract.py`.

### Entry 04 - Discoverability & Implicit Knowledge Remediation
- **Stage**: Navigation & Knowledge Externalization.
- **Prompt/goal**: Extract implicit tribal knowledge discovered during the BEFORE run and convert it into structured navigation.
- **AI Contribution**: Authored `results/implicit-knowledge.md` documenting test commands, protected seed fixtures, layer boundaries, and lint configs. Drafted `docs/REPO_MAP.md` mapping entry points, test suites, change guides, and protected paths.
- **Student Decision**: Accepted. Ensured `docs/REPO_MAP.md` explicitly lists `data/customers.json` under "Do Not Edit Directly".
- **Impact**: Created `docs/REPO_MAP.md` and `results/implicit-knowledge.md`.

### Entry 05 - AFTER Run Execution & Improvement Analysis
- **Stage**: Evaluation & Comparative Verification.
- **Prompt/goal**: Execute the controlled task under the improved repository, compare BEFORE vs. AFTER metrics, and compute the delta.
- **AI Contribution**: Ran the verification pipeline `./scripts/verify_repo.sh`, demonstrating zero clarification questions, zero command failures, and deterministic PASS with score rising from 45/100 to 94/100 (+49 delta).
- **Student Decision**: Validated metrics against the rubric and authored comprehensive responses to the 13 reflection questions in `results/readiness-improvement-report.md`.
- **Impact**: Created `results/after-agent-run.md`, `results/readiness-improvement-report.md`, and finalized `REPOSITORY_READINESS_AUDIT.md`.

### Entry 06 - CI Pipeline & Shared Contract
- **Stage**: Continuous Integration.
- **Prompt/goal**: Ensure verification is not dependent on local developer sessions by establishing a shared CI workflow.
- **AI Contribution**: Created `.github/workflows/verify.yml` that invokes `./scripts/verify_repo.sh` directly, establishing an identical verification contract between humans, coding agents, and CI runners.
- **Student Decision**: Accepted without modification.
- **Impact**: Created `.github/workflows/verify.yml`.
