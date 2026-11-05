"""Domain service implementing customer search, normalization, and ranking."""

import unicodedata

from src.models import Customer
from src.repository import CustomerRepositoryInterface


class ValidationError(Exception):
    """Raised when search query violates validation rules."""
    pass


ALLOWED_SYMBOLS: set[str] = {"@", ".", "_", "-", "'"}
ERROR_MIN_LENGTH: str = "Error: Search query must contain at least 3 non-whitespace characters."
ERROR_INVALID_CHARS: str = (
    "Error: Query contains invalid characters. Allowed symbols: @ . _ - ' and alphanumeric characters."
)


class CustomerSearchService:
    """Service encapsulating customer search matching, ranking, and normalization logic."""

    def __init__(self, repository: CustomerRepositoryInterface) -> None:
        self.repository = repository

    @staticmethod
    def normalize(text: str) -> str:
        """Strip diacritical marks via Unicode NFD decomposition and convert to lowercase.

        Preserves base Latin characters, digits, whitespace, and punctuation.
        """
        nfd_text = unicodedata.normalize("NFD", text)
        stripped = "".join(char for char in nfd_text if unicodedata.category(char) != "Mn")
        return stripped.lower()

    def validate_query(self, query: str) -> None:
        """Validate search query length and allowed characters according to VR-01 and VR-02.

        Raises:
            ValidationError: If query has fewer than 3 non-whitespace characters (EH-01)
                             or contains characters outside the whitelist (EH-02).
        """
        trimmed = query.strip()
        non_whitespace_count = sum(1 for c in trimmed if not c.isspace())

        if len(trimmed) < 3 or non_whitespace_count < 3:
            raise ValidationError(ERROR_MIN_LENGTH)

        for char in query:
            if char.isspace() or char in ALLOWED_SYMBOLS:
                continue
            base = "".join(c for c in unicodedata.normalize("NFD", char) if unicodedata.category(c) != "Mn")
            if not (base.isascii() and base.isalnum()):
                raise ValidationError(ERROR_INVALID_CHARS)

    def search(self, query: str) -> list[Customer]:
        """Search and rank customer records according to domain search rules.

        1. Normalizes query and target fields (NFD decomposition, lowercase).
        2. Segregates results into exact matches and partial matches.
        3. Deterministically resolves ties by last_name, first_name, and id.
        4. Caps output at a maximum of 20 records.
        """
        self.validate_query(query)

        trimmed_query = query.strip()
        normalized_query = self.normalize(trimmed_query)

        customers = self.repository.load_customers()

        exact_matches: list[Customer] = []
        partial_matches: list[Customer] = []

        for customer in customers:
            norm_id = self.normalize(customer.id)
            norm_first = self.normalize(customer.first_name)
            norm_last = self.normalize(customer.last_name)
            norm_full = self.normalize(customer.full_name)
            norm_email = self.normalize(customer.email)

            if normalized_query in (norm_id, norm_first, norm_last, norm_full, norm_email):
                exact_matches.append(customer)
            elif (
                normalized_query in norm_id
                or normalized_query in norm_full
                or normalized_query in norm_email
            ):
                partial_matches.append(customer)

        # Deterministic tie-breaking: sort ascending alphabetically by last_name, then first_name, then id
        exact_matches.sort(
            key=lambda c: (self.normalize(c.last_name), c.last_name, self.normalize(c.first_name), c.first_name, c.id)
        )
        partial_matches.sort(
            key=lambda c: (self.normalize(c.last_name), c.last_name, self.normalize(c.first_name), c.first_name, c.id)
        )

        ranked_results = exact_matches + partial_matches
        return ranked_results[:20]
