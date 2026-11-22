from __future__ import annotations

import os
import time

import requests

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
FALLBACK_MODELS = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"]
RETRYABLE = (404, 429, 500, 503)  # 과부하·한도 초과·모델 없음이면 다음 모델로 넘어간다


def models() -> list[str]:
    first = os.environ.get("GEMINI_MODEL") or FALLBACK_MODELS[0]
    return [first] + [m for m in FALLBACK_MODELS if m != first]


def generate(parts: list[dict], timeout: int = 150) -> str:
    """Gemini에 요청해 글 답변을 받는다. 모델이 과부하면 다음 모델로 차례로 넘어간다."""
    body = {"contents": [{"parts": parts}]}
    last = None
    for i, model in enumerate(models()):
        if i:
            time.sleep(5)
        try:
            resp = requests.post(ENDPOINT.format(model=model), json=body, timeout=timeout,
                                 headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
        except requests.RequestException as e:
            print(f"gemini {model}: {type(e).__name__}")
            last = e
            continue
        if resp.status_code < 400:
            print(f"gemini {model}: ok")
            out = resp.json()["candidates"][0]["content"]["parts"]
            return "".join(p.get("text", "") for p in out).strip()
        print(f"gemini {model}: http {resp.status_code} {' '.join(resp.text.split())[:200]}")
        last = requests.HTTPError(f"gemini http {resp.status_code}")
        if resp.status_code not in RETRYABLE:
            break
    raise last
