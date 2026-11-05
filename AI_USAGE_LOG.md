### Entry 01 - Change Request (CR-01) Definition & Refinement
- **Stage**: Requirements / Change Request Definition.
- **Prompt/goal**: Define and refine Change Request CR-01 to add customer ID search to `CustomerSearchService.search` across exact and partial tiers while preserving existing tie-breaking, normalization, and result-capping rules.
- **AI Contribution**: Drafted `CHANGE_REQUEST.md` outlining the goal, mapped requirements (`FR-01`, `AC-01`), constraints (preserve architecture boundaries `CLI -> SearchService -> Repository`, maintain existing tests, no external dependencies), and concrete verification criteria (e.g. `"CUST-001"` in exact tier, `"001"` in partial tier). Prepared `results/run-context.md`.
- **Student Decision**: Approved the Change Request specification without weakening the 3-character minimum length constraint or tie-breaking rules (`Approved to implement: YES, Approved by: Josueh C. (Human Reviewer)`).
- **Impact**: Created `CHANGE_REQUEST.md` and `results/run-context.md` on branch `ada09/cr-id-search` (Commit `e8ee211`).

### Entry 02 - Coder Agent Planning & Human Plan Approval
- **Stage**: Architectural & Implementation Planning.
- **Prompt/goal**: Formulate an implementation plan for CR-01 to add customer ID matching into `src/search_service.py` with corresponding test additions in `tests/test_search_service.py` and `tests/test_cli.py`.
- **AI Contribution**: Proposed a 7-step plan: (1) normalize `customer.id` with `self.normalize(customer.id)`, (2) include `norm_id` in exact match tuple check, (3) include `norm_id` in partial match substring `elif`, (4) preserve existing tie-breaking (`last_name`, `first_name`, `id`), (5) add unit tests for exact/partial ID matching and ranking precedence, (6) add CLI integration tests, and (7) run `./scripts/verify_repo.sh`.
- **Student Decision**: Approved the plan. Verified that business logic remained strictly confined within `CustomerSearchService` in `src/search_service.py` and that the presentation layer in `src/cli.py` remained decoupled.
- **Impact**: Documented plan in `results/coder-report.md`.

### Entry 03 - Implementation & Code Modification
- **Stage**: Implementation & Test Authoring.
- **Prompt/goal**: Implement customer ID search matching and ranking in `CustomerSearchService` and author automated unit, integration, and performance tests.
- **AI Contribution**: Implemented `norm_id = self.normalize(customer.id)` in `src/search_service.py`. Added 5 unit tests in `tests/test_search_service.py` (exact ID, partial ID, exact ID before partial, exact name before partial ID, ID tie-breaking), 2 CLI tests in `tests/test_cli.py`, and 1 latency query in `tests/test_performance.py`. Suggested handling short IDs, noting in coder report that VR-01 (>= 3 chars) applies universally.
- **Student Decision**: Accepted the core implementation and tests; rejected modifying `validate_query` or weakening VR-01 length constraints to accommodate IDs shorter than 3 characters, preserving spec integrity.
- **Impact**: Committed implementation as commit `94d770d` (`feat: implement CR-01 customer id search`), passing 82/82 tests.

### Entry 04 - Independent Reviewer Agent Audit & Evidence-Based Findings
- **Stage**: Independent Code & Contract Review.
- **Prompt/goal**: Perform an independent review of the PR candidate against `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `results/review-contract.md`, and git diff without approving based solely on green tests.
- **AI Contribution**: Conducted an exhaustive audit identifying 2 MUST FIX issues (RF-01: fabricated environment `Python 3.14.7` and pre-implementation commit `e8ee211` in `verification-report.md`; RF-02: `docs/traceability.md` not updated for CR-01, violating Definition of Done), 4 SHOULD FIX issues (RF-03: set assertion in ranking test masking tie-breaking order; RF-04: missing CLI test for partial ID; RF-05: missing 20-record capping test for ID matches; RF-06: stale CLI `--help` description and `README.md`), and 3 OPTIONAL findings.
- **Student Decision**: Validated the independent review findings as thorough and evidence-based. Acknowledged that passing green tests had masked evidence and traceability omissions.
- **Impact**: Authored `results/review-report.md` recommending `READY AFTER MUST FIX`.

### Entry 05 - Human Review Gate & Finding Severity Decisions
- **Stage**: Human Review & Triage Gate.
- **Prompt/goal**: Review agent findings in `results/review-report.md` and render authoritative human decisions on severity and required corrective actions.
- **AI Contribution**: Provided structured findings breakdown and file/line evidence citations.
- **Student Decision**:
  - **Accepted RF-01 (MUST FIX)**: Non-matching environment info confirmed; required regenerating `verification-report.md`.
  - **Modified RF-02 (MUST FIX -> SHOULD FIX)**: Reclassified as a maintainability issue rather than safety-critical defect; required updating `docs/traceability.md`.
  - **Modified RF-03 (SHOULD FIX -> MUST FIX)**: Reclassified to MUST FIX because loose set assertions risk test masking and regression in deterministic tie-breaking.
  - **Accepted RF-04 (SHOULD FIX)**: Confirmed missing CLI test for partial ID matching.
  - **Modified RF-05 (SHOULD FIX -> MUST FIX)**: Reclassified to MUST FIX because unverified capping represents a potential requirement violation of NFR-03.
  - **Accepted RF-06 (SHOULD FIX)**: Confirmed CLI help description and README omitted customer ID search.
- **Impact**: Created `results/human-review-decisions.md` (Commit `ef1380c`) returning PR to coder agent for fixes.

### Entry 06 - Fix Cycle, Re-Review Verification & Evidence Consolidation
- **Stage**: Remediation, Re-Review & Final Evidence Consolidation.
- **Prompt/goal**: Apply required fixes from human decisions, re-run verification, perform an independent re-review, and compile final PR evidence.
- **AI Contribution**: Updated `src/cli.py` description, added `test_cli_search_by_partial_customer_id` in `tests/test_cli.py`, tightened assertion in `tests/test_search_service.py` to strict list comparison, added `test_capping_partial_id_matches_limits_to_twenty` (84 tests total), updated `README.md`, `docs/traceability.md`, and `results/verification-report.md`. Conducted independent re-review confirming 6/6 findings RESOLVED with 0 regressions, and compiled `results/PR_EVIDENCE.md`.
- **Student Decision**: Reviewed the re-review report, verified `./scripts/verify_repo.sh` exits 0 (84 passed in 0.28s, ruff clean, contract PASS), confirmed zero regressions, and approved final status as `READY FOR HUMAN MERGE`.
- **Impact**: Committed fixes in `e8b8e2b`, generated `results/re-review-report.md` and `results/PR_EVIDENCE.md`.
