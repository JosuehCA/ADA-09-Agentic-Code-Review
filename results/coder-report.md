# Coder Agent Report

## Change
Change ID: CR-01
Branch: ada09/cr-id-search
Base commit: 3662558

## Requirements Covered
FR-01
AC-01

## Implementation Plan
1. Inspect the domain search service `CustomerSearchService.search` in `src/search_service.py`.
2. Add normalization of `customer.id` (`norm_id = self.normalize(customer.id)`) alongside name and email fields.
3. Include `norm_id` in the exact match condition (`normalized_query in (norm_id, norm_first, norm_last, norm_full, norm_email)`).
4. Include `norm_id` in the partial match condition (`normalized_query in norm_id or normalized_query in norm_full or normalized_query in norm_email`).
5. Ensure existing ranking tiers, tie-breaking (`last_name`, `first_name`, `id`), and 20-record capping remain intact.
6. Add comprehensive unit and integration tests covering exact and partial ID matching, case insensitivity, ranking tiers (exact ID match preceding partial matches, exact name match preceding partial ID match), and tie-breaking in `tests/test_search_service.py` and `tests/test_cli.py`.
7. Verify all existing and new tests pass, linter passes, and repo contract checks pass via `./scripts/verify_repo.sh`.

## Files Changed
- `src/search_service.py`: Added `norm_id = self.normalize(customer.id)` and evaluated `norm_id` in exact match check and partial match check.
- `tests/test_search_service.py`: Added unit tests for exact ID matching, partial ID matching, ranking precedence, and tie-breaking.
- `tests/test_cli.py`: Added CLI unit test and subprocess integration test verifying customer ID search.
- `tests/test_performance.py`: Added customer ID query to latency benchmark suite.

## Tests Added / Updated
- `tests/test_search_service.py`:
  - `test_search_matches_customer_id_exact`: Verifies exact query matching against customer ID, including case insensitivity.
  - `test_search_matches_customer_id_partial`: Verifies partial substring matching against customer ID in the partial tier.
  - `test_ranking_exact_id_matches_precede_partial_matches`: Verifies exact ID matches strictly precede partial matches.
  - `test_ranking_exact_name_precedes_partial_id_match`: Verifies exact name matches strictly precede partial ID matches.
  - `test_ranking_id_partial_matches_tie_breaking`: Verifies deterministic tie-breaking among ID matches by `last_name`, `first_name`, then `id`.
- `tests/test_cli.py`:
  - `test_cli_search_by_customer_id`: Verifies CLI handler execution and output formatting when searching by customer ID.
  - `test_subprocess_cli_search_by_id`: Verifies end-to-end CLI subprocess search by customer ID against default fixture dataset.
- `tests/test_performance.py`:
  - `test_performance_end_to_end_query_under_300ms`: Updated query list to include customer ID match (`"PERF-0500"`).

## Commands Executed
- `./scripts/verify_repo.sh`
- `git status`
- `git diff src/search_service.py`
- `git diff tests/test_search_service.py`
- `git diff tests/test_cli.py`
- `git diff tests/test_performance.py`

## Verification Result
- Command: `./scripts/verify_repo.sh`
- Exit Code: `0`
- Output:
  - pytest: 82 passed in ~0.28s
  - ruff check: All checks passed!
  - repo checks: REPO_CONTRACT: PASS, VERIFY_REPO: PASS

## Assumptions
- Customer ID format conforms to allowed whitelist characters (alphanumeric and symbols like `-`).
- Exact matching on customer ID is case-insensitive following existing normalization rules (NFD + lowercasing).
- Minimum query length constraint (VR-01, >= 3 non-whitespace characters) applies equally to customer ID searches.

## Known Limitations
- Customer ID search requires a minimum of 3 characters as mandated by VR-01. Customer IDs shorter than 3 characters cannot be searched in isolation.

## Self-Check
[x] Scope respected
[x] Existing tests not weakened
[x] No undocumented dependency/API introduced
[x] Ready for independent review

## Fix Cycle

### Addressed Findings from Human Review (results/human-review-decisions.md)
- **RF-01 (MUST FIX - ACCEPTED)**: Regenerated `results/verification-report.md` with accurate environment data (`Python 3.12.7`) and referenced implementation commit `94d770d`.
- **RF-02 (SHOULD FIX - MODIFIED)**: Updated `docs/traceability.md` to explicitly link customer ID search requirements under FR-01, FR-02, FR-06, and NFR-03 (with CR-01), mapping all newly added test functions.
- **RF-03 (MUST FIX - MODIFIED)**: In `tests/test_search_service.py` (`test_ranking_exact_id_matches_precede_partial_matches`), replaced the set assertion with an exact ordered assertion: `assert [c.id for c in results] == ["CUST-001", "CUST-0010", "CUST-002"]`.
- **RF-04 (SHOULD FIX - ACCEPTED)**: Added `test_cli_search_by_partial_customer_id` in `tests/test_cli.py` verifying that searching a partial customer ID substring (`"001"`) outputs formatted customer records to stdout and exits with code 0.
- **RF-05 (MUST FIX - MODIFIED)**: Added `test_capping_partial_id_matches_limits_to_twenty` in `tests/test_search_service.py` verifying that a partial ID query matching >20 records caps at exactly 20 records in deterministic sorted order.
- **RF-06 (SHOULD FIX - ACCEPTED)**: Updated `src/cli.py` argparse description to `"Search customers by first name, last name, email, or customer ID."` and added customer ID search examples (exact and partial) to `README.md`.

### Files Modified in Fix Cycle
- `src/cli.py`
- `tests/test_search_service.py`
- `tests/test_cli.py`
- `README.md`
- `docs/traceability.md`
- `results/verification-report.md`
- `results/coder-report.md`

### Verification Evidence
- Verification Command: `./scripts/verify_repo.sh`
- Exit Code: `0`
- Tests: 84 passed in 0.32s
- Lint: All checks passed!
- Repo Contract: REPO_CONTRACT: PASS, VERIFY_REPO: PASS

This report is NOT an approval.
