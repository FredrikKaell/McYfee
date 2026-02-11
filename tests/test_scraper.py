import requests
from webtracker.scraper.scraper import fetch_html


class DummyResponse:
    def __init__(self, text: str, status_code: int):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


def test_fetch_html_returns_text_when_200(monkeypatch):
    def mock_get(*args, **kwargs):
        return DummyResponse("<html>OK</html>", 200)

    monkeypatch.setattr("webtracker.scraper.scraper.requests.get", mock_get)

    result = fetch_html("https://example.com")
    assert result == "<html>OK</html>"


def test_fetch_html_returns_none_when_http_error(monkeypatch):
    def mock_get(*args, **kwargs):
        return DummyResponse("Error", 404)

    monkeypatch.setattr("webtracker.scraper.scraper.requests.get", mock_get)

    result = fetch_html("https://example.com", retries=0)
    assert result is None


def test_fetch_html_returns_none_on_request_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("Connection failed")

    monkeypatch.setattr("webtracker.scraper.scraper.requests.get", mock_get)

    result = fetch_html("https://example.com", retries=0)
    assert result is None
