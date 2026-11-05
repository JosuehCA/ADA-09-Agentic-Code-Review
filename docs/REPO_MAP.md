# Repository Map

## Entry Points
- `src/cli.py` - Command-line interface entry point (argparse, exit codes, formatting, stdout/stderr handling).
- `src/search_service.py` - Domain search service: query validation (VR-01, VR-02), Unicode normalization (NFD, SR-02), multi-field matching (SR-01), deterministic ranking and tie-breaking (SR-03), and 20-record capping (SR-04).
- `src/models.py` - Core domain entities (`Customer` dataclass with `full_name` property).
- `src/repository.py` - Data persistence layer: loading and deserializing `data/customers.json` into `Customer` instances.

## Tests
- `tests/test_search_service.py` - Unit tests for search service, normalization, validation rules, match tiers, and tie-breaking.
- `tests/test_cli.py` - Integration and CLI behavior tests, subprocess testing, terminal output, and process exit codes (0, 1, 2).
- `tests/test_repository.py` - Persistence tests, file reading, and malformed JSON error handling.
- `tests/test_performance.py` - Automated performance benchmark verifying latency ≤ 300 ms across 1,000 customer records.

## Change Guide
If changing search behavior or adding business rules:
1. Check `REQUIREMENTS.md` and `SPEC.md` for existing contracts and acceptance criteria.
2. Update `src/search_service.py` to add or modify domain logic.
3. Update `src/cli.py` only if presentation, argument parsing, or error formatting changes.
4. Add or update unit tests in `tests/test_search_service.py` and integration tests in `tests/test_cli.py`.
5. Run `./scripts/verify_repo.sh` to execute tests, linter, and repository contract checks.

## Do Not Edit Directly
- `data/customers.json` - Baseline test fixture. Must remain unmodified to ensure baseline test reproducibility.
- `REQUIREMENTS.md` & `SPEC.md` - Normative sources of truth. Never modify requirements solely to make code or tests pass.
- `docs/traceability.md` - Update only when intentionally modifying requirement/acceptance criterion test coverage.
- `.github/` - CI workflows and configuration.
