# Real Estate AI Project

Plateforme d'estimation immobilière basée sur un modèle de machine learning.

## Stack
- Backend: Flask + SQLAlchemy
- Machine Learning: scikit-learn
- Base de données: PostgreSQL
- Frontend: React (structure initialisée)

## Démarrage backend
```bash
cd backend
python -m pip install -r requirements.txt
python app.py
```

## Entraîner le modèle
```bash
cd backend
python train_model.py
```
Le script lit `data/raw/sample_properties.csv` et sauvegarde `models/model_v1.pkl`.


## Démarrage frontend
```bash
cd frontend
npm install
npm run dev
```
L'application sera accessible sur `http://localhost:5173` et appellera l'API Flask (`http://localhost:5000`).

## Lancer avec Docker Compose
```bash
cd ..
docker compose -f real-estate-ai-project/docker-compose.yml up --build
```
Cela démarre PostgreSQL sur `5432` et l'API Flask sur `5000`.

## API
### `GET /health`
Retourne l'état du service.

### `POST /predict`
Exemple de payload:
```json
{
  "surface": 92,
  "rooms": 4,
  "bedrooms": 3,
  "city": "Lyon",
  "construction_year": 2011,
  "has_garage": true,
  "has_garden": false,
  "has_balcony": true
}
```


## Tests
```bash
cd ..
pytest -q real-estate-ai-project/tests/test_model.py
pytest -q real-estate-ai-project/tests/test_api.py
```
