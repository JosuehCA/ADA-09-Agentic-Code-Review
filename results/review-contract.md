# Review Contract

## Change CR-01

## Requirements / Acceptance Criteria
FR-01
AC-01

## Architecture Constraints
**Expected dependency flow:** CLI -> SearchService -> Repository
**Business-rule location:** `src/search_service.py` (`CustomerSearchService`)
**Protected boundaries:** Presentation isolated to `src/cli.py`; data access isolated to `src/repository.py`; baseline fixture `data/customers.json` unmodified.

## Review Rules
Verify requirement coverage.
Verify every called API/dependency exists.
Check architecture boundaries.
Inspect tests for masking / false confidence.
Check regression behavior.
Identify unnecessary technical debt.
Cite evidence for every finding.

## Severity

**MUST FIX:**
Requirement violation, regression, security/integrity risk, hallucinated API/dependency, broken architecture constraint, or defect that makes the change unsafe to approve.

**SHOULD FIX:**
Significant maintainability, coverage, design, or clarity issue that does not block the requested behavior.

**OPTIONAL:**
Non-blocking improvement outside the minimum acceptance threshold.
