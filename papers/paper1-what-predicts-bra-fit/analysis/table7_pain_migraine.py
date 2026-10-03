import csv
import re
from collections import Counter

PATTERNS = re.compile(
    r"(neck pain|migrain|headache|shoulder pain|back pain|sore neck|neck ache)"
)

SMALL = {"AA", "A", "B", "C", "D"}
MEDIUM = {"DD", "E", "EE", "F", "FF", "G"}


def extract_cup(size: str) -> str | None:
    if not size:
        return None
    m = re.search(r"([0-9]{2,3})\s*([A-Z]{1,3})", size.strip().upper())
    return m.group(2) if m else None


def bucket(cup: str) -> str:
    if cup in SMALL:
        return "small (AA-D)"
    if cup in MEDIUM:
        return "medium (DD-G)"
    return "large (GG+)"


def main(reviews_csv: str = "reviews.csv") -> None:
    total = Counter()
    matched = Counter()
    with open(reviews_csv, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            cup = extract_cup(row.get("size", ""))
            if cup is None:
                continue
            group = bucket(cup)
            total[group] += 1
            if PATTERNS.search((row.get("review_text") or "").lower()):
                matched[group] += 1

    for group in ["small (AA-D)", "medium (DD-G)", "large (GG+)"]:
        t, m = total[group], matched[group]
        print(f"{group:<16}{t:>8}{m:>8}{100 * m / t:>10.3f}%")


if __name__ == "__main__":
    main()
