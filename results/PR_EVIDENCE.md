# PR Evidence

## Change
**Change ID:** CR-01  
**PR / Branch:** `ada09/cr-id-search`  
**Base commit:** `3662558` (`chore: added one more core change to be kept for final project`)  
**Final commit:** `e8b8e2b` (`fix: address ADA-09 review findings`)  

## Requirements / Acceptance Criteria
- **FR-01**: Multi-field search across customer fields (extended to support customer ID)
- **FR-02**: Partial substring matching on customer ID, full name, and email address
- **FR-06**: Deterministic ranking: exact matches first, partial matches second, alphabetical tie-breaking (`last_name`, `first_name`, `id`)
- **NFR-03**: Result capping at a maximum of 20 records
- **AC-01**: A valid query returns customer records where the term appears in `first_name`, `last_name`, `full_name`, `email`, or `id` as an exact match or partial substring
- **AC-05**: Exact matches precede partial matches; records with identical match tiers are ordered by `last_name`, `first_name`, and `id`
- **AC-08**: Queries matching more than 20 records return exactly the top 20 ranked records

## Implementation
**Coder report:** `results/coder-report.md`  
**Files changed:**
- `src/search_service.py`: Added customer ID normalization (`norm_id`), exact ID match evaluation, and partial ID match evaluation.
- `src/cli.py`: Updated argument parser description to include customer ID.
- `tests/test_search_service.py`: Added unit tests for exact ID matching, partial ID matching, ranking precedence, deterministic tie-breaking, and 20-record capping for ID matches.
- `tests/test_cli.py`: Added CLI unit tests for exact and partial ID search, and subprocess CLI search by ID.
- `tests/test_performance.py`: Added customer ID query (`"PERF-0500"`) to latency benchmark.
- `README.md`: Added customer ID search documentation and CLI usage examples.
- `docs/traceability.md`: Updated traceability matrix mapping FR-01, FR-02, FR-06, and NFR-03 to CR-01 and newly added tests.
- `CHANGE_REQUEST.md`: Recorded change request specification and initial human approval.
- `results/run-context.md`: Recorded environment and baseline metadata.
- `results/verification-report.md`: Recorded automated check evidence and runtime versions.

**Commits:**
- `e8ee211` chore: change request preparation
- `94d770d` feat: implement CR-01 customer id search
- `c8d97a0` chore: add initial review setup and results, with review contract and report from independent agent reviewer
- `ef1380c` chore: added human eval on agent review
- `e8b8e2b` fix: address ADA-09 review findings

## Verification
**Verification command:** `./scripts/verify_repo.sh`  
**Final result:** PASS (Exit code 0)  
**Tests:** 84 passed in 0.31s (`pytest -q` / `pytest -v`)  
**Lint:** PASS (`ruff check .` — All checks passed!)  
**Security / repo checks:** PASS (`python scripts/check_repo_contract.py` — `REPO_CONTRACT: PASS`, `VERIFY_REPO: PASS`; input length and character whitelist validation checks passed)  

## Independent Review
**Review report:** `results/review-report.md`  
**MUST FIX found:** 2
- **RF-01**: Fabricated Python runtime (`Python 3.14.7`) and pre-implementation commit hash (`e8ee211`) in verification report.
- **RF-02**: Traceability matrix in `docs/traceability.md` not updated for CR-01 (Definition of Done failure).

**SHOULD FIX found:** 4
- **RF-03**: Set comparison in `test_ranking_exact_id_matches_precede_partial_matches` masked deterministic tie-breaking order.
- **RF-04**: Missing test coverage for partial customer ID queries in the CLI presentation layer.
- **RF-05**: Missing test coverage for the 20-record capping rule on customer ID matches.
- **RF-06**: Stale CLI `--help` description and `README.md` lacking customer ID documentation.

**OPTIONAL found:** 3
- **RF-07**: Baseline `REQUIREMENTS.md` and `SPEC.md` not synchronized with CR-01 changes.
- **RF-08**: Redundant Unicode normalization passes in search loop and sort key.
- **RF-09**: Missing explicit unit test for rejection of isolated customer ID queries with fewer than 3 characters.

## Human Decisions
- **Accepted:**
  - **RF-01** (MUST FIX): Regenerate `results/verification-report.md` with accurate runtime environment data (`Python 3.12.7`) and reference implementation commit `94d770d`.
  - **RF-04** (SHOULD FIX): Add CLI test in `tests/test_cli.py` querying partial customer ID (`"001"`).
  - **RF-06** (SHOULD FIX): Update `src/cli.py` description and add customer ID examples to `README.md`.
