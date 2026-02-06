from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/v1", tags=["items"])


@router.get("/items", response_model=List[schemas.ItemResponse])
async def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all items."""
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items


@router.get("/items/{item_id}", response_model=schemas.ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a single item by ID."""
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("/items", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Create a new item."""
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/items/{item_id}", response_model=schemas.ItemResponse)
async def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item."""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item."""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return None
