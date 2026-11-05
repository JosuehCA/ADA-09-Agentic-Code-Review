# Tasks

## T-01 Project setup
- Goal: Initialize project directories, standard library layout, and test runner configuration.
- Files:
  - `src/__init__.py`
  - `tests/__init__.py`
  - `data/customers.json`
- Acceptance:
  - Project directory structure matches architectural components (`src/`, `tests/`, `data/`).
  - Test runner executes successfully in the workspace environment.
- Verification:
  - `pytest -v` runs without configuration errors.

## T-02 Domain model
- Goal: Implement the `Customer` domain model and `CustomerRepository` for local JSON data persistence.
- Files:
  - `src/models.py`
  - `src/repository.py`
  - `tests/test_repository.py`
- Acceptance:
  - `Customer` dataclass contains `id`, `first_name`, `last_name`, `email`, and computed `full_name` property.
  - `CustomerRepository` deserializes `data/customers.json` into a list of `Customer` instances.
  - Missing or malformed data files are handled gracefully with appropriate error handling.
  - Fulfills A-01, A-02, and Domain Model specification.
- Verification:
  - `pytest tests/test_repository.py -v` passes.

## T-03 Search logic
- Goal: Implement `CustomerSearchService` matching algorithms, Unicode normalization, multi-tier ranking, tie-breaking, and result capping.
- Files:
  - `src/search_service.py`
  - `tests/test_search_service.py`
- Acceptance:
  - AC-01: Matches query terms against `first_name`, `last_name`, `email`, and `full_name` (SR-01, FR-01, FR-02).
  - AC-03: Case-insensitive and diacritic-insensitive normalization using Unicode NFD decomposition (SR-02, FR-04).
  - AC-05: Exact matches strictly precede partial matches; ties are sorted alphabetically by `last_name`, then `first_name`, then `id` (SR-03, FR-06).
  - AC-08: Output is capped at a maximum of 20 customer records (SR-04, NFR-03).
- Verification:
  - `pytest tests/test_search_service.py -k "test_search or test_normalization or test_ranking or test_capping" -v` passes.

## T-04 Validation and errors
- Goal: Implement query validation rules, custom domain exceptions, and error messages.
- Files:
  - `src/search_service.py`
  - `tests/test_search_service.py`
- Acceptance:
  - AC-02: Queries with fewer than 3 non-whitespace characters raise `ValidationError` with EH-01 message (VR-01, FR-03).
  - AC-07: Queries with characters outside the whitelist raise `ValidationError` with EH-02 message (VR-02, NFR-02).
  - AC-04: Valid queries with no matches return an empty list without error, ready for EH-03 presentation (FR-05).
- Verification:
  - `pytest tests/test_search_service.py -k "test_validation or test_empty_state" -v` passes.

## T-05 Tests
- Goal: Implement the CLI presentation interface (`src/cli.py`), argument handling, exit codes, and end-to-end verification suites.
- Files:
  - `src/cli.py`
  - `tests/test_cli.py`
  - `tests/test_performance.py`
- Acceptance:
  - CLI formats and prints matching records displaying `id`, `first_name`, `last_name`, and `email` (SR-05).
  - CLI returns exit code `0` on successful query and on empty matches with EH-03 message (AC-04).
  - CLI returns exit code `2` and outputs EH-01 or EH-02 messages to stderr on validation failure (AC-02, AC-07).
  - AC-06: End-to-end query execution completes in ≤ 300 ms on a 1,000-record dynamically generated local dataset (NFR-01, TS-09).
- Verification:
  - `pytest -v` (full test suite passes).
  - Manual CLI execution verification (`python -m src.cli "<query>"`).

## T-06 Documentation
- Goal: Update traceability matrix, log AI interactions, prepare the agent execution report, and document project usage.
- Files:
  - `docs/traceability.md`
  - `AI_USAGE_LOG.md`
  - `results/agent-report.md`
  - `README.md`
- Acceptance:
  - `docs/traceability.md` connects Requirement → Acceptance Criterion → Task → Implementation → Test → Status PASS.
  - `AI_USAGE_LOG.md` contains entries covering all workflow stages.
  - `results/agent-report.md` documents tool version, task sequence, human reviews, test results, and final verification.
  - `README.md` documents environment setup, CLI invocation, and test execution commands.
  - All Definition of Done items from `AGENTS.md` are satisfied.
- Verification:
  - Human review of all documentation artifacts against Definition of Done checklist.
