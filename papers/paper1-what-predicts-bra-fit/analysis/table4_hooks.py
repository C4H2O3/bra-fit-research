import csv
from collections import defaultdict


def main(joined_csv: str = "joined.csv") -> None:
    counts = defaultdict(lambda: {"Fits": 0, "Didn't fit": 0})
    for row in csv.DictReader(open(joined_csv, encoding="utf-8", errors="replace")):
        if row["fit_status"] not in ("Fits", "Didn't fit"):
            continue
        try:
            hooks = int(row["hooks"])
        except (ValueError, KeyError):
            continue
        counts[hooks][row["fit_status"]] += 1

    for hooks in range(1, 7):  # matches the range reported in Table 4
        d = counts[hooks]
        total = d["Fits"] + d["Didn't fit"]
        print(f"{hooks}  n={total:>6}  Fits={d['Fits'] / total:.1%}")


if __name__ == "__main__":
    main()
