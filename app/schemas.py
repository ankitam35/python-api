from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ItemBase(BaseModel):
    """Base schema for Item."""
    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Schema for creating an Item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an Item."""
    name: Optional[str] = None
    description: Optional[str] = None


class ItemResponse(ItemBase):
    """Schema for Item response."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
