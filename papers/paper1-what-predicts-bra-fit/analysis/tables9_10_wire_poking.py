import csv
import re

PATTERN = re.compile(
    r"(wire (is |was )?poking|wire (is |was )?popp?ed|"
    r"wire (is |was )?coming (out|through)|wire (is |was )?sticking out|"
    r"wire broke|wire broken|poking (out|through)|"
    r"underwire (popped|poking)|wire (escaped|exposed)|wire stabb)"
)


def load_rows(joined_csv: str):
    rows = []
    with open(joined_csv, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            text = (row.get("review_text") or "").lower()
            hit = bool(PATTERN.search(text))
            rows.append((row, hit))
    return rows


def parse(row, field: str):
    try:
        return float(row[field])
    except (ValueError, KeyError):
        return None


def quintile_table(rows, field: str, label: str) -> None:
    # Both tables are restricted to underwired models (wire_length_cm != 0);
    # Table 9 bins by wire length, Table 10 bins by cup depth on the same
    # underwired subset, as a control check.
    data = []
    for row, hit in rows:
        wl = parse(row, "wire_length_cm")
        v = parse(row, field)
        if wl is None or wl == 0 or v is None or v == 0:
            continue
        data.append((v, hit))
    data.sort(key=lambda r: r[0])
    n = len(data)
    q = n // 5
    bins = [data[i * q:(i + 1) * q] if i < 4 else data[4 * q:] for i in range(5)]
    print(f"\n{label} quintiles (n={n}):")
    for i, group in enumerate(bins, 1):
        lo, hi = group[0][0], group[-1][0]
        mentions = sum(1 for _, hit in group if hit)
        print(
            f"Q{i}: {lo:.1f}-{hi:.1f} cm, n={len(group)}, "
            f"mentions={mentions}, rate={100 * mentions / len(group):.3f}%"
        )


def pearson(xs, ys) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    return cov / (sx * sy)


def main(joined_csv: str = "joined.csv") -> None:
    rows = load_rows(joined_csv)

    quintile_table(rows, field="wire_length_cm", label="Wire length")  # Table 9
    quintile_table(rows, field="cup_depth_cm", label="Cup depth")      # Table 10

    # Correlation check: requires wire length, cup depth, cup width and
    # cup height all present, wire length non-zero (wireless excluded).
    wl, cd, cw, ch = [], [], [], []
    for row, _ in rows:
        v_wl, v_cd, v_cw, v_ch = (
            parse(row, "wire_length_cm"),
            parse(row, "cup_depth_cm"),
            parse(row, "cup_width_cm"),
            parse(row, "cup_height_cm"),
        )
        if None in (v_wl, v_cd, v_cw, v_ch) or v_wl == 0:
            continue
        wl.append(v_wl)
        cd.append(v_cd)
        cw.append(v_cw)
        ch.append(v_ch)

    print(f"\ncorrelation sample size: n={len(wl)}")
    print(f"corr(wire_length, cup_depth)  = {pearson(wl, cd):.3f}")
    print(f"corr(wire_length, cup_width)  = {pearson(wl, cw):.3f}")
    print(f"corr(wire_length, cup_height) = {pearson(wl, ch):.3f}")


if __name__ == "__main__":
    main()
