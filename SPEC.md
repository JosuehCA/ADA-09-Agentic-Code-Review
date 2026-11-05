# Customer Search Feature

## Goal
Provide a command-line customer search capability that locates records by first name, last name, or email address with deterministic ranking and input validation.

## Requirements Covered
This specification implements and traces to:
- FR-01, FR-02, FR-03, FR-04, FR-05, FR-06
- NFR-01, NFR-02, NFR-03
- A-01, A-02, A-03

## Scope
- Validating query length (minimum non-whitespace characters) and allowed character sets.
- Matching query strings across first name, last name, computed full name, and email address.
- Normalizing characters for case-insensitive and diacritic-insensitive comparisons.
- Sorting results deterministically: exact matches first, followed by partial matches, with alphabetical tie-breaking.
- Capping query output to a maximum of 20 customer records.
- Displaying clear error messages on invalid input and a friendly message when no matches are found.
- CLI execution returning standard operating system exit codes (`0` for success, `2` for validation errors).

## Out of Scope
- Creating, updating, or deleting customer records.
- Non-Latin script normalization.
- Multi-field boolean filtering flags.
- Pagination commands or cursor navigation beyond returning the top 20 records.
- Remote database connections or external API calls.

## Domain Model

    Customer:
      id: str
      first_name: str
      last_name: str
      email: str

    Storage:
      JSON file: customers.json

## Search Rules
- **SR-01 Target Fields [FR-01, FR-02]**: The search query is evaluated against `first_name`, `last_name`, `email`, and the computed `full_name` (`f"{first_name} {last_name}"`). Multi-word inputs are matched as a continuous substring against `full_name`.
- **SR-02 Normalization [FR-04]**: Prior to matching, both the query and target fields are stripped of diacritical marks via Unicode normalization (NFD decomposition) and transformed to lowercase.
- **SR-03 Ranking & Ordering [FR-06]**:
  1. Exact match: The normalized query strictly equals `first_name`, `last_name`, `full_name`, or `email`.
  2. Partial match: The normalized query is a substring of `full_name` or `email`.
  3. Tie-breaking: If multiple records have the same match tier, sort ascending alphabetically by `last_name`, then `first_name`, then `id`.
- **SR-04 Result Capping [NFR-03]**: The search returns at most the first 20 ranked records.
- **SR-05 Result Presentation [FR-01]**: Each matching record displayed to the user includes `id`, `first_name`, `last_name`, and `email`.

## Validation Rules
- **VR-01 Query Length [FR-03]**: The input string is stripped of leading and trailing whitespace. If the trimmed string contains fewer than 3 characters, the query is rejected.
- **VR-02 Character Whitelist [NFR-02]**: The search query must only contain alphanumeric characters, Latin accented letters, whitespace, and the symbols: `@`, `.`, `_`, `-`, `'`. Any input containing characters outside this whitelist is rejected before search execution.

## Error Handling
- **EH-01 Input Length Error [FR-03, VR-01]**: When a query has fewer than 3 non-whitespace characters, output `"Error: Search query must contain at least 3 non-whitespace characters."` and exit with code `2`.
- **EH-02 Invalid Characters Error [NFR-02, VR-02]**: When a query contains disallowed characters, output `"Error: Query contains invalid characters. Allowed symbols: @ . _ - ' and alphanumeric characters."` and exit with code `2`.
- **EH-03 Zero Matches State [FR-05]**: When a valid query yields zero matching records, output `"No customers found matching '<query>'."` and exit with code `0`.

## Acceptance Criteria
- **AC-01 [FR-01, FR-02, SR-01]**: A valid query returns customer records where the term appears in `first_name`, `last_name`, `full_name`, or `email` as an exact match or partial substring.
- **AC-02 [FR-03, VR-01, EH-01]**: Executing a search with fewer than 3 non-whitespace characters outputs the EH-01 error message and exits with status code 2.
- **AC-03 [FR-04, SR-02]**: Queries match target fields regardless of uppercase/lowercase differences or diacritic variations.
- **AC-04 [FR-05, EH-03]**: Executing a valid search that matches no records prints the EH-03 empty state message and exits with status code 0.
- **AC-05 [FR-06, SR-03]**: Exact matches are listed before partial matches; records with identical match tiers are ordered by `last_name`, `first_name`, and `id`.
- **AC-06 [NFR-01]**: End-to-end query execution completes in ≤ 300 ms on a local dataset containing 1,000 customer records.
- **AC-07 [NFR-02, VR-02, EH-02]**: Providing an input with characters outside the whitelist halts execution with the EH-02 error message and status code 2.
- **AC-08 [NFR-03, SR-04]**: Queries matching more than 20 records return exactly the top 20 ranked records.

## Test Scenarios
- **TS-01 -> AC-01**: Search matching `first_name`, `last_name`, `full_name`, and `email` independently.
- **TS-02 -> AC-01**: Partial substring matching on internal segments of names and email addresses.
- **TS-03 -> AC-02, VR-01, EH-01**: Input validation failure and non-zero exit code for inputs: `""`, `"a"`, `" ab "`, and `"   "`.
- **TS-04 -> AC-03, SR-02**: Accent and casing combinations.
- **TS-05 -> AC-04, EH-03**: Valid query with no matching records returns zero results and displays the EH-03 message.
- **TS-06 -> AC-05, SR-03**: Mixed result verification confirming exact matches precede prefix and substring matches, with correct alphabetical tie-breaking.
- **TS-07 -> AC-07, VR-02, EH-02**: Rejection of forbidden characters with exit code 2.
- **TS-08 -> AC-08, SR-04**: Fixture with 25 matching records confirms that exactly 20 records are returned.
- **TS-09 -> AC-06**: Performance benchmark asserting latency ≤ 300 ms across 1,000 local records.

## Constraints
- **C-01 [Assignment]**: Python 3.11+ using standard library and pytest only.
- **C-02 [Assignment]**: Single-user local CLI application running without background server daemons.
- **C-03 [A-01, A-02]**: Dataset guarantees unique `id` and unique `email` per customer.
- **C-04 [A-03]**: Names contain Latin characters (supporting Spanish diacritics); emails conform to standard ASCII format.

## Open Questions
N/A: All questions from REQUIREMENTS.md have been resolved into verifiable contract rules:
- Q-01 resolved in SR-01.
- Q-02 resolved in SR-03.
- Q-03 resolved in VR-01 and EH-01.
- Q-04 resolved in SR-05.