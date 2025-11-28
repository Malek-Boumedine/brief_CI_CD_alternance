"""Point d'entrée principal de l'application FastAPI.

Ce module configure l'application FastAPI, initialise la base de données
et enregistre les routes de l'API.
"""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routes import items_router

load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE", True)
"""bool: Mode debug de l'application.

Chargé depuis la variable d'environnement DEBUG_MODE.
Active les logs détaillés et les messages d'erreur complets.
"""


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None]:
    """Gestionnaire du cycle de vie de l'application FastAPI.

    Exécute des actions au démarrage et à l'arrêt de l'application.
    Crée automatiquement toutes les tables de la base de données au démarrage.

    Args:
        fastapi_app: Instance de l'application FastAPI.

    Yields:
        None: Contrôle rendu à l'application pendant son exécution.

    Example:
        >>> app = FastAPI(lifespan=lifespan)
    """
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Items CRUD API",
    description="API pour gérer une liste d'articles",
    version="1.0.0",
    lifespan=lifespan,
)
"""FastAPI: Instance principale de l'application FastAPI.

Configure l'API avec ses métadonnées et son gestionnaire de cycle de vie.
"""

app.include_router(items_router)


@app.get("/")
def root() -> dict[str, str]:
    """Endpoint racine de l'API.

    Retourne un message de bienvenue pour confirmer que l'API fonctionne.

    Returns:
        dict[str, str]: Message de bienvenue.

    Example:
        >>> response = client.get("/")
        >>> response.json()
        {'message': 'Items CRUD API'}
    """
    return {"message": "Items CRUD API"}


@app.get("/health")
def health() -> dict[str, str]:
    """Endpoint de vérification de santé de l'API.

    Utilisé par les orchestrateurs (Docker, Kubernetes) pour vérifier
    que l'application répond correctement.

    Returns:
        dict[str, str]: Statut de santé de l'application.

    Example:
        >>> response = client.get("/health")
        >>> response.json()
        {'status': 'healthy'}
    """
    return {"status": "healthy"}
