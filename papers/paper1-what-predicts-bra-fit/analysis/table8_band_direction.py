import csv
import re

PATTERNS = {
    "band runs small": re.compile(r"band runs? (small|snug|tight)"),
    "band runs large": re.compile(r"band runs? (large|loose|big)"),
    "sized down band": re.compile(
        r"(sized? down.{0,15}band|band.{0,15}(down a size|sized? down)|went down a band|down a band)"
    ),
    "sized up band": re.compile(
        r"(sized? up.{0,15}band|band.{0,15}(up a size|sized? up)|went up a band|up a band)"
    ),
}


def main(reviews_csv: str = "reviews.csv") -> None:
    total = 0
    counts = {k: 0 for k in PATTERNS}
    with open(reviews_csv, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            total += 1
            text = (row.get("review_text") or "").lower()
            for label, pattern in PATTERNS.items():
                if pattern.search(text):
                    counts[label] += 1

    for label, n in counts.items():
        print(f"{label:<20}{n:>8}{100 * n / total:>10.3f}%")


if __name__ == "__main__":
    main()
