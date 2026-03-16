"""Tests API Flask pour l'endpoint de prédiction."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

pytest.importorskip("flask")
pytest.importorskip("sqlalchemy")

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

import app as app_module  # noqa: E402


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setattr(app_module, "init_db", lambda: None)
    app = app_module.create_app()

    class _DummySession:
        def add(self, _obj):
            return None

        def flush(self):
            return None

        def commit(self):
            return None

        def rollback(self):
            return None

        def close(self):
            return None

    monkeypatch.setattr(app_module, "SessionLocal", lambda: _DummySession())
    monkeypatch.setattr(app_module, "predict_price", lambda _features: 321000.0)

    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_predict_success(client):
    payload = {
        "surface": 100,
        "rooms": 5,
        "bedrooms": 3,
        "city": "Paris",
        "construction_year": 2012,
        "has_garage": True,
        "has_garden": False,
        "has_balcony": True,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.get_json()
    assert body["estimated_price"] == 321000.0


def test_predict_bad_payload(client):
    response = client.post("/predict", json={"surface": 50})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_predict_invalid_json_body(client):
    response = client.post("/predict", data="not-json", content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.get_json()
