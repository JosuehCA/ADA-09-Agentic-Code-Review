"""Command-line interface for the customer search application."""

import argparse
import sys
from typing import Sequence, TextIO

from src.models import Customer
from src.repository import CustomerRepository, RepositoryError
from src.search_service import CustomerSearchService, ValidationError


def format_customer(customer: Customer) -> str:
    """Format a customer record for display (SR-05).

    Includes id, first_name, last_name, and email.
    """
    return f"[{customer.id}] {customer.first_name} {customer.last_name} - {customer.email}"


class CLI:
    """CLI handler for parsing arguments, invoking search service, and presenting output."""

    def __init__(
        self,
        service: CustomerSearchService | None = None,
        stdout: TextIO | None = None,
        stderr: TextIO | None = None,
    ) -> None:
        if service is None:
            repo = CustomerRepository()
            service = CustomerSearchService(repo)
        self.service = service
        self.stdout = stdout if stdout is not None else sys.stdout
        self.stderr = stderr if stderr is not None else sys.stderr

    def run(self, argv: Sequence[str] | None = None) -> int:
        """Execute command-line search flow.

        Returns:
            int: 0 on success or empty matches, 2 on validation or argument errors, 1 on repository failure.
        """
        parser = argparse.ArgumentParser(
            prog="python -m src.cli",
            description="Search customers by first name, last name, email, or customer ID.",
        )
        parser.add_argument("query", help="Search term (minimum 3 non-whitespace characters)")

        # Capture argparse error output to self.stderr
        try:
            # We redirect sys.stderr temporarily if self.stderr is custom and argv fails
            original_stderr = sys.stderr
            sys.stderr = self.stderr
            try:
                args = parser.parse_args(argv)
            finally:
                sys.stderr = original_stderr
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 2

        query = args.query

        try:
            results = self.service.search(query)
        except ValidationError as exc:
            print(str(exc), file=self.stderr)
            return 2
        except RepositoryError as exc:
            print(f"Error: {exc}", file=self.stderr)
            return 1

        if not results:
            print(f"No customers found matching '{query}'.", file=self.stdout)
            return 0

        for customer in results:
            print(format_customer(customer), file=self.stdout)
        return 0


def main() -> None:
    """Main entrypoint for CLI execution."""
    cli = CLI()
    exit_code = cli.run(sys.argv[1:])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
