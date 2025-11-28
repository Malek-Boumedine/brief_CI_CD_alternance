"""Configuration de la base de données et gestion des sessions.

Ce module gère la connexion à la base de données PostgreSQL
et fournit une fonction générateur pour obtenir des sessions de base de données.
"""

import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "database_url")
"""str: URL de connexion à la base de données PostgreSQL.

L'URL est chargée depuis la variable d'environnement DATABASE_URL.
Par défaut, utilise "database_url" si la variable n'est pas définie.
"""

engine = create_engine(DATABASE_URL)
"""Engine: Moteur SQLModel pour les opérations de base de données.

Cet objet gère le pool de connexions et l'exécution des requêtes SQL.
"""


def get_db() -> Generator[Session]:
    """Générateur de sessions de base de données pour l'injection de
    dépendances FastAPI.

    Crée une session SQLModel dans un contexte géré qui garantit
    la fermeture propre de la session après utilisation.

    Yields:
        Session: Session de base de données active pour effectuer des opérations CRUD.

    Example:
        >>> from fastapi import Depends
        >>> def my_endpoint(db: Session = Depends(get_db)):
        ...     items = db.exec(select(Item)).all()
        ...     return items
    """
    with Session(engine) as session:
        yield session
