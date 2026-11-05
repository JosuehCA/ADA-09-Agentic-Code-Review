# Implicit Knowledge Found

## IK-01
What:
The canonical test command is `pytest` and tests reside in `tests/`.

How was it discovered:
By inspecting directory structure and testing command availability in the shell.

Should this remain implicit?
NO

Where should it become explicit?
`AGENTS.md` (Standard Commands) and `scripts/verify_repo.sh`.

## IK-02
What:
`data/customers.json` is a protected baseline dataset fixture and must not be mutated or overwritten during feature development.

How was it discovered:
By inspecting `tests/test_repository.py` and finding hardcoded assertions expecting 25 baseline customers.

Risk:
An agent implementing an edge case might alter or add records directly to `data/customers.json`, causing regressions in existing repository tests.

Remediation:
Document as a protected path in `AGENTS.md` and `docs/REPO_MAP.md`, and validate its presence in `scripts/check_repo_contract.py`.

## IK-03
What:
Layering strictly flows Presentation (`src/cli.py`) -> Domain Service (`src/search_service.py`) -> Persistence (`src/repository.py`). CLI must never call `CustomerRepository` directly or implement ranking logic.

How was it discovered:
By reading `ARCHITECTURE.md`.

Risk:
An agent might bypass the service layer for quick queries or place validation/ranking logic directly into `cli.py`.

Remediation:
`docs/REPO_MAP.md` (Architecture Boundaries & Change Guide) + `AGENTS.md`.

## IK-04
What:
Linting standard for Python files accepts up to 130 character line length for descriptive test function names, configured via `ruff.toml` with `line-length = 130` and executed with `ruff check .`.

How was it discovered:
By running default linters and observing standard 79/88-character limits failing on long test names.

Should this remain implicit?
NO

Where should it become explicit?
`ruff.toml`, `scripts/verify_repo.sh`, and `AGENTS.md`.

