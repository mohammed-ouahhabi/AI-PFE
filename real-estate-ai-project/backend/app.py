"""API Flask pour estimation immobilière."""
from __future__ import annotations

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from database import Prediction, Property, SessionLocal, init_db
from predict import predict_price, validate_payload


def create_app() -> Flask:
    """Crée et configure l'application Flask."""

    app = Flask(__name__)
    CORS(app)
    init_db()

    @app.get("/health")
    def health_check():
        """Vérifie la disponibilité de l'API."""

        return jsonify({"status": "ok"}), 200

    @app.post("/predict")
    def predict():
        """Prédit le prix d'un bien et stocke la requête en base PostgreSQL."""

        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "Corps JSON invalide ou manquant"}), 400

        try:
            features = validate_payload(payload)
            estimated_price = predict_price(features)
        except (ValueError, FileNotFoundError) as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": f"Erreur modèle: {exc}"}), 500

        db = SessionLocal()
        try:
            property_row = Property(**features)
            db.add(property_row)
            db.flush()

            prediction_row = Prediction(
                property_id=property_row.id,
                predicted_price=estimated_price,
                model_version="v1",
            )
            db.add(prediction_row)
            db.commit()
        except SQLAlchemyError as exc:
            db.rollback()
            return jsonify({"error": f"Erreur base de données: {exc}"}), 500
        finally:
            db.close()

        return (
            jsonify(
                {
                    "estimated_price": estimated_price,
                    "currency": "EUR",
                    "model_version": "v1",
                }
            ),
            200,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
