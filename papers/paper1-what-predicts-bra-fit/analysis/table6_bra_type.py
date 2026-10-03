import csv
from collections import defaultdict


def load_bra_type(models_csv: str) -> dict:
    bra_type = {}
    with open(models_csv, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            bra_type[(row["brand"], row["model_slug"])] = row["bra_type"]
    return bra_type


def main(reviews_csv: str = "joined.csv", models_csv: str = "models.csv") -> None:
    bra_type = load_bra_type(models_csv)
    counts = defaultdict(lambda: {"Fits": 0, "Didn't fit": 0})

    with open(reviews_csv, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            if row["fit_status"] not in ("Fits", "Didn't fit"):
                continue
            bt = bra_type.get((row["brand"], row["model_slug"]))
            if not bt:
                continue
            counts[bt][row["fit_status"]] += 1

    for bt, d in sorted(counts.items(), key=lambda kv: -sum(kv[1].values())):
        total = d["Fits"] + d["Didn't fit"]
        print(f"{bt:<24} n={total:>6}  Fits={d['Fits'] / total:.1%}")


if __name__ == "__main__":
    main()
