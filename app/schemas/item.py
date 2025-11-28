"""Schémas de validation et de sérialisation pour les articles.

Ce module définit les schémas Pydantic/SQLModel utilisés pour valider
les données d'entrée et formater les réponses de l'API.
"""

from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    """Schéma de base contenant les champs communs des articles.

    Attributes:
        nom: Nom de l'article (1-255 caractères).
        prix: Prix de l'article en euros (doit être supérieur à 10).

    Example:
        >>> item = ItemBase(nom="Clavier", prix=49.99)
    """

    nom: str = Field(min_length=1, max_length=255)
    prix: float = Field(gt=10)


class ItemCreate(ItemBase):
    """Schéma pour la création d'un nouvel article.

    Hérite de tous les champs de ItemBase sans ajout de contraintes supplémentaires.
    Utilisé pour valider les données lors d'une requête POST.

    Example:
        >>> create_data = ItemCreate(nom="Souris gaming", prix=59.99)
        >>> response = client.post("/items/", json=create_data.model_dump())
    """

    pass


class ItemUpdate(SQLModel):
    """Schéma pour la mise à jour partielle d'un article.

    Tous les champs sont optionnels pour permettre des mises à jour partielles.
    Utilisé pour valider les données lors d'une requête PUT.

    Attributes:
        nom: Nouveau nom de l'article (optionnel, 1-255 caractères si fourni).
        prix: Nouveau prix de l'article (optionnel, doit être positif si fourni).

    Example:
        >>> update_data = ItemUpdate(prix=39.99)
        >>> response = client.put("/items/1",
            json=update_data.model_dump(exclude_unset=True))
    """

    nom: str | None = Field(None, min_length=1, max_length=255)
    prix: float | None = Field(None, gt=0)


class ItemResponse(ItemBase):
    """Schéma de réponse pour un article.

    Étend ItemBase en ajoutant l'identifiant unique généré par la base de données.
    Utilisé pour sérialiser les articles dans les réponses HTTP.

    Attributes:
        id: Identifiant unique de l'article (généré automatiquement).

    Example:
        >>> item = ItemResponse(id=1, nom="Écran 24 pouces", prix=199.99)
        >>> return item  # FastAPI le convertit automatiquement en JSON
    """

    id: int
