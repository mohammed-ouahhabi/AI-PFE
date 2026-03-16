"""Script d'entraînement local du modèle immobilier (RandomForestRegressor)."""
from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "sample_properties.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "model_v1.pkl"

NUMERIC_FEATURES = [
    "surface",
    "rooms",
    "bedrooms",
    "construction_year",
    "has_garage",
    "has_garden",
    "has_balcony",
]
CATEGORICAL_FEATURES = ["city"]
TARGET = "price"


def train_and_save_model() -> None:
    """Entraîne un pipeline sklearn puis sauvegarde le modèle en .pkl."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Données introuvables: {RAW_DATA_PATH}")

    data = pd.read_csv(RAW_DATA_PATH)
    features = data[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    target = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("num", "passthrough", NUMERIC_FEATURES),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=250,
                    random_state=42,
                    min_samples_split=2,
                    min_samples_leaf=1,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Modèle sauvegardé: {MODEL_PATH}")
    print(f"MAE: {mae:.2f}")
    print(f"R2: {r2:.4f}")


if __name__ == "__main__":
    train_and_save_model()
