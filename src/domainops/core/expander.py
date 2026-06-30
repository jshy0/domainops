DEFAULT_TLDS = [".com", ".io", ".app", ".ai", ".co"]


def parse_tlds(tlds_str: str) -> list[str] | None:
    parsed = [f".{t.strip().lstrip('.')}" for t in tlds_str.split(",") if t.strip()]
    return parsed or None


def expand_domains(names: list[str], tlds: list[str] | None = None) -> list[str]:
    resolved = tlds if tlds is not None else DEFAULT_TLDS
    return [f"{name.lower()}{tld}" for name in names for tld in resolved]
