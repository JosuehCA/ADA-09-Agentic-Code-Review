"""Tests for Customer domain model and CustomerRepository."""

from dataclasses import FrozenInstanceError
import json
import pytest

from src.models import Customer
from src.repository import CustomerRepository, RepositoryError


def test_customer_model_fields_and_full_name() -> None:
    """Customer entity holds required fields and computes full_name correctly."""
    customer = Customer(
        id="CUST-999",
        first_name="Ada",
        last_name="Lovelace",
        email="ada@example.com",
    )
    assert customer.id == "CUST-999"
    assert customer.first_name == "Ada"
    assert customer.last_name == "Lovelace"
    assert customer.email == "ada@example.com"
    assert customer.full_name == "Ada Lovelace"


def test_customer_model_is_immutable() -> None:
    """Customer entity is frozen and cannot be modified."""
    customer = Customer(
        id="CUST-999",
        first_name="Ada",
        last_name="Lovelace",
        email="ada@example.com",
    )
    with pytest.raises(FrozenInstanceError):
        customer.first_name = "Grace"  # type: ignore[misc]


def test_load_customers_from_default_file() -> None:
    """CustomerRepository loads default customers.json file successfully."""
    repo = CustomerRepository()
    customers = repo.load_customers()

    assert len(customers) == 25
    assert all(isinstance(c, Customer) for c in customers)

    # Validate A-01: IDs are unique
    ids = [c.id for c in customers]
    assert len(ids) == len(set(ids))

    # Validate A-02: Emails are unique
    emails = [c.email for c in customers]
    assert len(emails) == len(set(emails))

    # Verify first customer record
    first = customers[0]
    assert first.id == "CUST-001"
    assert first.first_name == "Carlos"
    assert first.last_name == "García"
    assert first.email == "carlos.garcia@example.com"
    assert first.full_name == "Carlos García"


def test_load_customers_from_custom_valid_file(tmp_path: pytest.TempPathFactory) -> None:
    """CustomerRepository loads records from a custom path."""
    data = [
        {"id": "1", "first_name": "Alan", "last_name": "Turing", "email": "alan@turing.org"},
        {"id": "2", "first_name": "Katherine", "last_name": "Johnson", "email": "katherine@nasa.gov"},
    ]
    file_path = tmp_path / "custom_customers.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    repo = CustomerRepository(file_path=file_path)
    customers = repo.load_customers()

    assert len(customers) == 2
    assert customers[0].full_name == "Alan Turing"
    assert customers[1].full_name == "Katherine Johnson"


def test_load_customers_missing_file(tmp_path: pytest.TempPathFactory) -> None:
    """CustomerRepository raises RepositoryError when file does not exist."""
    missing_file = tmp_path / "non_existent.json"
    repo = CustomerRepository(file_path=missing_file)

    with pytest.raises(RepositoryError, match="Customer data file not found"):
        repo.load_customers()


def test_load_customers_malformed_json(tmp_path: pytest.TempPathFactory) -> None:
    """CustomerRepository raises RepositoryError when JSON syntax is invalid."""
    malformed_file = tmp_path / "malformed.json"
    malformed_file.write_text("{ this is not valid json }", encoding="utf-8")
    repo = CustomerRepository(file_path=malformed_file)

    with pytest.raises(RepositoryError, match="Malformed customer JSON data"):
        repo.load_customers()


def test_load_customers_invalid_root_type(tmp_path: pytest.TempPathFactory) -> None:
    """CustomerRepository raises RepositoryError when root is not a list."""
    invalid_file = tmp_path / "dict_root.json"
    invalid_file.write_text(json.dumps({"id": "1"}), encoding="utf-8")
    repo = CustomerRepository(file_path=invalid_file)

    with pytest.raises(RepositoryError, match="Expected JSON array of customer records"):
        repo.load_customers()


def test_load_customers_invalid_record_type(tmp_path: pytest.TempPathFactory) -> None:
    """CustomerRepository raises RepositoryError when an element is not a dict."""
    invalid_file = tmp_path / "invalid_item.json"
    invalid_file.write_text(json.dumps(["not-a-dict"]), encoding="utf-8")
    repo = CustomerRepository(file_path=invalid_file)

    with pytest.raises(RepositoryError, match="expected JSON object"):
        repo.load_customers()


def test_load_customers_missing_required_fields(tmp_path: pytest.TempPathFactory) -> None:
    """CustomerRepository raises RepositoryError when required attributes are missing."""
    invalid_file = tmp_path / "missing_fields.json"
    invalid_file.write_text(
        json.dumps([{"id": "1", "first_name": "OnlyFirst"}]),
        encoding="utf-8",
    )
    repo = CustomerRepository(file_path=invalid_file)

    with pytest.raises(RepositoryError, match="missing required field\\(s\\): last_name, email"):
        repo.load_customers()
