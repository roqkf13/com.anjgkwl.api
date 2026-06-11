"""Ollama 로컬 LLM 클라이언트 — get_ollama_client()로 싱글턴 인스턴스를 주입받는다."""

import os
from functools import lru_cache

from ollama import Client

DEFAULT_OLLAMA_MODEL = "llama3.2"


@lru_cache
def get_ollama_base_url() -> str:
    return (os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434").strip()


@lru_cache
def get_ollama_model_name() -> str:
    return (os.getenv("OLLAMA_MODEL") or DEFAULT_OLLAMA_MODEL).strip()


@lru_cache
def get_ollama_client() -> Client:
    return Client(host=get_ollama_base_url())


def generate_reply_ollama(*, message: str) -> str:
    client = get_ollama_client()
    model = get_ollama_model_name()
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": message}],
    )
    text = (response.message.content or "").strip()
    if not text:
        raise ValueError("Ollama가 비어 있는 응답을 반환했습니다.")
    return text


__all__ = [
    "get_ollama_client",
    "get_ollama_base_url",
    "get_ollama_model_name",
    "generate_reply_ollama",
]
