"""Data access layer for customer persistence."""

import json
from pathlib import Path
from typing import Protocol

from src.models import Customer


class RepositoryError(Exception):
    """Raised when loading or parsing customer data fails."""
    pass


class CustomerRepositoryInterface(Protocol):
    """Protocol defining the repository contract for customer retrieval."""

    def load_customers(self) -> list[Customer]:
        """Load and return all customer records."""
        ...


class CustomerRepository:
    """Repository implementation for loading customer entities from a local JSON file."""

    def __init__(self, file_path: str | Path = "data/customers.json") -> None:
        self.file_path = Path(file_path)

    def load_customers(self) -> list[Customer]:
        """Deserialize and return customer records from the JSON file.

        Raises:
            RepositoryError: If the file does not exist, cannot be read, contains
                             malformed JSON, or does not conform to the expected schema.
        """
        if not self.file_path.exists():
            raise RepositoryError(f"Customer data file not found: {self.file_path}")

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise RepositoryError(f"Malformed customer JSON data in {self.file_path}: {exc}") from exc
        except OSError as exc:
            raise RepositoryError(f"Error reading customer data from {self.file_path}: {exc}") from exc

        if not isinstance(data, list):
            raise RepositoryError(
                f"Expected JSON array of customer records in {self.file_path}, got {type(data).__name__}"
            )

        customers: list[Customer] = []
        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise RepositoryError(
                    f"Invalid record at index {index}: expected JSON object, got {type(item).__name__}"
                )

            required_fields = ("id", "first_name", "last_name", "email")
            missing_fields = [field for field in required_fields if field not in item]
            if missing_fields:
                raise RepositoryError(
                    f"Invalid record at index {index}: missing required field(s): {', '.join(missing_fields)}"
                )

            customers.append(
                Customer(
                    id=str(item["id"]),
                    first_name=str(item["first_name"]),
                    last_name=str(item["last_name"]),
                    email=str(item["email"]),
                )
            )

        return customers
