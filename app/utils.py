def format_usd(v: float) -> str:
    if v is None: return "-"
    if v >= 1_000_000: return f"${v/1_000_000:.2f}M"
    if v >= 1_000: return f"${v/1_000:.2f}k"
    return f"${v:.2f}"
