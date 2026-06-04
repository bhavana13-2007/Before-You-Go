import csv
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


import budget_logger

VALID_ENTRY = {
    "date": "2026-06-03",
    "category": "groceries",
    "amount": "12.50",
    "description": "milk",
}

INVALID_AMOUNT_ENTRY = {
    "date": "2026-06-03",
    "category": "groceries",
    "amount": "twelve",
    "description": "milk",
}

INVALID_DATE_ENTRY = {
    "date": "03-06-2026",
    "category": "utilities",
    "amount": "55.00",
    "description": "electricity",
}


def _read_csv_rows(path: Path):
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.reader(file))


def test_append_creates_file(tmp_path: Path):
    target = tmp_path / "data.csv"
    result = budget_logger.append_entry(VALID_ENTRY, data_file=target)

    assert result["success"] is True
    rows = _read_csv_rows(target)
    assert rows[0] == budget_logger.EXPECTED_HEADER
    assert rows[1] == ["2026-06-03", "groceries", "12.5", "milk"]


def test_append_appends_to_existing_file(tmp_path: Path):
    target = tmp_path / "data.csv"
    budget_logger._initialize_file(target)
    budget_logger.append_entry(VALID_ENTRY, data_file=target)
    second_entry = {
        "date": "2026-06-04",
        "category": "transport",
        "amount": "25.00",
        "description": "bus pass",
    }

    result = budget_logger.append_entry(second_entry, data_file=target)

    assert result["success"] is True
    rows = _read_csv_rows(target)
    assert len(rows) == 3
    assert rows[1] == ["2026-06-03", "groceries", "12.5", "milk"]
    assert rows[2] == ["2026-06-04", "transport", "25.0", "bus pass"]


def test_rejects_missing_required_field(tmp_path: Path):
    target = tmp_path / "data.csv"
    entry = VALID_ENTRY.copy()
    entry["category"] = ""

    result = budget_logger.append_entry(entry, data_file=target)

    assert result["success"] is False
    assert "category is required" in result["errors"]
    assert not target.exists()


def test_rejects_invalid_numeric_and_date_values(tmp_path: Path):
    target = tmp_path / "data.csv"

    date_result = budget_logger.append_entry(INVALID_DATE_ENTRY, data_file=target)
    assert date_result["success"] is False
    assert "date must be ISO 8601" in date_result["errors"][0]
    assert not target.exists()

    amount_result = budget_logger.append_entry(INVALID_AMOUNT_ENTRY, data_file=target)
    assert amount_result["success"] is False
    assert "amount must be a numeric value" in amount_result["errors"]
    assert not target.exists()


def test_rejects_malformed_header(tmp_path: Path):
    target = tmp_path / "data.csv"
    target.write_text("foo,bar\n1,2\n", encoding="utf-8")

    result = budget_logger.append_entry(VALID_ENTRY, data_file=target)

    assert result["success"] is False
    assert "Header mismatch" in result["message"]
    rows = _read_csv_rows(target)
    assert rows[0] == ["foo", "bar"]
    assert len(rows) == 2


def test_concurrent_appends_preserve_complete_rows(tmp_path: Path):
    target = tmp_path / "data.csv"
    entries = [
        {
            "date": "2026-06-03",
            "category": "groceries",
            "amount": "12.50",
            "description": "milk",
        },
        {
            "date": "2026-06-03",
            "category": "transport",
            "amount": "10.00",
            "description": "taxi",
        },
    ]

    with ThreadPoolExecutor(max_workers=2) as executor:

        def fn(entry):
            return budget_logger.append_entry(
                entry,
                data_file=target,
            )

        results = list(executor.map(fn, entries))

        # Final pipeline sanity check
    assert all(result["success"] for result in results)
    rows = _read_csv_rows(target)
    assert rows[0] == budget_logger.EXPECTED_HEADER
    assert len(rows) == 3
    assert ["2026-06-03", "groceries", "12.5", "milk"] in rows
    assert ["2026-06-03", "transport", "10.0", "taxi"] in rows


def test_append_latency_is_under_two_seconds(tmp_path: Path):
    target = tmp_path / "data.csv"
    start = time.monotonic()
    result = budget_logger.append_entry(VALID_ENTRY, data_file=target)
    elapsed = time.monotonic() - start

    assert result["success"] is True
    assert elapsed < 2.0
