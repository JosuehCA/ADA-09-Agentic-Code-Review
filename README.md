# Customer Search Feature

A lightweight, spec-driven command-line customer search application designed with modular architecture, deterministic ranking, Unicode diacritic-insensitive matching, and robust input validation.

---

## Architecture Overview

The system follows a layered architecture with clean separation of concerns:

- **Presentation Layer (`src/cli.py`)**: Handles CLI arguments via `argparse`, prints formatted customer records to `stdout`, directs error messages to `stderr`, and maps outcomes to standard exit codes (`0`, `1`, `2`).
- **Domain Layer (`src/search_service.py`)**: Encapsulates query validation (length and character whitelist), Unicode NFD normalization, multi-field matching, multi-tier ranking (exact over partial), deterministic tie-breaking, and result capping.
- **Persistence Layer (`src/repository.py`)**: Deserializes customer entities from `data/customers.json` with robust error handling for missing or malformed data files.
- **Domain Model (`src/models.py`)**: Defines the immutable `Customer` dataclass with `id`, `first_name`, `last_name`, `email`, and computed `full_name`.

---

## Requirements & Environment Setup

- **Python**: Version 3.11+
- **Runtime Dependencies**: Python standard library only (`unicodedata`, `argparse`, `json`, `pathlib`, etc.)
- **Development & Testing**: `pytest`

### Quick Start

1. Ensure Python 3.11+ and `pytest` are installed:
   ```bash
   python3 --version
   pytest --version
   ```

2. Verify project structure:
   ```bash
   ls data/customers.json src/ tests/
   ```

---

## CLI Usage

Run searches using the Python module execution syntax:

```bash
python -m src.cli "<query>"
```

### Examples

1. **Exact & Partial Name Search**:
   ```bash
   python -m src.cli "Carlos"
   # Output: [CUST-001] Carlos García - carlos.garcia@example.com
   ```

2. **Accented and Case-Insensitive Matching**:
   Search matching is diacritic-insensitive and case-insensitive:
   ```bash
   python -m src.cli "jose"
   # Output: [CUST-003] José Hernández - jose.hernandez@example.com

   python -m src.cli "JOSÉ"
   # Output: [CUST-003] José Hernández - jose.hernandez@example.com
   ```

3. **Multi-Word Search**:
   Multi-word queries match continuously against computed full names:
   ```bash
   python -m src.cli "Carlos García"
   # Output: [CUST-001] Carlos García - carlos.garcia@example.com
   ```

4. **Email Search**:
   ```bash
   python -m src.cli "example.com"
   # Displays up to 20 matching records with example.com email addresses
   ```

5. **Customer ID Search (Exact & Partial)**:
   Search matching supports exact and partial customer IDs:
   ```bash
   # Exact customer ID match
   python -m src.cli "CUST-001"
   # Output: [CUST-001] Carlos García - carlos.garcia@example.com

   # Partial customer ID match
   python -m src.cli "001"
   # Output: [CUST-001] Carlos García - carlos.garcia@example.com
   ```

6. **Zero Matches State (Exit Code 0)**:
   ```bash
   python -m src.cli "NonexistentUser"
   # Output: No customers found matching 'NonexistentUser'.
   ```

7. **Input Validation Errors (Exit Code 2)**:
   - Query too short (< 3 non-whitespace characters):
     ```bash
     python -m src.cli "ab"
     # Stderr: Error: Search query must contain at least 3 non-whitespace characters.
     ```
   - Disallowed characters:
     ```bash
     python -m src.cli "user*name"
     # Stderr: Error: Query contains invalid characters. Allowed symbols: @ . _ - ' and alphanumeric characters.
     ```

---

## Exit Codes

| Exit Code | Description |
| :---: | :--- |
| **0** | Successful execution (matches found or zero matches empty state). |
| **1** | Repository/persistence failure (missing or malformed data file). |
| **2** | Input validation error (query length, forbidden characters, or missing arguments). |

---

## Testing

Execute the test suites with `pytest`:

```bash
# Run all unit, integration, CLI, and performance tests
pytest -v

# Run domain repository tests
pytest tests/test_repository.py -v

# Run search and validation tests
pytest tests/test_search_service.py -v

# Run CLI presentation and subprocess tests
pytest tests/test_cli.py -v

# Run latency performance benchmark (< 300 ms on 1,000 records)
pytest tests/test_performance.py -v
```

---

## Documentation & Traceability

- [REQUIREMENTS.md](REQUIREMENTS.md): Functional and non-functional requirements.
- [SPEC.md](SPEC.md): Technical specification, business rules, and acceptance criteria.
- [ARCHITECTURE.md](ARCHITECTURE.md): Component responsibilities, data flow, and interfaces.
- [TASKS.md](TASKS.md): Step-by-step implementation tasks.
- [docs/traceability.md](docs/traceability.md): Requirements to tests traceability matrix.
- [results/agent-report.md](results/agent-report.md): Execution summary, problem resolutions, and review logs.
