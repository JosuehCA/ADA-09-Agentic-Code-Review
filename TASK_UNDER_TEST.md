# Task Under Test

Change ID: CR-01

## Goal
Add customer ID matching to `CustomerSearchService.search` so that searching for a customer ID (exact or partial) returns the corresponding customer record, ranking exact ID matches in the exact tier and partial ID matches in the partial tier, respecting all existing tie-breaking and capping rules.

## Requirements Covered
- FR-01
- AC-01

## Verification
- An exact query for a customer ID (e.g., `"CUST-001"`) returns the matching customer in the exact match tier.
- A partial query for a customer ID substring (e.g., `"001"`) returns the matching customer in the partial match tier.
- Existing tests continue to pass without regression, and new unit tests in `tests/test_search_service.py` demonstrate ID search functionality.

## Constraints
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Keep changes scoped to this task.
- Do not redefine requirements in this file.
