"""Unit and integration tests for CustomerSearchService."""

import pytest

from src.models import Customer
from src.repository import CustomerRepositoryInterface
from src.search_service import (
    CustomerSearchService,
    ERROR_INVALID_CHARS,
    ERROR_MIN_LENGTH,
    ValidationError,
)


class InMemoryCustomerRepository(CustomerRepositoryInterface):
    """Test double for CustomerRepositoryInterface with in-memory records."""

    def __init__(self, customers: list[Customer] | None = None) -> None:
        self._customers = customers if customers is not None else []

    def load_customers(self) -> list[Customer]:
        return list(self._customers)


# ============================================================================
# Normalization Tests (AC-03, SR-02, FR-04)
# ============================================================================

def test_normalization_strips_diacritics_and_lowercases() -> None:
    """Normalization strips combining diacritical marks and converts to lowercase."""
    repo = InMemoryCustomerRepository([])
    service = CustomerSearchService(repo)

    assert service.normalize("José") == "jose"
    assert service.normalize("GARCÍA") == "garcia"
    assert service.normalize("Peña") == "pena"
    assert service.normalize("MÜLLER") == "muller"
    assert service.normalize("áéíóúÁÉÍÓÚñÑ") == "aeiouaeiounn"


def test_normalization_preserves_allowed_punctuation() -> None:
    """Normalization preserves symbols like '@', '.', '_', '-', and '''."""
    repo = InMemoryCustomerRepository([])
    service = CustomerSearchService(repo)

    assert service.normalize("user.name-test_01@domain.com") == "user.name-test_01@domain.com"
    assert service.normalize("O'Connor") == "o'connor"


# ============================================================================
# Search Matching Tests (AC-01, SR-01, FR-01, FR-02)
# ============================================================================

@pytest.fixture
def sample_customers() -> list[Customer]:
    return [
        Customer(id="1", first_name="Carlos", last_name="García", email="carlos.garcia@example.com"),
        Customer(id="2", first_name="María", last_name="Rodríguez", email="maria.r@example.com"),
        Customer(id="3", first_name="José", last_name="Hernández", email="jose.h@example.com"),
        Customer(id="4", first_name="Ana", last_name="Martínez", email="ana.m@example.com"),
        Customer(id="5", first_name="Giancarlos", last_name="Silva", email="gian@example.com"),
        Customer(id="6", first_name="John", last_name="Doe", email="jdoe@example.com"),
    ]


def test_search_matches_first_name(sample_customers: list[Customer]) -> None:
    """Matches query against first_name exactly and partially."""
    repo = InMemoryCustomerRepository(sample_customers)
    service = CustomerSearchService(repo)

    results = service.search("Ana")
    assert len(results) == 1
    assert results[0].id == "4"

    results_partial = service.search("Mar")
    assert any(c.id == "2" for c in results_partial)


def test_search_matches_last_name(sample_customers: list[Customer]) -> None:
    """Matches query against last_name."""
    repo = InMemoryCustomerRepository(sample_customers)
    service = CustomerSearchService(repo)

    results = service.search("García")
    assert len(results) == 1
    assert results[0].id == "1"


def test_search_matches_full_name(sample_customers: list[Customer]) -> None:
    """Matches continuous substring across computed full_name."""
    repo = InMemoryCustomerRepository(sample_customers)
    service = CustomerSearchService(repo)

    results = service.search("John Doe")
    assert len(results) == 1
    assert results[0].id == "6"

    results_partial = service.search("hn Do")
    assert len(results_partial) == 1
    assert results_partial[0].id == "6"


def test_search_matches_email(sample_customers: list[Customer]) -> None:
    """Matches query against email address."""
    repo = InMemoryCustomerRepository(sample_customers)
    service = CustomerSearchService(repo)

    results_exact = service.search("jdoe@example.com")
    assert len(results_exact) == 1
    assert results_exact[0].id == "6"

    results_domain = service.search("example.com")
    assert len(results_domain) == len(sample_customers)


