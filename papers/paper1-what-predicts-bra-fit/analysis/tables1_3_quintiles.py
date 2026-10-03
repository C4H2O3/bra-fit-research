import csv
from collections import defaultdict

TABLE1_CUP = {
    "cup_depth_cm": "Cup depth",
    "cup_width_cm": "Cup width",
    "wire_length_cm": "Wire length",
    "cup_height_cm": "Cup height",
}
TABLE2_BAND = {
    "ribcage_cm": "Underbust circumference",
    "stretched_band_cm": "Stretched band",
    "band_length_cm": "Band length",
}
TABLE3_CONSTRUCTION = {
    "gore_height_cm": "Gore height",
    "wing_height_cm": "Wing height",
    "cup_separation_cm": "Cup spread",
    "strap_width_cm": "Strap width",
}

MIN_BRAND_N = 30


def load_rows(joined_csv: str):
    rows = []
    with open(joined_csv, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            if row["fit_status"] in ("Fits", "Didn't fit"):
                rows.append(row)
    return rows


def to_float(v):
    try:
        f = float(v)
        return f if f > 0 else None
    except (ValueError, TypeError):
        return None


def demean_by_brand(rows, field: str):
    by_brand = defaultdict(list)
    for r in rows:
        v = to_float(r[field])
        if v is not None:
            by_brand[r["brand"]].append(v)
    brand_mean = {b: sum(vs) / len(vs) for b, vs in by_brand.items() if len(vs) >= MIN_BRAND_N}

    out = []
    for r in rows:
        v = to_float(r[field])
        if v is None or r["brand"] not in brand_mean:
            continue
        out.append((v - brand_mean[r["brand"]], r["fit_status"]))
    return out, len(brand_mean)


def quintile_fit_rates(demeaned):
    vals = sorted(v for v, _ in demeaned)
    n = len(vals)
    cuts = [vals[int(n * p)] for p in (0.2, 0.4, 0.6, 0.8)]

    def bucket(v):
        for i, c in enumerate(cuts):
            if v <= c:
                return i
        return len(cuts)

    buckets = defaultdict(lambda: {"Fits": 0, "Didn't fit": 0})
    for v, fit in demeaned:
        buckets[bucket(v)][fit] += 1

    rates = []
    for b in range(5):
        d = buckets[b]
        total = d["Fits"] + d["Didn't fit"]
        rates.append(d["Fits"] / total if total else float("nan"))
    return rates


def print_table(fields: dict, joined_csv: str) -> None:
    rows = load_rows(joined_csv)
    for field, label in fields.items():
        demeaned, n_brands = demean_by_brand(rows, field)
        rates = quintile_fit_rates(demeaned)
        pct = "  ".join(f"{r:.1%}" for r in rates)
        print(f"{label:<28}{pct}   brands={n_brands}")


def main(joined_csv: str = "joined.csv") -> None:
    print("Table 1 — cup measurements")
    print_table(TABLE1_CUP, joined_csv)
    print("\nTable 2 — band measurements")
    print_table(TABLE2_BAND, joined_csv)
    print("\nTable 3 — construction geometry")
    print_table(TABLE3_CONSTRUCTION, joined_csv)


if __name__ == "__main__":
    main()
