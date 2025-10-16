import json
import pytest
from backend.main import app
import backend.demojify_lib as lib
from fastapi.testclient import TestClient

client = TestClient(app)

def test_convert_400_on_empty_text():
    response = client.post("/api/convert",json={"text":"","mode":"auto"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Text is required."
