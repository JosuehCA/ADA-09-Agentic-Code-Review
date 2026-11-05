"""Domain models for the customer search application."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """Immutable representation of a customer entity."""

    id: str
    first_name: str
    last_name: str
    email: str

    @property
    def full_name(self) -> str:
        """Computed full name composed of first and last name."""
        return f"{self.first_name} {self.last_name}"
