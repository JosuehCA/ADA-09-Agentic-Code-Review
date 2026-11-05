"""Integration and unit tests for the CLI presentation interface."""

import io
import subprocess
import sys
import pytest

from src.cli import CLI, format_customer
from src.models import Customer
from src.repository import CustomerRepositoryInterface, RepositoryError
from src.search_service import (
    CustomerSearchService,
    ERROR_INVALID_CHARS,
    ERROR_MIN_LENGTH,
)


class InMemoryCustomerRepository(CustomerRepositoryInterface):
    """In-memory stub repository for CLI testing."""

    def __init__(self, customers: list[Customer] | None = None) -> None:
        self._customers = customers if customers is not None else []

    def load_customers(self) -> list[Customer]:
        return list(self._customers)


class FailingCustomerRepository(CustomerRepositoryInterface):
    """Stub repository that simulates a persistence failure."""

    def load_customers(self) -> list[Customer]:
        raise RepositoryError("Customer data file not found: non_existent.json")


@pytest.fixture
def sample_service() -> CustomerSearchService:
    customers = [
        Customer(id="CUST-001", first_name="Carlos", last_name="García", email="carlos.garcia@example.com"),
        Customer(id="CUST-002", first_name="María", last_name="Rodríguez", email="maria.r@example.com"),
    ]
    return CustomerSearchService(InMemoryCustomerRepository(customers))


# ============================================================================
# Formatting Tests (SR-05)
# ============================================================================

def test_format_customer_includes_all_required_attributes() -> None:
    """Formatted record contains id, first_name, last_name, and email."""
    customer = Customer(
        id="CUST-100",
        first_name="Ada",
        last_name="Lovelace",
        email="ada@computing.org",
    )
    formatted = format_customer(customer)
    assert "CUST-100" in formatted
    assert "Ada" in formatted
    assert "Lovelace" in formatted
    assert "ada@computing.org" in formatted


# ============================================================================
# CLI Execution & Exit Code Tests (AC-01, AC-02, AC-04, AC-07)
# ============================================================================

def test_cli_successful_search_returns_zero_and_prints_records(sample_service: CustomerSearchService) -> None:
    """CLI outputs matching records to stdout and exits with code 0."""
    out, err = io.StringIO(), io.StringIO()
    cli = CLI(service=sample_service, stdout=out, stderr=err)

    exit_code = cli.run(["Carlos"])

    assert exit_code == 0
    stdout_content = out.getvalue()
    assert "[CUST-001] Carlos García - carlos.garcia@example.com" in stdout_content
    assert err.getvalue() == ""


def test_cli_search_by_customer_id(sample_service: CustomerSearchService) -> None:
    """CLI searches by customer ID and outputs matching records (CR-01)."""
    out, err = io.StringIO(), io.StringIO()
    cli = CLI(service=sample_service, stdout=out, stderr=err)

    exit_code = cli.run(["CUST-001"])

    assert exit_code == 0
    assert "[CUST-001] Carlos García - carlos.garcia@example.com" in out.getvalue()
    assert err.getvalue() == ""


def test_cli_search_by_partial_customer_id(sample_service: CustomerSearchService) -> None:
    """CLI searches by customer ID substring and outputs matching records (RF-04)."""
    out, err = io.StringIO(), io.StringIO()
    cli = CLI(service=sample_service, stdout=out, stderr=err)

    exit_code = cli.run(["001"])

    assert exit_code == 0
    assert "[CUST-001] Carlos García - carlos.garcia@example.com" in out.getvalue()
    assert err.getvalue() == ""


def test_cli_empty_matches_returns_zero_and_prints_eh03_message(sample_service: CustomerSearchService) -> None:
    """CLI prints EH-03 empty-state message to stdout and exits with code 0 (AC-04)."""
    out, err = io.StringIO(), io.StringIO()
    cli = CLI(service=sample_service, stdout=out, stderr=err)

    exit_code = cli.run(["Nonexistent"])

    assert exit_code == 0
    assert out.getvalue().strip() == "No customers found matching 'Nonexistent'."
    assert err.getvalue() == ""


def test_cli_validation_length_error_exits_with_code_2(sample_service: CustomerSearchService) -> None:
    """Query with fewer than 3 non-whitespace chars outputs EH-01 to stderr and exits with 2 (AC-02)."""
    out, err = io.StringIO(), io.StringIO()
    cli = CLI(service=sample_service, stdout=out, stderr=err)

    exit_code = cli.run(["ab"])

    assert exit_code == 2
    assert out.getvalue() == ""
    assert err.getvalue().strip() == ERROR_MIN_LENGTH


def test_cli_validation_invalid_character_error_exits_with_code_2(sample_service: CustomerSearchService) -> None:
    """Query with disallowed characters outputs EH-02 to stderr and exits with 2 (AC-07)."""
    out, err = io.StringIO(), io.StringIO()
    cli = CLI(service=sample_service, stdout=out, stderr=err)

    exit_code = cli.run(["carlos!"])

    assert exit_code == 2
    assert out.getvalue() == ""
    assert err.getvalue().strip() == ERROR_INVALID_CHARS


def test_cli_missing_argument_exits_with_code_2(sample_service: CustomerSearchService) -> None:
    """CLI invoked without search query argument exits with code 2."""
    out, err = io.StringIO(), io.StringIO()
    cli = CLI(service=sample_service, stdout=out, stderr=err)

    exit_code = cli.run([])

    assert exit_code == 2


def test_cli_repository_error_exits_with_code_1() -> None:
    """Persistence failure reports error to stderr and exits with code 1."""
    failing_service = CustomerSearchService(FailingCustomerRepository())
    out, err = io.StringIO(), io.StringIO()
    cli = CLI(service=failing_service, stdout=out, stderr=err)

    exit_code = cli.run(["Carlos"])

    assert exit_code == 1
    assert "Error: Customer data file not found" in err.getvalue()


# ============================================================================
# Subprocess End-to-End Tests (python -m src.cli ...)
# ============================================================================

def test_subprocess_cli_search_success() -> None:
    """Subprocess execution with valid match exits with 0 and prints results."""
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "Carlos"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Carlos García" in result.stdout
    assert result.stderr == ""


def test_subprocess_cli_empty_state() -> None:
    """Subprocess execution with unmatched valid query exits with 0 and EH-03 message."""
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "NobodyMatching"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "No customers found matching 'NobodyMatching'."
    assert result.stderr == ""


def test_subprocess_cli_length_error() -> None:
    """Subprocess execution with short query exits with 2 and EH-01 message."""
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "ab"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert ERROR_MIN_LENGTH in result.stderr


def test_subprocess_cli_invalid_characters_error() -> None:
    """Subprocess execution with invalid characters exits with 2 and EH-02 message."""
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "user*name"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert ERROR_INVALID_CHARS in result.stderr


def test_subprocess_cli_search_by_id() -> None:
    """Subprocess execution searching by customer ID exits with 0 and prints results."""
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "CUST-001"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "[CUST-001] Carlos García - carlos.garcia@example.com" in result.stdout
    assert result.stderr == ""
