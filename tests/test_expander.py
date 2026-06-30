from domainops.core.expander import DEFAULT_TLDS, expand_domains, parse_tlds

class TestExpandDomains:
    def test_uses_default_tlds(self):
        result = expand_domains(["fitora"])
        assert result == [f"fitora{tld}" for tld in DEFAULT_TLDS]

    def test_custom_tlds(self):
        assert expand_domains(["fitora"], tlds=[".com", ".ai"]) == ["fitora.com", "fitora.ai"]

    def test_lowercases_names(self):
        assert expand_domains(["Fitora"], tlds=[".com"]) == ["fitora.com"]

    def test_empty_names(self):
        assert expand_domains([]) == []

    def test_multiple_names(self):
        assert expand_domains(["a", "b"], tlds=[".com"]) == ["a.com", "b.com"]

class TestParseTlds:
    def test_with_dots(self):
        assert parse_tlds(".com,.io") == [".com", ".io"]
    
    def test_without_dots(self):
        assert parse_tlds("com,io") == [".com", ".io"]

    def test_mixed(self):
        assert parse_tlds("com,.io,ai") == [".com", ".io", ".ai"]

    def test_strips_whitespace(self):
        assert parse_tlds(" com , io ") == [".com", ".io"]

    def test_empty_string_returns_none(self):
        assert parse_tlds("") is None

    def test_only_commas_returns_none(self):
        assert parse_tlds(",,,") is None