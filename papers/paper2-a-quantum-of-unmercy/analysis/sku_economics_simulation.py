import json
import math
import re
from collections import Counter, defaultdict

D_TOTAL = 10000  # illustrative annual demand for one style/color
MOQ = 100  # conservative lower tier (argusapparel.com cites 50-100)
COARSE_BANDS = [32, 34, 36, 38]
COARSE_CUPS = ["A", "B", "C", "D"]
CUP_ORDER = ["A", "B", "C", "D", "DD", "E", "EE", "F", "FF", "G", "GG", "H"]


def norm_cup(c: str) -> str:
    c = c.lower().strip()
    c = c.replace("ddd/e", "e").replace("dd/e", "dd")
    return c.upper()


def load_real_demand(rtr_path: str, modcloth_path: str) -> Counter:
    combined = Counter()
    with open(rtr_path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            bs = row.get("bust size")
            if not bs:
                continue
            m = re.match(r"(\d+)([a-zA-Z/+]+)", bs)
            if not m:
                continue
            combined[(int(m.group(1)), norm_cup(m.group(2)))] += 1

    with open(modcloth_path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            bs, cup = row.get("bra size"), row.get("cup size")
            if not bs or not cup:
                continue
            try:
                band = int(float(bs))
            except ValueError:
                continue
            combined[(band, norm_cup(cup))] += 1
    return combined


def snap_band(b: int) -> int:
    return min(COARSE_BANDS, key=lambda x: abs(x - b))


def snap_cup(c: str) -> str:
    if c not in CUP_ORDER:
        return "D"
    idx = CUP_ORDER.index(c)
    coarse_idx = [CUP_ORDER.index(x) for x in COARSE_CUPS]
    nearest = min(coarse_idx, key=lambda ci: abs(ci - idx))
    return CUP_ORDER[nearest]


def unit_cost(qty: float) -> float:
    # midpoints of seamapparel.com's cited MOQ price tiers
    if qty < 200:
        return 24.0
    if qty < 500:
        return 15.0
    if qty < 1000:
        return 11.5
    return 9.0


def weighted_avg_cost(skus: dict) -> float:
    total_units = sum(skus.values())
    total_cost = sum(unit_cost(v) * v for v in skus.values())
    return total_cost / total_units


def main(rtr_path: str = "renttherunway_final_data.json",
         modcloth_path: str = "modcloth_final_data.json") -> None:
    combined = load_real_demand(rtr_path, modcloth_path)
    total = sum(combined.values())

    fine_skus = {k: D_TOTAL * n / total for k, n in combined.items()}

    coarse_skus = defaultdict(float)
    for (b, c), n in combined.items():
        coarse_skus[(snap_band(b), snap_cup(c))] += D_TOTAL * n / total

    N_fine, N_coarse = len(fine_skus), len(coarse_skus)
    print(f"N_fine = {N_fine}, N_coarse = {N_coarse}")

    capital_ratio = math.sqrt(N_fine / N_coarse)
    print(f"Square Root Law capital ratio: {capital_ratio:.2f}x")

    below_moq_fine = {k: v for k, v in fine_skus.items() if v < MOQ}
    forced_overstock = sum(MOQ - v for v in below_moq_fine.values())
    print(f"Fine SKUs below MOQ={MOQ}: {len(below_moq_fine)}/{N_fine} "
          f"({100 * len(below_moq_fine) / N_fine:.0f}%)")
    print(f"Forced overstock: {forced_overstock:,.0f} units/year")

    print(f"Weighted avg unit cost: fine ${weighted_avg_cost(fine_skus):.2f} "
          f"vs coarse ${weighted_avg_cost(coarse_skus):.2f}")


if __name__ == "__main__":
    main()
