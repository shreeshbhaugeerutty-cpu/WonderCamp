"""
Turns a list of daily prices into an SVG path, so the price trend chart
can be drawn with plain <svg> + <path> in the template - no JS charting
library needed.
"""


def _fmt(n):
    return f"{n:.1f}".rstrip("0").rstrip(".")


def build_price_chart(prices, width=300, pad_left=14, pad_right=4, top=8, base=100):
    """
    prices: list of numbers, oldest first (one per day).
    Returns a dict with:
      - area_path: SVG path string for the filled area under the line
      - ticks: list of {"day": i, "x": x-position} for axis labels
    """
    if len(prices) < 2:
        return None

    lo = min(prices) - 10
    hi = max(prices) + 6
    span = (hi - lo) or 1
    n = len(prices)

    def x_at(i):
        return pad_left + (i / (n - 1)) * (width - pad_left - pad_right)

    def y_at(v):
        return base - ((v - lo) / span) * (base - top)

    pts = [(x_at(i), y_at(v)) for i, v in enumerate(prices)]

    # Smooth curve through the points (Catmull-Rom converted to cubic Beziers)
    line = f"M{_fmt(pts[0][0])} {_fmt(pts[0][1])}"
    for i in range(n - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[i + 2] if i + 2 < n else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        line += f" C{_fmt(c1[0])} {_fmt(c1[1])} {_fmt(c2[0])} {_fmt(c2[1])} {_fmt(p2[0])} {_fmt(p2[1])}"

    area_path = f"{line} L{_fmt(x_at(n - 1))} {base} L{_fmt(x_at(0))} {base} Z"

    tick_days = sorted(set([0, n // 3, 2 * n // 3, n - 1]))
    ticks = [{"day": d, "x": _fmt(x_at(d))} for d in tick_days]

    return {"area_path": area_path, "ticks": ticks}