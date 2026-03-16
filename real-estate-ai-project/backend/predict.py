"""Logique de prédiction du prix immobilier."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "model_v1.pkl"

REQUIRED_FIELDS = {
    "surface",
    "rooms",
    "bedrooms",
    "city",
    "construction_year",
    "has_garage",
    "has_garden",
    "has_balcony",
}

TRUE_VALUES = {"true", "1", "yes", "oui", "on"}
FALSE_VALUES = {"false", "0", "no", "non", "off"}


@lru_cache(maxsize=1)
def load_model() -> Any:
    """Charge le modèle entraîné depuis le disque."""

    import joblib

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modèle introuvable: {MODEL_PATH}. Entraînez puis sauvegardez model_v1.pkl."
        )
    return joblib.load(MODEL_PATH)


def _to_bool(value: Any, field_name: str) -> bool:
    """Convertit un booléen robuste depuis bool/int/str.

    Évite le piège Python: bool("false") == True.
    """

    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value in (0, 1):
            return bool(value)
        raise ValueError(f"{field_name} doit valoir 0 ou 1")
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in TRUE_VALUES:
            return True
        if normalized in FALSE_VALUES:
            return False
    raise ValueError(f"{field_name} doit être un booléen valide")


def validate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Valide et convertit les champs d'entrée venant du frontend."""

    missing = REQUIRED_FIELDS.difference(payload.keys())
    if missing:
        raise ValueError(f"Champs manquants: {sorted(missing)}")

    try:
        normalized = {
            "surface": float(payload["surface"]),
            "rooms": int(payload["rooms"]),
            "bedrooms": int(payload["bedrooms"]),
            "city": str(payload["city"]).strip(),
            "construction_year": int(payload["construction_year"]),
            "has_garage": _to_bool(payload["has_garage"], "has_garage"),
            "has_garden": _to_bool(payload["has_garden"], "has_garden"),
            "has_balcony": _to_bool(payload["has_balcony"], "has_balcony"),
        }
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Format de données invalide: {exc}") from exc

    if normalized["surface"] <= 0:
        raise ValueError("surface doit être > 0")
    if normalized["rooms"] <= 0 or normalized["bedrooms"] < 0:
        raise ValueError("rooms doit être > 0 et bedrooms doit être >= 0")
    if normalized["bedrooms"] > normalized["rooms"]:
        raise ValueError("bedrooms ne peut pas dépasser rooms")
    if not normalized["city"]:
        raise ValueError("city ne peut pas être vide")
    if not 1700 <= normalized["construction_year"] <= 2100:
        raise ValueError("construction_year doit être compris entre 1700 et 2100")

    return normalized


def predict_price(features: Dict[str, Any]) -> float:
    """Retourne un prix estimé en euros à partir des caractéristiques du bien."""

    import pandas as pd

    model = load_model()
    frame = pd.DataFrame([features])
    prediction = model.predict(frame)[0]
    return float(prediction)
