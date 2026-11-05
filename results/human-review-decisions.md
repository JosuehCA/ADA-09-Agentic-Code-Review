# Human Review Decisions

## Change CR-01

### RF-01
**Reviewer severity:** MUST FIX 
**Human decision:** ACCEPTED 
**Reason:** Non-matching info compared to local environment has been revised and confirmed.
**Required action:** Regenerate `results/verification-report.md` with accurate environment data (`Python 3.12.7`) and reference the actual implementation commit (`94d770d`).

### RF-02
**Reviewer severity:** MUST FIX 
**Human decision:** MODIFIED
**Reason**: Does not actually fit into a "MUST FIX" category from the review contract, but does for a "SHOULD FIX" as a "significant maintainability" problem.
**Final severity:** SHOULD FIX
**Required action:** Update `docs/traceability.md` to document customer ID search under FR-01 and AC-01 (or CR-01) and map all newly introduced test functions.

### RF-03
**Reviewer severity:** SHOULD FIX 
**Human decision:** MODIFIED
**Reason**: Directly involves a regression problem with existing tests.
**Final severity:** MUST FIX
**Required action:** Replace the set assertion with an exact ordered assertion:
`assert [c.id for c in results] == ["CUST-001", "CUST-0010", "CUST-002"]`.

### RF-04
**Reviewer severity:** SHOULD FIX 
**Human decision:** ACCEPTED
**Reason**: Correctly identifies missing tests for partial matches at the CLI level for customer IDs
**Required action:** Add a CLI test in `tests/test_cli.py` querying a partial customer ID substring (e.g. `"001"`) asserting stdout formatting and exit code 0.

### RF-05
**Reviewer severity:** SHOULD FIX 
**Human decision:** MODIFIED
**Reason**: Requirement violation of NFR-03 by not setting the cap of size 20 for matches on IDs
**Final severity:** MUST FIX
**Required action:** Add a test in `tests/test_search_service.py` verifying that a partial ID query matching >20 records returns exactly 20 records in sorted order.

### RF-06
**Reviewer severity:** SHOULD FIX 
**Human decision:** ACCEPTED
**Reason**: CLI help menu does indeed miss to declare that ID matching functionality is supported.
**Required action:** Update `src/cli.py` description to `"Search customers by first name, last name, email, or customer ID."` and add customer ID query examples to `README.md`.

## Human Gate
[X] Return to coder-agent
[ ] Ready for final re-review [ ] Stop / escalate