- **Modified:**
  - **RF-02** (MUST FIX -> SHOULD FIX): Reclassified as maintainability issue; required updating `docs/traceability.md` for FR-01/AC-01 and CR-01 tests.
  - **RF-03** (SHOULD FIX -> MUST FIX): Reclassified as regression prevention; required replacing set assertion with exact ordered assertion in `tests/test_search_service.py`.
  - **RF-05** (SHOULD FIX -> MUST FIX): Reclassified as requirement violation of NFR-03; required adding test verifying 20-record capping on customer ID matches.
- **Rejected:** None
- **Deferred:** RF-07 (Spec baseline synchronization), RF-08 (Performance optimization), RF-09 (Short ID query test).

## Re-review
**Resolved:** 6 (RF-01, RF-02, RF-03, RF-04, RF-05, RF-06)  
**Partially resolved:** 0  
**Not resolved:** 0  
**New MUST FIX:** 0 (Full test suite passes at 84/84 tests, linter clean, repo contract verified, architecture boundaries intact)  

## Traceability

| Requirement / AC | Task / Change | Code | Test | Review Finding |
|---|---|---|---|---|
| **FR-01 / AC-01** (Exact ID Search) | CR-01, T-03, T-05 | `CustomerSearchService.search()` in `src/search_service.py`<br/>`CLI.run()` in `src/cli.py` | `test_search_matches_customer_id_exact` in `tests/test_search_service.py`<br/>`test_cli_search_by_customer_id`, `test_subprocess_cli_search_by_id` in `tests/test_cli.py` | RF-01, RF-02, RF-06 (Resolved) |
| **FR-02 / AC-01** (Partial ID Search) | CR-01, T-03, T-05 | `CustomerSearchService.search()` in `src/search_service.py`<br/>`CLI.run()` in `src/cli.py` | `test_search_matches_customer_id_partial` in `tests/test_search_service.py`<br/>`test_cli_search_by_partial_customer_id` in `tests/test_cli.py` | RF-02, RF-04 (Resolved) |
| **FR-06 / AC-05** (Ranking & Tie-breaking) | CR-01, T-03 | `CustomerSearchService.search()` in `src/search_service.py` | `test_ranking_exact_id_matches_precede_partial_matches`<br/>`test_ranking_exact_name_precedes_partial_id_match`<br/>`test_ranking_id_partial_matches_tie_breaking` in `tests/test_search_service.py` | RF-02, RF-03 (Resolved) |
| **NFR-03 / AC-08** (Result Capping at 20) | CR-01, T-03 | `CustomerSearchService.search()` in `src/search_service.py` | `test_capping_partial_id_matches_limits_to_twenty` in `tests/test_search_service.py` | RF-02, RF-05 (Resolved) |
| **NFR-01 / AC-06** (Latency <= 300 ms) | CR-01, T-05 | `CustomerSearchService.search()` in `src/search_service.py` | `test_performance_end_to_end_query_under_300ms` in `tests/test_performance.py` | RF-08 (Deferred / Non-blocking) |
| **Audit & Contract Integrity** | CR-01, Review Cycle | `docs/traceability.md`<br/>`results/verification-report.md`<br/>`README.md` | `./scripts/verify_repo.sh`<br/>`python scripts/check_repo_contract.py` | RF-01, RF-02, RF-06 (Resolved) |

## Remaining Risks / Technical Debt
- **Specification Baseline Drift (RF-07):** Baseline `REQUIREMENTS.md` and `SPEC.md` remain scoped to name/email search, while `CHANGE_REQUEST.md` and `docs/traceability.md` document the customer ID search addition. Recommended to synchronize baselines during the next scheduled documentation refresh.
- **Redundant Unicode Normalization (RF-08):** Static customer records are normalized during each search and sort invocation. Currently well within SLA (~15 ms measured vs 300 ms limit), but precomputing normalized fields at repository load time is recommended if scaling beyond 10,000 records.
- **Minimum Query Length Constraint:** Customer IDs shorter than 3 characters cannot be searched in isolation due to VR-01 (length >= 3 non-whitespace characters).

## Final Human Decision
[ ] NOT READY  
[x] READY FOR HUMAN MERGE  

**Approved by:** Josueh C. (Human Reviewer)  
**Date:** 2026-11-05
