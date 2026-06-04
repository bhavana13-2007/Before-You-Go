from pathlib import Path
import os
import zipfile
import xml.etree.ElementTree as ET

from flask import Flask, jsonify, render_template, request
import pandas as pd

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.csv"
REQUIRED_COLUMNS = {"list", "required_doc", "tips"}


def _xlsx_cell_value(cell, shared_strings, namespace):
    value = cell.find("a:v", namespace)
    if cell.get("t") == "inlineStr":
        return "".join(text.text or "" for text in cell.findall(".//a:t", namespace))
    if value is None:
        return ""
    if cell.get("t") == "s":
        return shared_strings[int(value.text)]
    return value.text or ""


def _read_xlsx_without_openpyxl(path):
    namespace = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as workbook:
        shared_strings = []
        if "xl/sharedStrings.xml" in workbook.namelist():
            root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
            for item in root.findall("a:si", namespace):
                shared_strings.append(
                    "".join(
                             text.text or ""
                            for text in item.findall(".//a:t", namespace)
                        )
                )

        sheet = ET.fromstring(workbook.read("xl/worksheets/sheet1.xml"))
        rows = []
        for row in sheet.findall(".//a:sheetData/a:row", namespace):
            rows.append(
                [
                    _xlsx_cell_value(cell, shared_strings, namespace)
                    for cell in row.findall("a:c", namespace)
                ]
            )

    if not rows:
        return pd.DataFrame()

    headers = rows[0]
    normalized_rows = [(row + [""] * len(headers))[: len(headers)] for row in rows[1:]]
    return pd.DataFrame(normalized_rows, columns=headers)


def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    with DATA_FILE.open("rb") as file:
        is_excel_file = file.read(4) == b"PK\x03\x04"

    if is_excel_file:
        try:
            data = pd.read_excel(DATA_FILE)
        except ImportError:
            data = _read_xlsx_without_openpyxl(DATA_FILE)
    else:
        data = pd.read_csv(DATA_FILE, encoding="utf-8-sig", on_bad_lines="skip")

    data.columns = data.columns.astype(str).str.strip()
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
       raise ValueError(
            "Missing required columns in data file: "
            f"{', '.join(sorted(missing_columns))}"
        )

    data["search_key"] = data["list"].astype(str).str.strip().str.lower()
    return data


df = load_data()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/suggestions")
def get_suggestions():
    suggestions = df["list"].dropna().astype(str).tolist()
    return jsonify(suggestions)
#Testing
print("Suggestions Running")


@app.route("/document/<name>")
def get_document(name):
    service_name = name.strip().lower()
    row = df[df["search_key"] == service_name]

    if row.empty:
        return jsonify({"error": "Not Found"}), 404

    row = row.iloc[0]
    return jsonify(
        {
            "required_document": str(row["required_doc"]),
            "tips": str(row["tips"]),
            "fee": str(row.get("fee", "")),
            "estimated_time": str(row.get("estimated _time", "")),
        }
    )
    #Testing
    print("Document fetching sucessfully")


@app.route("/get_info")
def get_info():
    service_name = request.args.get("service", "").strip()
    if not service_name:
        return jsonify({"error": "Service name is required"}), 400

    row = df[df["search_key"] == service_name.lower()]
    if row.empty:
        return jsonify({"error": "Service not found"}), 404

    row = row.iloc[0]
    return jsonify(
        {
            "documents": row["required_doc"],
            "mistakes": row["tips"],
            "fee": row.get("fee", ""),
            "estimated_time": row.get("estimated _time", ""),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

def test_basic():
    assert True

