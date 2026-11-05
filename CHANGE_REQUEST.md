# Change Request

Change ID: CR-01

## Goal
Add customer ID matching to `CustomerSearchService.search` so that searching for a customer ID (exact or partial) returns the corresponding customer record, ranking exact ID matches in the exact tier and partial ID matches in the partial tier, while respecting existing tie-breaking, normalization, and result-capping rules.

## Requirements Covered
- FR-01
- AC-01

## Constraints
- Follow AGENTS.md.
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Preserve architecture boundaries (`CLI -> SearchService -> Repository`).
- Do not weaken or delete existing tests.
- Do not modify `data/customers.json` or add external dependencies.

## Verification
- An exact query matching a customer ID (e.g., `"CUST-001"`) returns the matching customer in the exact match tier.
- A partial query matching a customer ID substring (e.g., `"001"`) returns the matching customer in the partial match tier.
- All existing tests in the suite pass with `./scripts/verify_repo.sh`.
- New automated tests in `tests/test_search_service.py` demonstrate ID search and ranking correctness.

## Human Approval
Approved to implement: YES
Approved by: Josueh C. (Human Reviewer)
Date: 2026-11-05
