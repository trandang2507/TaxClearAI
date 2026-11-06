from src.core import middleware


class FakeSettings:
    frontend_origin = " https://tax-clear-ai.vercel.app/ , http://localhost:3000 ,"


class WildcardSettings:
    frontend_origin = "*"


class LocalSettings:
    frontend_origin = "http://localhost:3000"


def test_allowed_origins_ignores_spaces_trailing_slash_and_empty_items(monkeypatch):
    monkeypatch.setattr(middleware, "get_settings", lambda: FakeSettings())
    assert middleware.allowed_origins() == [
        "https://tax-clear-ai.vercel.app",
        "http://localhost:3000",
    ]


def test_is_origin_allowed_with_wildcard(monkeypatch):
    monkeypatch.setattr(middleware, "get_settings", lambda: WildcardSettings())
    assert middleware.is_origin_allowed("https://tax-clear-ai.vercel.app")
    assert middleware.is_origin_allowed("http://localhost:3000")
    assert not middleware.is_origin_allowed(None)
    assert not middleware.is_origin_allowed("")


def test_is_origin_allowed_with_local_and_official_domain(monkeypatch):
    monkeypatch.setattr(middleware, "get_settings", lambda: LocalSettings())
    assert middleware.is_origin_allowed("http://localhost:3000")
    assert middleware.is_origin_allowed("https://tax-clear-ai.vercel.app")
    assert not middleware.is_origin_allowed("https://ke-gian.vercel.app")
    assert not middleware.is_origin_allowed(None)