def test_search_matches_customer_id_exact() -> None:
    """Matches query against customer ID exactly (case-insensitive)."""
    customers = [
        Customer(id="CUST-001", first_name="Carlos", last_name="García", email="carlos.garcia@example.com"),
        Customer(id="CUST-002", first_name="María", last_name="Rodríguez", email="maria.r@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers)
    service = CustomerSearchService(repo)

    # Exact query matching customer ID
    results = service.search("CUST-001")
    assert len(results) == 1
    assert results[0].id == "CUST-001"

    # Case-insensitive exact matching
    results_lower = service.search("cust-001")
    assert len(results_lower) == 1
    assert results_lower[0].id == "CUST-001"


def test_search_matches_customer_id_partial() -> None:
    """Matches query against customer ID substring in partial tier."""
    customers = [
        Customer(id="CUST-001", first_name="Carlos", last_name="García", email="carlos.garcia@example.com"),
        Customer(id="CUST-002", first_name="María", last_name="Rodríguez", email="maria.r@example.com"),
        Customer(id="USER-999", first_name="John", last_name="Doe", email="jdoe@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers)
    service = CustomerSearchService(repo)

    # Substring match on numeric ID portion
    results = service.search("001")
    assert len(results) == 1
    assert results[0].id == "CUST-001"

    # Substring match on prefix portion
    results_prefix = service.search("CUST")
    assert len(results_prefix) == 2
    assert {c.id for c in results_prefix} == {"CUST-001", "CUST-002"}


def test_search_diacritic_and_case_insensitive(sample_customers: list[Customer]) -> None:
    """Queries match regardless of casing or diacritic differences."""
    repo = InMemoryCustomerRepository(sample_customers)
    service = CustomerSearchService(repo)

    # Accent in target ('José'), unaccented in query ('jose')
    results = service.search("jose")
    assert any(c.id == "3" for c in results)

    # All-caps accented query ('JOSÉ')
    results_caps = service.search("JOSÉ")
    assert any(c.id == "3" for c in results_caps)

    # Accent in target ('García'), unaccented search ('garcia')
    results_garcia = service.search("garcia")
    assert any(c.id == "1" for c in results_garcia)


# ============================================================================
# Ranking & Tie-breaking Tests (AC-05, SR-03, FR-06)
# ============================================================================

def test_ranking_exact_matches_precede_partial_matches() -> None:
    """Exact matches strictly precede partial matches."""
    customers = [
        Customer(id="1", first_name="Giancarlos", last_name="Silva", email="gian@example.com"),
        Customer(id="2", first_name="Carlos", last_name="García", email="carlos.garcia@example.com"),
        Customer(id="3", first_name="Juan", last_name="Carlos", email="juan.carlos@example.com"),
        Customer(id="4", first_name="Ana", last_name="Carlos-Soto", email="ana.c@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers)
    service = CustomerSearchService(repo)

    # Searching "Carlos":
    # - Customer 2 (Carlos García): exact match on first_name
    # - Customer 3 (Juan Carlos): exact match on last_name
    # - Customer 1 (Giancarlos Silva): partial match (substring of full_name)
    # - Customer 4 (Ana Carlos-Soto): partial match (substring of full_name)
    results = service.search("Carlos")

    assert len(results) == 4
    # Exact matches must come first
    exact_ids = {results[0].id, results[1].id}
    assert exact_ids == {"2", "3"}

    # Partial matches must follow
    partial_ids = {results[2].id, results[3].id}
    assert partial_ids == {"1", "4"}


def test_ranking_tie_breaking_order() -> None:
    """Ties within the same match tier sort by last_name, first_name, then id."""
    customers = [
        Customer(id="3", first_name="Carlos", last_name="Zúñiga", email="c1@example.com"),
        Customer(id="2", first_name="Carlos", last_name="Álvarez", email="c2@example.com"),
        Customer(id="5", first_name="Bob", last_name="Smith", email="b.smith@example.com"),
        Customer(id="4", first_name="Alice", last_name="Smith", email="a.smith@example.com"),
        Customer(id="7", first_name="Alice", last_name="Smith", email="a7.smith@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers)
    service = CustomerSearchService(repo)

    # Searching "Carlos" -> exact matches on first_name for id="2" (Álvarez) and id="3" (Zúñiga)
    results = service.search("Carlos")
    assert [c.id for c in results] == ["2", "3"]

    # Searching "Smith" -> exact matches on last_name:
    # 1. Alice Smith (id=4) vs Alice Smith (id=7) -> same last and first -> sorted by id ("4" < "7")
    # 2. Bob Smith (id=5) -> sorted after Alice Smith
    results_smith = service.search("Smith")
    assert [c.id for c in results_smith] == ["4", "7", "5"]


def test_ranking_exact_id_matches_precede_partial_matches() -> None:
    """Exact customer ID match strictly precedes partial matches."""
    customers = [
        Customer(id="CUST-0010", first_name="Bob", last_name="Brown", email="bob@example.com"),
        Customer(id="CUST-001", first_name="Alice", last_name="Smith", email="alice@example.com"),
        Customer(id="CUST-002", first_name="CUST-001-Nick", last_name="Davis", email="davis@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers)
    service = CustomerSearchService(repo)

    # Searching "CUST-001":
    # - Customer CUST-001: exact match on id
    # - Customer CUST-0010: partial match on id ("CUST-001" in "CUST-0010")
    # - Customer CUST-002: partial match on full_name ("CUST-001" in "CUST-001-Nick Davis")
    results = service.search("CUST-001")
    assert len(results) == 3
    assert results[0].id == "CUST-001"  # Exact match tier
    assert {results[1].id, results[2].id} == {"CUST-0010", "CUST-002"}  # Partial match tier


def test_ranking_exact_name_precedes_partial_id_match() -> None:
    """Exact name match strictly precedes partial ID match."""
    customers = [
        Customer(id="CUST-100", first_name="Alice", last_name="Smith", email="alice@example.com"),
        Customer(id="OTHER-99", first_name="Cust", last_name="Jones", email="cust@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers)
    service = CustomerSearchService(repo)

    # Searching "Cust":
    # - OTHER-99: exact match on first_name ("Cust")
    # - CUST-100: partial match on id ("Cust" in "CUST-100")
    results = service.search("Cust")
    assert len(results) == 2
    assert results[0].id == "OTHER-99"
    assert results[1].id == "CUST-100"


def test_ranking_id_partial_matches_tie_breaking() -> None:
    """Partial ID matches resolve ties by last_name, first_name, then id."""
    customers = [
        Customer(id="CUST-901", first_name="Zachary", last_name="Adams", email="z.adams@example.com"),
        Customer(id="CUST-902", first_name="Abigail", last_name="Adams", email="a.adams@example.com"),
        Customer(id="CUST-903", first_name="Bob", last_name="Baker", email="b.baker@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers)
    service = CustomerSearchService(repo)

    results = service.search("CUST")
    assert [c.id for c in results] == ["CUST-902", "CUST-901", "CUST-903"]


# ============================================================================
# Result Capping Tests (AC-08, SR-04, NFR-03)
# ============================================================================

def test_capping_limits_to_twenty_records() -> None:
    """When more than 20 records match, exactly the top 20 are returned."""
    # 25 customers all sharing partial match 'test'
    customers = [
        Customer(
            id=f"{i:02d}",
            first_name=f"Customer{i:02d}",
            last_name="TestGroup",
            email=f"user{i:02d}@testgroup.com",
        )
        for i in range(1, 26)
    ]
    repo = InMemoryCustomerRepository(customers)
    service = CustomerSearchService(repo)

    results = service.search("TestGroup")
    assert len(results) == 20


def test_capping_exact_matches_prioritized_in_capping() -> None:
    """When capping occurs, exact matches take priority over partial matches."""
    exact_matches = [
        Customer(id=f"exact_{i:02d}", first_name="Match", last_name=f"Exact{i:02d}", email=f"ex{i}@test.com")
        for i in range(15)
    ]
    partial_matches = [
        Customer(id=f"partial_{i:02d}", first_name="MatchingPrefix", last_name=f"Partial{i:02d}", email=f"part{i}@test.com")
        for i in range(15)
    ]
    repo = InMemoryCustomerRepository(exact_matches + partial_matches)
    service = CustomerSearchService(repo)

    results = service.search("Match")
    assert len(results) == 20

    # All 15 exact matches must be present in the capped 20 results
    returned_exact_count = sum(1 for c in results if c.id.startswith("exact_"))
    assert returned_exact_count == 15

    # Exactly 5 partial matches should fill the remainder
    returned_partial_count = sum(1 for c in results if c.id.startswith("partial_"))
    assert returned_partial_count == 5


# ============================================================================
# Validation & Error Tests (AC-02, AC-07, AC-04, VR-01, VR-02, EH-01, EH-02)
# ============================================================================

@pytest.mark.parametrize(
    "invalid_query",
    [
        "",
        "a",
        "ab",
        "  ",
        "   ",
        " ab ",
        "a b",
        "  a  ",
    ],
)
def test_validation_query_length_rejects_fewer_than_three_characters(invalid_query: str) -> None:
    """Queries with fewer than 3 non-whitespace characters raise ValidationError with EH-01 message."""
    service = CustomerSearchService(InMemoryCustomerRepository([]))

    with pytest.raises(ValidationError) as exc_info:
        service.search(invalid_query)

    assert str(exc_info.value) == ERROR_MIN_LENGTH


@pytest.mark.parametrize(
    "valid_query",
    [
        "Ana",
        "  Ana  ",
        "123",
        "a b c",
        "   carlos   ",
    ],
)
def test_validation_query_length_accepts_valid_length(valid_query: str) -> None:
    """Queries with at least 3 non-whitespace characters pass length validation."""
    service = CustomerSearchService(InMemoryCustomerRepository([]))
    # Should not raise ValidationError for length
    try:
        service.validate_query(valid_query)
    except ValidationError as e:
        pytest.fail(f"validate_query unexpectedly raised ValidationError on '{valid_query}': {e}")


@pytest.mark.parametrize(
    "forbidden_query",
    [
        "carlos!",
        "user#1",
        "admin$",
        "100%",
        "john*doe",
        "select;",
        "<script>",
        "test/query",
        "what?",
        'name"test',
        "hello+world",
        "query=test",
        "drop table customers;--",
        "greek_αβγ",
        "cyrillic_д",
        "chinese_中文",
        "emoji_😀",
    ],
)
def test_validation_whitelist_rejects_disallowed_characters(forbidden_query: str) -> None:
    """Queries containing disallowed characters raise ValidationError with EH-02 message."""
    service = CustomerSearchService(InMemoryCustomerRepository([]))

    with pytest.raises(ValidationError) as exc_info:
        service.search(forbidden_query)

    assert str(exc_info.value) == ERROR_INVALID_CHARS


@pytest.mark.parametrize(
    "valid_query",
    [
        "Carlos",
        "José",
        "María",
        "Peña",
        "Müller",
        "Álvarez",
        "O'Connor",
        "user.name-test_01@domain.com",
        "John-Paul",
        "first_second",
        "test.email@corp-domain.org",
        "a b c",
    ],
)
def test_validation_whitelist_accepts_allowed_symbols_and_latin_accents(valid_query: str) -> None:
    """Queries containing Latin accented letters, whitespace, and allowed symbols pass validation."""
    service = CustomerSearchService(InMemoryCustomerRepository([]))
    try:
        service.validate_query(valid_query)
    except ValidationError as e:
        pytest.fail(f"validate_query unexpectedly rejected valid query '{valid_query}': {e}")


def test_empty_state_returns_empty_list() -> None:
    """Valid query matching zero records returns an empty list without error."""
    customers = [
        Customer(id="1", first_name="Carlos", last_name="García", email="carlos@example.com"),
    ]
    service = CustomerSearchService(InMemoryCustomerRepository(customers))

    results = service.search("NonexistentTerm")
    assert results == []

