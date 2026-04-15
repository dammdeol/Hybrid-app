from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ItemModel

router = APIRouter(prefix="/items", tags=["items"])


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    price: float = Field(..., gt=0)


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    price: Optional[float] = Field(None, gt=0)


class ItemOut(ItemCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


@router.get("", response_model=Page[ItemOut])
def list_items(
    name: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, gt=0),
    max_price: Optional[float] = Query(None, gt=0),
    db: Session = Depends(get_db)
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price",
        )
    query = select(ItemModel).order_by(ItemModel.id.asc())
    if name:
        query = query.where(ItemModel.name.ilike(f"%{name}%"))

    if min_price is not None:
        query = query.where(ItemModel.price >= min_price)

    if max_price is not None:
        query = query.where(ItemModel.price <= max_price)
    return paginate(db, query)


@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    existing_item = db.query(ItemModel).filter(
        ItemModel.name == payload.name).first()
    if existing_item:
        raise HTTPException(status_code=409, detail="Item name already exists")

    item = ItemModel(name=payload.name, price=payload.price)
    db.add(item)
    try:
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Database integrity error")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{item_id}", response_model=ItemOut)
def patch_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if payload.name is not None:
        existing_item = (
            db.query(ItemModel)
            .filter(ItemModel.name == payload.name, ItemModel.id != item_id)
            .first()
        )
        if existing_item:
            raise HTTPException(
                status_code=409, detail="Item name already exists")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(item, field, value)

    try:
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Database integrity error")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Database integrity error")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
