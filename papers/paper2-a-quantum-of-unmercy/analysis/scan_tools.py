"""
Инструменты для облака точек (PLY, Scaniverse) — техтест из KB §44:
"читается ли файл, извлекаются ли ориентиры/объём". Не часть recommend()
и не подключено к BodyPassport — отдельная утилита для разведки скана и
сверки с лентой, пока пайплайн скан->объём не построен.

Метод — намеренно самый простой из возможных (периметр выпуклой оболочки
по горизонтальным срезам), взят как нижняя планка, не как целевой алгоритм
(KB §44). Единицы на входе — как в файле Scaniverse (метры); все функции
здесь возвращают см.
"""

import numpy as np
from dataclasses import dataclass
from scipy.spatial import ConvexHull
from sklearn.cluster import DBSCAN

# Грубая внешняя граница правдоподобия для периметра ТОРСА взрослого
# человека (не талии конкретно — просто "это анатомически может быть
# торс, а не рука/бедро"). Не калибровка, не диапазон "нормы" — только
# чтобы отсечь явно чужие части тела при поиске талии/бюста (KB §51).
PLAUSIBLE_TORSO_PERIMETER_CM = (55.0, 160.0)


def load_ply_xyzrgb(path: str, scale_to_cm: float = 100.0):
    """
    Читает бинарный PLY (little-endian, x,y,z,uchar r,g,b) — формат
    Scaniverse. Возвращает (xyz в см, rgb uint8). Не универсальный
    PLY-парсер: рассчитан именно на этот формат экспорта (KB §44).
    """
    with open(path, "rb") as f:
        header = b""
        n = None
        while True:
            line = f.readline()
            header += line
            if line.strip().startswith(b"element vertex"):
                n = int(line.strip().split()[-1])
            if line.strip() == b"end_header":
                break
        if n is None:
            raise ValueError("не нашёл 'element vertex' в заголовке PLY")
        data = f.read()

    dtype = np.dtype([("x", "<f4"), ("y", "<f4"), ("z", "<f4"),
                       ("r", "u1"), ("g", "u1"), ("b", "u1")])
    arr = np.frombuffer(data, dtype=dtype, count=n)
    xyz = np.stack([arr["x"], arr["y"], arr["z"]], axis=1) * scale_to_cm
    rgb = np.stack([arr["r"], arr["g"], arr["b"]], axis=1).astype(np.uint8)
    return xyz, rgb


@dataclass
class SliceStats:
    height_cm: float
    n_points: int         # точек В ВЫБРАННОМ (торсовом) кластере среза
    perimeter_cm: float
    width_cm: float   # ось X скана (лево-право)
    depth_cm: float    # ось Y скана (перёд-зад)
    n_points_total: int = 0   # точек во ВСЁМ срезе, до отсечения рук
    n_clusters: int = 1       # сколько кластеров нашлось на срезе (DBSCAN)

    @property
    def width_over_depth(self) -> float:
        return self.width_cm / self.depth_cm if self.depth_cm > 0 else float("inf")

    @property
    def likely_contaminated(self) -> bool:
        """
        Подстраховка НА СЛУЧАЙ, когда кластеризация не смогла разделить
        руку и торс (рука физически касается тела на этой высоте — так
        бывает у плеча/верхней части груди даже при разведённых руках,
        KB §51). Порог 1.3 — та же эвристика, что и раньше (KB §44),
        проверена на двух сканах, не калибровка.
        """
        return self.width_over_depth > 1.3

    @property
    def reliable(self) -> bool:
        """
        Два условия (KB §51): (1) достаточно точек — иначе оболочка
        ненадёжна (шум/край скана); (2) выбранный кластер — БОЛЬШИНСТВО
        точек среза, не мелкий обломок среди нескольких кластеров.
        Второе поймало реальный случай: у края скана срез иногда рвётся
        на 4-5 кусков (неполное покрытие), и "крупнейший" из них всё равно
        мелкий и с бессмысленным периметром — сам по себе не флагуется
        likely_contaminated (ширина/глубина в норме для СВОЕГО обломка).
        """
        if self.n_points < 50:
            return False
        if self.n_points_total > 0 and (self.n_points / self.n_points_total) < 0.6:
            return False
        return True


def height_profile(xyz: np.ndarray, step_cm: float = 1.0,
                    band_cm: float = 1.5, min_points: int = 6,
                    cluster_eps_cm: float = 2.5, cluster_min_samples: int = 5) -> list[SliceStats]:
    """
    Горизонтальные срезы по оси Z (высота). На каждом срезе точки сначала
    кластеризуются (DBSCAN по XY, `cluster_eps_cm`) — берём только САМЫЙ
    КРУПНЫЙ кластер (торс) и считаем периметр выпуклой оболочки по нему,
    отбрасывая более мелкие кластеры (руки, если они пространственно
    отделены на этой высоте). Это ключевое отличие от первой версии
    инструмента (KB §44), которая брала оболочку по ВСЕМ точкам среза —
    на скане с руками, разведёнными в стороны НО не строго горизонтально
    (KB §51, Model_2.2), руки пересекают почти всю высоту торса по
    диагонали, и без кластеризации портят практически весь профиль, не
    только зону подмышек.

    ВАЖНО: кластеризация помогает, только если рука на этой высоте
    пространственно отделена от торса (дальше `cluster_eps_cm`). Там, где
    рука касается тела (обычно верх груди/плечо), DBSCAN вернёт один
    слитный кластер — это по-прежнему ловит `likely_contaminated`
    (эвристика по width/depth), но как честное "не знаю", не как
    исправление позы за геометрию.

    Ось Z — вертикаль скана Scaniverse; для скана в другой ориентации
    входной xyz нужно заранее повернуть так, чтобы Z был вертикалью.
    """
    z = xyz[:, 2]
    z_min, z_max = z.min(), z.max()
    results = []
    zc = z_min + band_cm
    while zc < z_max - band_cm:
        mask = (z >= zc - band_cm / 2) & (z < zc + band_cm / 2)
        pts = xyz[mask][:, :2]
        n_total = len(pts)
        if n_total >= min_points:
            try:
                labels = DBSCAN(eps=cluster_eps_cm, min_samples=cluster_min_samples).fit_predict(pts)
                valid = labels >= 0
                if valid.any():
                    vals, counts = np.unique(labels[valid], return_counts=True)
                    n_clusters = len(vals)
                    biggest = vals[np.argmax(counts)]
                    torso_pts = pts[labels == biggest]
                else:
                    n_clusters = 0
                    torso_pts = pts  # DBSCAN не нашёл ни одного кластера — берём как есть
                if len(torso_pts) >= 6:
                    hull = ConvexHull(torso_pts)
                    perim = hull.area  # для 2D ConvexHull.area == периметр
                    width = torso_pts[:, 0].max() - torso_pts[:, 0].min()
                    depth = torso_pts[:, 1].max() - torso_pts[:, 1].min()
                    results.append(SliceStats(zc, len(torso_pts), perim, width, depth,
                                               n_points_total=n_total, n_clusters=n_clusters))
            except Exception:
                pass
        zc += step_cm
    return results


