"""Modèle de données pour les articles.

Ce module définit le modèle SQLModel pour la table des articles
dans la base de données PostgreSQL.
"""

from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    """Modèle représentant un article dans la base de données.

    Cette classe définit la structure de la table 'items' et les contraintes
    associées. Elle est utilisée à la fois comme modèle ORM et comme schéma
    de validation.

    Attributes:
        id: Identifiant unique auto-incrémenté de l'article.
        nom: Nom de l'article, indexé pour améliorer les performances de recherche.
        prix: Prix de l'article en euros.

    Example:
        >>> item = Item(nom="Clavier mécanique", prix=89.99)
        >>> db.add(item)
        >>> db.commit()
        >>> print(item.id)  # ID auto-généré
        1
    """

    __tablename__ = "items"

    id: int | None = Field(default=None, primary_key=True)
    nom: str = Field(index=True)
    prix: float

    def _legacy_method(self) -> None:
        """Méthode héritée conservée pour compatibilité.

        Note:
            Cette méthode est dépréciée et sera supprimée dans une version future.
        """
        pass
