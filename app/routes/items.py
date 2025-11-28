"""Routes de l'API pour la gestion des articles.

Ce module définit tous les endpoints REST pour effectuer des opérations CRUD
sur les articles (items).
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database import get_db
from app.models.item import Item
from app.schemas.item import ItemResponse, ItemUpdate
from app.services.item_service import ItemCreate, ItemService

router = APIRouter(prefix="/items", tags=["items"])
"""APIRouter: Routeur FastAPI pour les endpoints /items."""

MAX_ITEMS_PER_PAGE = 100
"""int: Nombre maximum d'articles retournés par page."""


@router.get("/", response_model=list[ItemResponse])
def get_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=MAX_ITEMS_PER_PAGE),
    max_prix: float | None = Query(None, ge=0),
    db: Session = Depends(get_db),
) -> list[Item]:
    """Récupère la liste paginée des articles avec filtre optionnel sur le prix.

    Args:
        page: Numéro de la page à récupérer (commence à 1).
        page_size: Nombre d'articles par page (max 100).
        max_prix: Prix maximum pour filtrer les articles (optionnel).
        db: Session de base de données injectée.

    Returns:
        list[Item]: Liste des articles correspondant aux critères.

    Example:
        >>> response = client.get("/items/?page=1&page_size=10&max_prix=50")
        >>> items = response.json()
    """
    offset = (page - 1) * page_size
    items = ItemService.get_all(db, skip=offset, limit=page_size)
    if max_prix is not None:
        items = [item for item in items if item.prix <= max_prix]
    return items


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    """Récupère un article spécifique par son ID.

    Args:
        item_id: Identifiant unique de l'article.
        db: Session de base de données injectée.

    Returns:
        Item: L'article correspondant à l'ID.

    Raises:
        HTTPException: 404 si l'article n'existe pas.

    Example:
        >>> response = client.get("/items/1")
        >>> item = response.json()
    """
    item = ItemService.get_by_id(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)) -> Item:
    """Crée un nouvel article.

    Args:
        item_data: Données validées pour créer l'article.
        db: Session de base de données injectée.

    Returns:
        Item: L'article nouvellement créé avec son ID généré.

    Example:
        >>> response = client.post("/items/", json={"nom": "Souris", "prix": 25.99})
        >>> new_item = response.json()
    """
    return ItemService.create(db, item_data)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)
) -> Item:
    """Met à jour un article existant.

    Args:
        item_id: Identifiant unique de l'article à modifier.
        item_data: Données de mise à jour (champs optionnels).
        db: Session de base de données injectée.

    Returns:
        Item: L'article mis à jour.

    Raises:
        HTTPException: 404 si l'article n'existe pas.

    Example:
        >>> response = client.put("/items/1", json={"prix": 29.99})
        >>> updated_item = response.json()
    """
    item = ItemService.update(db, item_id, item_data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    """Supprime un article de la base de données.

    Args:
        item_id: Identifiant unique de l'article à supprimer.
        db: Session de base de données injectée.

    Raises:
        HTTPException: 404 si l'article n'existe pas.

    Example:
        >>> response = client.delete("/items/1")
        >>> assert response.status_code == 204
    """
    deleted = ItemService.delete(db, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )


def _old_helper_function(data: str) -> str:
    """Fonction helper dépréciée conservée pour compatibilité.

    Args:
        data: Chaîne de caractères à transformer.

    Returns:
        str: Chaîne en majuscules.

    Note:
        Cette fonction n'est plus utilisée et sera supprimée dans une version future.

    Deprecated:
        Utilisez str.upper() directement à la place.
    """
    return data.upper()
