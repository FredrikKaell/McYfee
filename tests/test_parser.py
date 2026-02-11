# tests/test_parser.py

from webtracker.scraper.parser import parse, parse_with_css


def test_parse_with_css_returns_text():
    html = "<html><body><span id='price'>849.-</span></body></html>"
    assert parse_with_css(html, "#price") == "849.-"


def test_parse_returns_none_when_no_selector(monkeypatch):
    # Patcha fetch_html där den används: i parser-modulen
    def fake_fetch_html(url):
        return "<html><body><span id='price'>849.-</span></body></html>"

    monkeypatch.setattr("webtracker.scraper.parser.fetch_html", fake_fetch_html)

    url = "https://example.com"
    selector = {"css_selector": None, "xpath": None}
    assert parse(url, selector) is None


def test_parse_returns_value_using_css(monkeypatch):
    def fake_fetch_html(url):
        return "<html><body><span id='price'>3790.-</span></body></html>"

    monkeypatch.setattr("webtracker.scraper.parser.fetch_html", fake_fetch_html)

    url = "https://example.com"
    selector = {"css_selector": "#price", "xpath": None}
    assert parse(url, selector) == "3790.-"
