"""Configuration de la base de données PostgreSQL et modèles ORM."""
from __future__ import annotations

import os
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Exemple: postgresql+psycopg2://postgres:postgres@localhost:5432/real_estate_ai
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/real_estate_ai",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """Utilisateur de la plateforme."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    predictions = relationship("Prediction", back_populates="user")


class Property(Base):
    """Bien immobilier décrit par l'utilisateur."""

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    surface = Column(Float, nullable=False)
    rooms = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    city = Column(String(100), nullable=False)
    construction_year = Column(Integer, nullable=False)
    has_garage = Column(Boolean, nullable=False)
    has_garden = Column(Boolean, nullable=False)
    has_balcony = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    predictions = relationship("Prediction", back_populates="property")


class Prediction(Base):
    """Résultat d'estimation produit par le modèle."""

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    predicted_price = Column(Float, nullable=False)
    model_version = Column(String(50), default="v1", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="predictions")
    property = relationship("Property", back_populates="predictions")
    feedback = relationship("Feedback", back_populates="prediction", uselist=False)


class Feedback(Base):
    """Retour utilisateur post-prédiction."""

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=False, unique=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    prediction = relationship("Prediction", back_populates="feedback")


def init_db() -> None:
    """Crée les tables si elles n'existent pas."""

    Base.metadata.create_all(bind=engine)
