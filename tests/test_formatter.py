from domainops.utils.formatter import format_price

class TestFormatPrice:
  def test_usd(self):
    assert format_price(12_990_000, "USD") == "$12.99"

  def test_gbp(self):
    assert format_price(9_990_000, "GBP") == "£9.99"

  def test_none_returns_dash(self):
    assert format_price(None, "USD") == "[dim]—[/dim]"

  def test_zero_returns_dash(self):
    assert format_price(0, "USD") == "[dim]—[/dim]"

  def test_unknown_currency_uses_code(self):
    assert format_price(5_000_000, "XYZ") == "XYZ5.00"