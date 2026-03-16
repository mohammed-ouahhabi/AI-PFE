"""Tests unitaires de la validation des entrées du modèle."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from predict import _to_bool, validate_payload  # noqa: E402


def _valid_payload() -> dict:
    return {
        "surface": 85,
        "rooms": 4,
        "bedrooms": 3,
        "city": "Lyon",
        "construction_year": 2008,
        "has_garage": "true",
        "has_garden": False,
        "has_balcony": 1,
    }


def test_validate_payload_success():
    payload = validate_payload(_valid_payload())
    assert payload["surface"] == 85.0
    assert payload["has_garage"] is True
    assert payload["has_balcony"] is True


def test_validate_payload_missing_field():
    payload = _valid_payload()
    payload.pop("city")

    with pytest.raises(ValueError, match="Champs manquants"):
        validate_payload(payload)


def test_validate_payload_invalid_booleans():
    payload = _valid_payload()
    payload["has_garden"] = "peut-être"

    with pytest.raises(ValueError, match="booléen valide"):
        validate_payload(payload)


def test_validate_payload_bedrooms_gt_rooms():
    payload = _valid_payload()
    payload["bedrooms"] = 6

    with pytest.raises(ValueError, match="ne peut pas dépasser"):
        validate_payload(payload)


def test_validate_payload_empty_json():
    with pytest.raises(ValueError, match="Champs manquants"):
        validate_payload({})


def test_to_bool_variants():
    assert _to_bool("oui", "f") is True
    assert _to_bool("0", "f") is False
    assert _to_bool(1, "f") is True
    with pytest.raises(ValueError, match="doit valoir 0 ou 1"):
        _to_bool(2, "f")
