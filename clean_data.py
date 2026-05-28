from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable


INPUT_FILE = Path(__file__).with_name("APPLE_daily.csv")
OUTPUT_FILE = Path(__file__).with_name("APPLE_daily_reformed.csv")
START_DATE = datetime(2000, 1, 1)


def parse_row(row: list[str]) -> tuple[datetime, list[str]]:
    if len(row) != 7:
        raise ValueError(f"Expected 7 columns per row, got {len(row)}: {row}")

    date = datetime.strptime(row[0], "%Y-%m-%d")
    open_price = row[1]
    high_price = row[2]
    low_price = row[3]
    close_price = row[4]
    volume = row[5]
    adj_close = row[6]

    return date, [
        row[0],
        open_price,
        high_price,
        low_price,
        close_price,
        volume,
        adj_close,
    ]


def clean_rows(rows: Iterable[list[str]]) -> list[list[str]]:
    cleaned_rows: list[list[str]] = []

    for row in rows:
        date, normalized_row = parse_row(row)
        if date >= START_DATE:
            cleaned_rows.append(normalized_row)

    cleaned_rows.sort(key=lambda item: item[0])
    return cleaned_rows


def main() -> None:
    with INPUT_FILE.open(newline="", encoding="utf-8") as source:
        reader = csv.reader(source)
        header = next(reader)
        if len(header) != 7:
            raise ValueError(f"Expected 7 columns in header, got {len(header)}: {header}")

        cleaned_rows = clean_rows(list(reader))

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["Date", "Open", "High", "Low", "Close", "Volume", "Adj Close"])
        writer.writerows(cleaned_rows)

    print(f"Wrote {len(cleaned_rows)} rows to {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()