def find_waist_and_bust(profile: list[SliceStats]):
    """
    Талия — минимум периметра среди НАДЁЖНЫХ срезов (reliable) по всему
    профилю; без этого фильтра край скана (единицы точек, вырожденная
    оболочка) может выдать бессмысленно маленький "периметр" (KB §44:
    так и случилось на первой версии этой функции — 7.9 см на 19 точках).
    Бюст — максимум периметра среди надёжных, НЕ контaминированных срезов
    выше талии. Если таких нет вообще (весь верх скана задет руками, как
    и получилось на Model_2) — возвращает None, это честный результат,
    не число, которому нельзя доверять.

    ВАЖНО (KB §51, найдено на Model_2.2): на срезах ниже торса кластеризация
    иногда выбирает "крупнейший кластер", который анатомически не торс, а
    бедро/пах — ширина/глубина там в норме (не ловится likely_contaminated),
    но периметр физически не может быть периметром талии/пояса взрослого
    человека. `PLAUSIBLE_TORSO_PERIMETER_CM` — грубый нижний фильтр
    правдоподобия (не калибровка), отсекает такие срезы до поиска минимума.
    Возвращает (waist: SliceStats | None, bust: SliceStats | None).
    """
    reliable = [s for s in profile
                if s.reliable and PLAUSIBLE_TORSO_PERIMETER_CM[0] <= s.perimeter_cm <= PLAUSIBLE_TORSO_PERIMETER_CM[1]]
    if not reliable:
        return None, None
    waist = min(reliable, key=lambda s: s.perimeter_cm)
    above_clean = [s for s in reliable
                   if s.height_cm > waist.height_cm and not s.likely_contaminated]
    bust = max(above_clean, key=lambda s: s.perimeter_cm) if above_clean else None
    return waist, bust


def print_profile(profile: list[SliceStats]) -> None:
    print(f"{'высота,см':>10} {'n_торс':>7} {'n_всего':>8} {'кластер':>7} {'периметр,см':>12} "
          f"{'ширина,см':>10} {'глубина,см':>11} {'w/d':>5} {'подозрит.':>10}")
    for s in profile:
        flag = "РУКИ?" if s.likely_contaminated else ""
        print(f"{s.height_cm:10.1f} {s.n_points:7d} {s.n_points_total:8d} {s.n_clusters:7d} "
              f"{s.perimeter_cm:12.1f} {s.width_cm:10.1f} {s.depth_cm:11.1f} "
              f"{s.width_over_depth:5.2f} {flag:>10}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Использование: python3 scan_tools.py путь/к/скану.ply [пояс_лентой_см] [бюст_лентой_см]")
        sys.exit(1)

    xyz, _ = load_ply_xyzrgb(sys.argv[1])
    print(f"Точек: {len(xyz)}, диапазон высоты: {xyz[:,2].min():.1f}..{xyz[:,2].max():.1f} см")

    profile = height_profile(xyz)
    print_profile(profile)

    waist, bust = find_waist_and_bust(profile)
    print()
    if waist:
        print(f"Талия (мин. периметр всего профиля): {waist.perimeter_cm:.1f} см "
              f"на высоте {waist.height_cm:.1f} см")
    if bust:
        print(f"Лучший ЧИСТЫЙ кандидат в сторону бюста (не сам бюст!): "
              f"{bust.perimeter_cm:.1f} см на высоте {bust.height_cm:.1f} см. "
              "Это последний надёжный срез перед контаминацией рукой, а не "
              "обязательно пик обхвата — если контаминация начинается НИЖЕ "
              "истинного пика (как на Model_2), это число будет меньше "
              "реального обхвата груди, не равно ему.")
    else:
        print("Бюст не определён — все срезы выше талии помечены как "
              "потенциально задетые руками (см. likely_contaminated).")

    if len(sys.argv) >= 3:
        tape_band = float(sys.argv[2])
        print(f"\nЛента (пояс): {tape_band:.1f} см; скан (талия/пояс): "
              f"{waist.perimeter_cm:.1f} см; разница: {waist.perimeter_cm - tape_band:+.1f} см")
    if len(sys.argv) >= 4 and bust:
        tape_bust = float(sys.argv[3])
        print(f"Лента (грудь стоя): {tape_bust:.1f} см; скан (бюст): "
              f"{bust.perimeter_cm:.1f} см; разница: {bust.perimeter_cm - tape_bust:+.1f} см")
