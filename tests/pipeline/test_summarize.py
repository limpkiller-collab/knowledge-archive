import pytest
from scrap import summarize
from scrap.models import Extracted

CATS = ["경제·투자", "테크", "etc"]
GOOD = {"title": "제목", "summary": "한 줄", "key_points": ["a", "b", "c"], "category": "테크",
        "tags": ["x", "y", "z"], "cover_word": "에이전트", "slug": "agent-prompt"}


def ex(**kw):
    return Extracted(source_type="article", url="https://e.com/a", text="본문", **kw)


def test_returns_validated_result():
    assert summarize.run(ex(), "", "", CATS, call_model=lambda p: dict(GOOD)) == GOOD


def test_chosen_category_overrides_model():
    out = summarize.run(ex(), "", "경제·투자", CATS, call_model=lambda p: dict(GOOD))
    assert out["category"] == "경제·투자"


def test_unknown_category_becomes_etc():
    out = summarize.run(ex(), "", "", CATS, call_model=lambda p: {**GOOD, "category": "없는것"})
    assert out["category"] == "etc"


def test_retries_once_then_fails():
    calls = []
    def bad(p):
        calls.append(1)
        return {**GOOD, "key_points": []}
    with pytest.raises(summarize.SummarizeError):
        summarize.run(ex(), "", "", CATS, call_model=bad)
    assert len(calls) == 2


def test_bad_slug_is_replaced():
    out = summarize.run(ex(), "", "", CATS, call_model=lambda p: {**GOOD, "slug": "한글 슬러그!"})
    assert out["slug"] == "card"


def test_long_transcript_is_truncated_with_warning():
    e = ex(transcript="가" * 130000)
    seen = {}

    def fake(p):
        seen["p"] = p
        return dict(GOOD)

    summarize.run(e, "", "", CATS, call_model=fake)
    assert len(seen["p"]["text"]) < 125000
    assert any("잘라" in w for w in e.warnings)
