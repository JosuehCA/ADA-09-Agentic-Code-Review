# Traceability Matrix

This matrix establishes end-to-end traceability connecting Requirements to Acceptance Criteria, Tasks, Implementation Components, Test Suites, and Verification Status.

## Traceability Table

| Requirement ID | Acceptance Criterion | Task | Implementation Component | Test Suite / Test Name | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-01** (Multi-field Search / Customer ID Search) | AC-01, AC-05 | T-03, T-05, CR-01 | `CustomerSearchService.search()` in `src/search_service.py`<br/>`format_customer()` in `src/cli.py` | `test_search_matches_first_name`, `test_search_matches_last_name`, `test_search_matches_full_name`, `test_search_matches_email`, `test_search_matches_customer_id_exact` in `tests/test_search_service.py`<br/>`test_cli_search_by_customer_id`, `test_subprocess_cli_search_by_id` in `tests/test_cli.py` | **PASS** |
| **FR-02** (Partial Substring Matching) | AC-01 | T-03, CR-01 | `CustomerSearchService.search()` in `src/search_service.py` | `test_search_matches_full_name`, `test_search_matches_email`, `test_search_matches_customer_id_partial` in `tests/test_search_service.py`<br/>`test_cli_search_by_partial_customer_id` in `tests/test_cli.py` | **PASS** |
| **FR-03** (Min 3 Non-whitespace Chars) | AC-02 | T-04, T-05 | `CustomerSearchService.validate_query()` in `src/search_service.py`<br/>`CLI.run()` in `src/cli.py` | `test_validation_query_length_rejects_fewer_than_three_characters`, `test_validation_query_length_accepts_valid_length` in `tests/test_search_service.py`<br/>`test_cli_validation_length_error_exits_with_code_2` in `tests/test_cli.py` | **PASS** |
| **FR-04** (Case & Diacritic Insensitive) | AC-03 | T-03 | `CustomerSearchService.normalize()` in `src/search_service.py` | `test_normalization_strips_diacritics_and_lowercases`, `test_search_diacritic_and_case_insensitive` in `tests/test_search_service.py` | **PASS** |
| **FR-05** (Zero Matches User Message) | AC-04 | T-04, T-05 | `CustomerSearchService.search()` in `src/search_service.py`<br/>`CLI.run()` in `src/cli.py` | `test_empty_state_returns_empty_list` in `tests/test_search_service.py`<br/>`test_cli_empty_matches_returns_zero_and_prints_eh03_message`, `test_subprocess_cli_empty_state` in `tests/test_cli.py` | **PASS** |
| **FR-06** (Ranking: Exact First, Partial Second) | AC-05 | T-03, CR-01 | `CustomerSearchService.search()` in `src/search_service.py` | `test_ranking_exact_matches_precede_partial_matches`, `test_ranking_tie_breaking_order`, `test_ranking_exact_id_matches_precede_partial_matches`, `test_ranking_exact_name_precedes_partial_id_match`, `test_ranking_id_partial_matches_tie_breaking` in `tests/test_search_service.py` | **PASS** |
| **NFR-01** (Response Time ≤ 300 ms) | AC-06 | T-05 | In-memory evaluation in `src/search_service.py` | `test_performance_end_to_end_query_under_300ms` in `tests/test_performance.py` | **PASS** |
| **NFR-02** (Disallowed Characters Protection) | AC-07 | T-04, T-05 | `CustomerSearchService.validate_query()` in `src/search_service.py`<br/>`CLI.run()` in `src/cli.py` | `test_validation_whitelist_rejects_disallowed_characters`, `test_validation_whitelist_accepts_allowed_symbols_and_latin_accents` in `tests/test_search_service.py`<br/>`test_cli_validation_invalid_character_error_exits_with_code_2` in `tests/test_cli.py` | **PASS** |
| **NFR-03** (Result Capping at 20) | AC-08 | T-03, CR-01 | `CustomerSearchService.search()` in `src/search_service.py` | `test_capping_limits_to_twenty_records`, `test_capping_exact_matches_prioritized_in_capping`, `test_capping_partial_id_matches_limits_to_twenty` in `tests/test_search_service.py` | **PASS** |
| **A-01** (Unique Customer ID) | Domain Model | T-01, T-02 | `Customer.id` in `src/models.py`<br/>`CustomerRepository.load_customers()` in `src/repository.py` | `test_load_customers_from_default_file` in `tests/test_repository.py` | **PASS** |
| **A-02** (Unique Email Address) | Domain Model | T-01, T-02 | `Customer.email` in `src/models.py`<br/>`CustomerRepository.load_customers()` in `src/repository.py` | `test_load_customers_from_default_file` in `tests/test_repository.py` | **PASS** |
| **A-03** (Latin Characters & Accents) | SR-02, VR-02 | T-01, T-03, T-04 | `CustomerSearchService.normalize()`, `validate_query()` in `src/search_service.py` | `test_normalization_strips_diacritics_and_lowercases`, `test_validation_whitelist_accepts_allowed_symbols_and_latin_accents` in `tests/test_search_service.py` | **PASS** |

---

## Contract & Specification Mapping

- **SR-01 (Target Fields)**: Implemented in `CustomerSearchService.search` -> Verified by `test_search_matches_*`.
- **SR-02 (Unicode NFD Normalization)**: Implemented in `CustomerSearchService.normalize` -> Verified by `test_normalization_*`.
- **SR-03 (Ranking & Deterministic Tie-breaking)**: Implemented in `CustomerSearchService.search` -> Verified by `test_ranking_*`.
- **SR-04 (Result Capping at 20)**: Implemented in `CustomerSearchService.search` -> Verified by `test_capping_*`.
- **SR-05 (Result Presentation)**: Implemented in `format_customer` in `src/cli.py` -> Verified by `test_format_customer_includes_all_required_attributes`.
- **VR-01 / EH-01 (Length Validation & Error)**: Implemented in `CustomerSearchService.validate_query` and `CLI.run` -> Verified by `test_validation_query_length_*` and `test_cli_validation_length_error_exits_with_code_2`.
- **VR-02 / EH-02 (Character Whitelist Validation & Error)**: Implemented in `CustomerSearchService.validate_query` and `CLI.run` -> Verified by `test_validation_whitelist_*` and `test_cli_validation_invalid_character_error_exits_with_code_2`.
- **EH-03 (Empty State)**: Implemented in `CLI.run` -> Verified by `test_empty_state_returns_empty_list` and `test_cli_empty_matches_returns_zero_and_prints_eh03_message`.
