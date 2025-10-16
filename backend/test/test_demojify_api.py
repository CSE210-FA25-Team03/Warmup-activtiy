import json
from main import app
import demojify_lib as lib
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

client = TestClient(app)

def test_convert_400_on_empty_text():
    response = client.post("/api/convert",json={"text":"","mode":"auto"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Text is required."


def test_validator_accepts_llm(monkeypatch):
    fake_llm = Mock(return_value=json.dumps({"response": "hello world!"}))

    monkeypatch.setattr("demojify_lib.emoji_to_meaning", fake_llm)
    monkeypatch.setattr("demojify_lib.evaluate_consistency_zero_one", lambda *a, **k: 1)

    r = client.post("/api/convert", json={"text":"LOL soooo funny 😂😂","mode":"auto"})
    assert r.status_code == 200
    out = r.json()
    assert out["source"] == "llm"
    assert out["reason"] == "llm_valid"
    assert out["output"] == "hello world!"

    fake_llm.assert_called_once()

def test_standard_mode_bypasses_llm(monkeypatch):
    fake_llm = Mock(return_value=json.dumps({"response": "should not be used"}))
    fake_validator = Mock(return_value=1)

    # If STANDARD, neither LLM nor validator should run
    monkeypatch.setattr("demojify_lib.emoji_to_meaning", fake_llm)
    monkeypatch.setattr("demojify_lib.evaluate_consistency_zero_one", fake_validator)

    r = client.post("/api/convert", json={"text": "Nice 😂", "mode": "standard"})
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "standard"
    assert body["reason"] == "rules_only"
    fake_llm.assert_not_called()
    fake_validator.assert_not_called()

def test_validator_rejects_llm(monkeypatch):
    input_text = "Finally finished 😭😭🔥"

    # LLM path returns something different, but validator rejects it (0)
    fake_llm = Mock(return_value=json.dumps({"response": "I am devastated."}))
    monkeypatch.setattr("demojify_lib.emoji_to_meaning", fake_llm)
    monkeypatch.setattr("demojify_lib.evaluate_consistency_zero_one", lambda *a, **k: 0)

    r = client.post("/api/convert", json={"text": input_text, "mode": "auto"})
    assert r.status_code == 200
    body = r.json()

    assert body["source"] == "standard"
    assert body["reason"] == "validator_rejected"

    expected_standard = lib.emoji_semantic_clean(input_text)
    assert body["output"] == expected_standard

    fake_llm.assert_called_once()

def test_validator_error_fallback(monkeypatch):
    input_text = "I can’t believe this 😂🔥"

    fake_llm = Mock(return_value=json.dumps({"response": "That’s awesome!"}))
    monkeypatch.setattr("demojify_lib.emoji_to_meaning", fake_llm)

    # Validator returns None → simulate invalid / junk response
    monkeypatch.setattr("demojify_lib.evaluate_consistency_zero_one", lambda *a, **k: None)

    r = client.post("/api/convert", json={"text": input_text, "mode": "auto"})
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "standard"
    assert body["reason"] == "validator_error"
    expected_standard = lib.emoji_semantic_clean(input_text)
    assert body["output"] == expected_standard

    fake_llm.assert_called_once()

def test_llm_json_with_emoji_gets_sanitized(monkeypatch):
    monkeypatch.setattr("demojify_lib.emoji_to_meaning",
        lambda *a, **k: json.dumps({"response":"Great job 🎉"}), raising=False)
    monkeypatch.setattr("demojify_lib.evaluate_consistency_zero_one", lambda *a, **k: 1, raising=False)

    r = client.post("/api/convert", json={"text":"Great job 🎉", "mode":"auto"})
    assert r.status_code == 200
    assert "🎉" not in r.json()["output"]

@pytest.mark.parametrize("inp, expect_nonempty", [("😂😂", True), ("🔥", True), ("!!!", False)])
def test_standard_emoji_only(inp, expect_nonempty):
    r = client.post("/api/convert", json={"text": inp, "mode":"standard"})
    assert r.status_code == 200
    assert (r.json()["output"] != "") is expect_nonempty

def test_health_contract():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert "ok" in data and "llm_client" in data and "model" in data

def test_when_llm_client_none_uses_standard(monkeypatch):
    # simulate app boot with no LLM client
    monkeypatch.setattr("main.OpenAIClient", None, raising=False)

    r = client.post("/api/convert", json={"text":"Nice 😂", "mode":"auto"})
    assert r.status_code == 200
    out = r.json()
    assert out["source"] == "standard"
    assert out["reason"] == "rules_only" or out["reason"].startswith("llm_error")
