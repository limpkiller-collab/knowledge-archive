from scrap import gemini


class Resp:
    def __init__(self, status, text="", data=None):
        self.status_code, self.text, self._data = status, text, data

    def json(self):
        return self._data


def test_falls_back_to_next_model_on_overload(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.setattr(gemini.time, "sleep", lambda s: None)
    calls = []

    def post(url, **kw):
        calls.append(url)
        if len(calls) == 1:
            return Resp(503, "busy")
        return Resp(200, data={"candidates": [{"content": {"parts": [{"text": "답"}]}}]})

    monkeypatch.setattr(gemini.requests, "post", post)
    assert gemini.generate([{"text": "q"}]) == "답"
    assert "gemini-3.8-flash" in calls[0] and "gemini-3.6-flash" in calls[1]


def test_configured_model_goes_first(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    assert gemini.models() == ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3.6-flash"]
