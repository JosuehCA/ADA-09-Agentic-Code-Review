"""Performance benchmark tests asserting latency requirements (NFR-01, AC-06, TS-09)."""

import io
import json
import time
from pathlib import Path
import pytest

from src.cli import CLI
from src.repository import CustomerRepository
from src.search_service import CustomerSearchService


@pytest.fixture
def thousand_records_dataset(tmp_path: Path) -> Path:
    """Generate a temporary dataset with 1,000 valid customer records."""
    records = []
    first_names = ["Carlos", "María", "José", "Ana", "David", "Lucía", "Sofía", "John", "Mateo", "Camila"]
    last_names = ["García", "Rodríguez", "Hernández", "López", "González", "Pérez", "Sánchez", "Smith", "Díaz", "Peña"]

    for i in range(1, 1001):
        first = first_names[i % len(first_names)]
        last = last_names[(i // len(first_names)) % len(last_names)]
        records.append(
            {
                "id": f"PERF-{i:04d}",
                "first_name": first,
                "last_name": last,
                "email": f"perf.user{i:04d}.{first.lower()}@domain{i % 10}.com",
            }
        )

    dataset_path = tmp_path / "customers_1000.json"
    dataset_path.write_text(json.dumps(records), encoding="utf-8")
    return dataset_path


def test_performance_end_to_end_query_under_300ms(thousand_records_dataset: Path) -> None:
    """End-to-end query execution completes in <= 300 ms on 1,000 records (AC-06, NFR-01)."""
    repo = CustomerRepository(file_path=thousand_records_dataset)
    service = CustomerSearchService(repo)
    out, err = io.StringIO(), io.StringIO()
    cli = CLI(service=service, stdout=out, stderr=err)

    test_queries = [
        "Carlos",               # Exact match on first_name
        "García",               # Exact match on last_name
        "Carlos García",        # Multi-word match on full_name
        "perf.user0500",        # Partial email match
        "NonexistentRecord",    # Empty-state query
    ]

    for query in test_queries:
        out.seek(0)
        out.truncate(0)

        start_time = time.perf_counter()
        exit_code = cli.run([query])
        elapsed_seconds = time.perf_counter() - start_time

        assert exit_code == 0, f"Query '{query}' failed with non-zero exit code {exit_code}"
        assert (
            elapsed_seconds <= 0.300
        ), f"Query '{query}' took {elapsed_seconds * 1000:.2f} ms, exceeding 300 ms limit"
