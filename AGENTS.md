# AGENTS.md

## Read First
1. REQUIREMENTS.md
2. SPEC.md
3. ARCHITECTURE.md
4. TASKS.md
5. docs/REPO_MAP.md

## Sources of Truth
- Requirements live only in `REQUIREMENTS.md`.
- Verifiable behavior lives in `SPEC.md`.
- Architectural boundaries and layering live in `ARCHITECTURE.md`.
- Do not change requirements/spec merely to make tests pass.

## Repository Map
- `src/` - Implementation (CLI presentation, search service, repository, models).
- `tests/` - Automated pytest suite (search service, CLI, repository, performance).
- `docs/` - Architecture, repository map, and traceability matrix.
- `scripts/` - Deterministic verification scripts and repository contract checks.
- `results/` - Audit records, run logs, and verification evidence.
- `data/` - Static fixture datasets (`customers.json`).

## Standard Commands
- Install: `pip install pytest flake8`
- Run: `python -m src.cli "<query>"`
- Test: `pytest -q`
- Lint: `flake8 src tests --max-line-length=130 --ignore=W391`
- Verify: `./scripts/verify_repo.sh`

## Change Rules
- Keep changes scoped strictly to the requested task.
- Do not weaken or delete existing tests.
- Do not introduce new dependencies without justification.
- Do not modify `data/customers.json` or secrets.
- Always preserve architecture boundaries (`CLI -> SearchService -> Repository`).

## Stop Conditions
Stop and ask for human input when:
- Requirements or specifications conflict.
- A destructive action is required.
- An architecture boundary must change.
- A required external system or command is unavailable.

## Definition of Done
- Relevant automated tests pass (`pytest -q`).
- Acceptance criteria are covered by tests.
- `./scripts/verify_repo.sh` exits with code 0.
- No unrelated or protected files are modified.
- Documentation and traceability reflect final behavior.
