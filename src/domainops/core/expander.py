DEFAULT_TLDS = [".com", ".io", ".app", ".ai", ".co"]


def expand_domains(names: list[str], tlds: list[str] | None = None) -> list[str]:
    resolved = tlds if tlds is not None else DEFAULT_TLDS
    return [f"{name.lower()}{tld}" for name in names for tld in resolved]
