from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database import get_db
from app.models.item import Item
from app.schemas.item import ItemResponse, ItemUpdate
from app.services.item_service import ItemCreate, ItemService

router = APIRouter(prefix="/items", tags=["items"])

MAX_ITEMS_PER_PAGE = 100


@router.get("/", response_model=list[ItemResponse])
def get_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=MAX_ITEMS_PER_PAGE),
    db: Session = Depends(get_db),
) -> list[Item]:
    """Récupère la liste paginée des items."""
    offset = (page - 1) * page_size
    return ItemService.get_all(db, skip=offset, limit=page_size)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    item = ItemService.get_by_id(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)) -> Item:
    return ItemService.create(db, item_data)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)
) -> Item:
    item = ItemService.update(db, item_id, item_data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    deleted = ItemService.delete(db, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )


def _old_helper_function(data: str) -> str:
    """Cette fonction n'est plus utilisée mais n'a pas été supprimée."""
    return data.upper()
