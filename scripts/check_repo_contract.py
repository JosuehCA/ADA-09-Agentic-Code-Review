from pathlib import Path
import sys

required = [
    "AGENTS.md",
    "README.md",
    "REQUIREMENTS.md",
    "SPEC.md",
    "ARCHITECTURE.md",
    "TASKS.md",
    "docs/REPO_MAP.md",
    "scripts/verify_repo.sh",
]

missing = [path for path in required if not Path(path).exists()]

if missing:
    print("REPO_CONTRACT: FAIL")
    for path in missing:
        print(f"Missing required file: {path}")
    sys.exit(1)

# Check required directories
required_dirs = ["src", "tests", "docs", "scripts", "results", "data"]
missing_dirs = [d for d in required_dirs if not Path(d).is_dir()]
if missing_dirs:
    print("REPO_CONTRACT: FAIL")
    for d in missing_dirs:
        print(f"Missing required directory: {d}")
    sys.exit(1)

# Check protected baseline fixture data exists
if not Path("data/customers.json").exists():
    print("REPO_CONTRACT: FAIL - Missing baseline fixture data/customers.json")
    sys.exit(1)

print("REPO_CONTRACT: PASS")
sys.exit(0)

