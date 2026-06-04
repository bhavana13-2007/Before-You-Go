from __future__ import annotations

import csv
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Iterator

DATA_FILE = Path(__file__).resolve().parent / "data.csv"
EXPECTED_HEADER = ["date", "category", "amount", "description"]
LOCK_SUFFIX = ".lock"


class BudgetLoggerError(Exception):
    pass


def _normalize_header(header: Iterable[str]) -> List[str]:
    return [str(column).strip().lower() for column in header]


def _parse_date(value: str) -> str:
    candidate = str(value).strip()
    if not candidate:
        raise ValueError("date is required")

    try:
        return datetime.fromisoformat(candidate).date().isoformat()
    except ValueError:
        pass

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(candidate, fmt).date().isoformat()
        except ValueError:
            continue

    raise ValueError(
        "date must be ISO 8601 or one of YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY"
    )


def _validate_amount(value: str) -> str:
    candidate = str(value).strip()
    if not candidate:
        raise ValueError("amount is required")

    try:
        return str(float(candidate))
    except ValueError:
        raise ValueError("amount must be a numeric value")


def _validate_string_field(value: str, field_name: str) -> str:
    candidate = str(value).strip()
    if not candidate:
        raise ValueError(f"{field_name} is required")
    return candidate


def _normalize_entry(
    entry: Mapping[str, Any],
) -> Tuple[bool, List[str], Optional[List[str]]]:
    errors: List[str] = []

    try:
        date_value = _parse_date(str(entry.get("date", "")))
    except ValueError as exc:
        errors.append(str(exc))
        date_value = ""

    try:
        category_value = _validate_string_field(
            str(entry.get("category", "")),
            "category",
        )
    except ValueError as exc:
        errors.append(str(exc))
        category_value = ""

    try:
        amount_value = _validate_amount(str(entry.get("amount", "")))
    except ValueError as exc:
        errors.append(str(exc))
        amount_value = ""

    try:
        description_value = _validate_string_field(
            str(entry.get("description", "")),
            "description",
        )
    except ValueError as exc:
        errors.append(str(exc))
        description_value = ""

    if errors:
        return False, errors, None

    return True, [], [
        date_value,
        category_value,
        amount_value,
        description_value,
    ]


def _read_header(data_file: Path) -> Optional[List[str]]:
    if not data_file.exists():
        return None

    with data_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        try:
            header = next(reader)
        except StopIteration:
            return None

    return _normalize_header(header)


def _initialize_file(data_file: Path) -> None:
    data_file.parent.mkdir(parents=True, exist_ok=True)
    with data_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(EXPECTED_HEADER)
        file.flush()
        os.fsync(file.fileno())


def _append_row_atomically(data_file: Path, row: List[str]) -> None:
    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        dir=str(data_file.parent),
        delete=False,
        newline="",
        encoding="utf-8",
    )
    try:
        with temp_file as handle:
            writer = csv.writer(handle)
            if data_file.exists() and data_file.stat().st_size > 0:
                with data_file.open("r", newline="", encoding="utf-8") as source:
                    for existing in csv.reader(source):
                        writer.writerow(existing)
            else:
                writer.writerow(EXPECTED_HEADER)
            writer.writerow(row)
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temp_file.name, data_file)
    except Exception:
        try:
            os.remove(temp_file.name)
        except OSError:
            pass
        raise


@contextmanager
def _file_lock(data_file: Path) -> Iterator[None]:
    lock_file = data_file.with_name(data_file.name + LOCK_SUFFIX)
    lock_file.parent.mkdir(parents=True, exist_ok=True)

    with open(lock_file, "a+", encoding="utf-8") as handle:
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(  # type: ignore[attr-defined]
                handle.fileno(),
                msvcrt.LK_LOCK,  # type: ignore[attr-defined]
                1,
            )
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)

        try:
            yield
        finally:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(  # type: ignore[attr-defined]
                    handle.fileno(),
                    msvcrt.LK_UNLCK,  # type: ignore[attr-defined]
                    1,
                )
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def append_entry(
    entry: Mapping[str, Any],
    data_file: Optional[Path] = None,
) -> Dict[str, Any]:
    data_file = Path(data_file) if data_file is not None else DATA_FILE

    # 1. Validate the input
    valid, errors, row = _normalize_entry(entry)

    if not valid:
        return {
            "success": False,
            "message": "Validation failed",
            "errors": errors,
        }

    assert row is not None

    # 2. Use the file lock to ensure atomic operations
    try:
        with _file_lock(data_file):
            _append_row_atomically(data_file, row)
            return {
                "success": True,
                "message": "Entry appended successfully"
            }
    except Exception as e:
        # This catches any file system errors (permission issues, etc.)
        return {
            "success": False,
            "message": "Failed to write to file",
            "errors": [str(e)],
        }

def _cli_entry_from_args(args: Any) -> Dict[str, str]:
    return {
        "date": args.date,
        "category": args.category,
        "amount": args.amount,
        "description": args.description,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description=(
        "Append a clean budget row to data.csv "
        "with safe validation and atomic persistence."
        )
    )
    parser.add_argument(
    "--date",
    required=True,
    help="Budget entry date in YYYY-MM-DD or DD/MM/YYYY",
    )
    parser.add_argument("--category", required=True, help="Budget category")
    parser.add_argument("--amount", required=True, help="Numeric amount")
    parser.add_argument("--description", required=True, help="Budget entry description")
    parser.add_argument(
        "--file",
        default=str(DATA_FILE),
        help="Target CSV file to write",
    )
    args = parser.parse_args()

    result = append_entry(_cli_entry_from_args(args), data_file=Path(args.file))

    if result["success"]:
        print(result["message"])
        return 0

    print("Failed to append budget entry:")
    for error in result["errors"]:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
