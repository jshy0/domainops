TLDS = [".com", ".io", ".app", ".ai", ".co"]


def expand_domains(names: list[str]) -> list[str]:
    return [f"{name.lower()}{tld}" for name in names for tld in TLDS]
