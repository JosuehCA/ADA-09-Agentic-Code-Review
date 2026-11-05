# Agent Report

## Agent / Version
Antigravity IDE (Gemini 3.8 Flash)

## Initial Context
REQUIREMENTS.md, SPEC.md, ARCHITECTURE.md, TASKS.md, and AGENTS.md

## Task Sequence

### T-01: Project Setup
- **What the agent did**: Initialized standard package layout with `src/__init__.py`, `tests/__init__.py`, and created `data/customers.json` containing 25 valid customer records adhering to the domain model and constraints (A-01, A-02, A-03).
- **Human review**: Reviewed changes, verified clean directory structure, and committed to git (`572fe3f`).
- **Tests**: Ran `pytest -v` confirming test runner execution without configuration errors. Verified JSON deserialization and imports via python script.

### T-02: Domain Model & Persistence
- **What the agent did**: Implemented immutable `Customer` dataclass with computed `full_name` property in `src/models.py`. Implemented `CustomerRepositoryInterface`, `RepositoryError`, and `CustomerRepository` in `src/repository.py` for deserializing `data/customers.json` with robust error handling for missing/malformed files and schema anomalies.
- **Human review**: Reviewed implementation, confirmed domain contract conformance, and committed to git (`c299d0c`).
- **Tests**: Authored and passed 9 tests in `tests/test_repository.py` covering model immutability, fields, computed property, unique constraints, missing files, and malformed JSON.

### T-03: Search Logic
- **What the agent did**: Implemented `CustomerSearchService` in `src/search_service.py` including Unicode NFD diacritics stripping and case-folding normalization (`normalize`), multi-field search evaluation (`first_name`, `last_name`, `full_name`, `email`), two-tier ranking (exact matches preceding partial matches), normalized alphabetical tie-breaking (`last_name`, `first_name`, `id`), and 20-record capping.
- **Human review**: Reviewed search algorithms and tie-breaking ordering, and committed to git (`13eb41a`).
- **Tests**: Authored and passed 11 tests in `tests/test_search_service.py` covering normalization, field matching, diacritic/case insensitivity, ranking tiers, tie-breaking order, and capping.

### T-04: Validation and Errors
- **What the agent did**: Implemented `validate_query` in `src/search_service.py` enforcing VR-01 length constraints (≥ 3 non-whitespace characters) with EH-01 message, and VR-02 character whitelist (`@ . _ - '`, alphanumeric, Latin accents, whitespace) with EH-02 message. Kept zero-match queries returning empty lists without error for EH-03 presentation.
- **Human review**: Reviewed validation rules and error message contracts, and committed to git (`8c76a69`).
- **Tests**: Authored 43 parametrized test cases in `tests/test_search_service.py` covering query length rejection/acceptance, whitelist rejection/acceptance across forbidden symbols and non-Latin scripts, and empty state return. All 63 test suite cases passed.

### T-05: Tests & CLI Presentation
- **What the agent did**: Implemented `src/cli.py` featuring record formatting `[id] first_name last_name - email` (SR-05), `argparse` query parsing, output to stdout/stderr, and exit code mappings (0 for success / zero matches, 2 for validation errors, 1 for persistence errors). Created `tests/test_cli.py` and `tests/test_performance.py`.
- **Human review**: Reviewed CLI presentation and subprocess integration, and committed to git (`624273a`).
- **Tests**: Authored 11 CLI unit/subprocess tests and a performance benchmark on a 1,000-record dataset. All 75 tests passed. Benchmarked query response times at ~11 ms, comfortably under the 300 ms NFR-01 limit. Executed manual CLI smoke tests across success, empty, and validation modes.

### T-06: Documentation
- **What the agent did**: Populated `docs/traceability.md` establishing end-to-end requirement-to-test traceability. Created comprehensive `README.md` with environment setup, architecture overview, usage examples, and test execution instructions. Documented the agent workflow in `results/agent-report.md`.
- **Human review**: Verified all documentation against the Definition of Done checklist.
- **Tests**: Verified test suite passes without regressions (`75 passed in 0.42s`).

## Problems Encountered
1. **Unicode Alphabetical Tie-Breaking**: During initial implementation of T-03 tie-breaking, sorting accented names like "Álvarez" directly using Python string comparison resulted in "Álvarez" sorting after "Zúñiga" because the Unicode codepoint for 'Á' (193) is greater than 'Z' (90).
   - *Resolution*: Updated the sorting key to use `self.normalize(c.last_name)` and `self.normalize(c.first_name)`, ensuring proper alphabetical ordering in accordance with Spanish/Latin alphabetization rules while preserving deterministic tie-breaking.

## Human Interventions
1. The user reviewed and made individual git commits after each discrete task (T-01 through T-05).
2. The user instructed to leave `AI_USAGE_LOG.md` unmodified during T-06 documentation.

## Requirement / Specification Changes
None. The requirements in `REQUIREMENTS.md` and contract in `SPEC.md` were held strictly immutable throughout the entire implementation process.

## Final Verification
- **Automated Test Suite**: 75 tests passing across all test files (`test_repository.py`, `test_search_service.py`, `test_cli.py`, `test_performance.py`).
- **Performance**: End-to-end queries execute in ~11 ms on 1,000 records (well below the ≤ 300 ms requirement).
- **Manual Verification**: CLI tested via `python -m src.cli` with exact, accented, empty, and invalid queries.
- **Traceability**: All requirements and acceptance criteria fully mapped and verified in `docs/traceability.md`.

## Lessons Learned
- Spec-driven development with strict separation of concerns (CLI, domain service, repository) ensures testability without subprocess overhead for domain rules.
- Explicit Unicode normalization handling is essential when dealing with accented names to avoid subtle sorting anomalies under standard codepoint comparisons.
- Incremental review and verification per task maintains high code quality and strict adherence to requirements.