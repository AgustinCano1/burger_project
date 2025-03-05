from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.domain import ingredient as domain
from app.services import ingredient_service
from app.db import connection
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/v1/", response_model=domain.Ingredient, status_code=201)
@limiter.limit("5/minute")
async def create_ingredient(request: Request, ingredient: domain.IngredientCreate, db: Session = Depends(connection.get_db)):
    return ingredient_service.create_ingredient(db, ingredient)

@router.get("/v1/{ingredient_id}", response_model=domain.IngredientBase, status_code=200)
@limiter.limit("15/minute")
async def read_ingredient(request: Request, ingredient_id: int, db: Session = Depends(connection.get_db)):
    return ingredient_service.get_ingredient(db, ingredient_id)

@router.put("/v1/{ingredient_id}", response_model=domain.Ingredient, status_code=201)
@limiter.limit("5/minute")
async def update_ingredient(request: Request, ingredient_id: int, ingredient: domain.IngredientCreate, db: Session = Depends(connection.get_db)):
    return ingredient_service.update_ingredient(db, ingredient_id, ingredient)

@router.delete("/v1/{ingredient_id}", status_code=204)
@limiter.limit("5/minute")
async def delete_ingredient(request: Request, ingredient_id: int, db: Session = Depends(connection.get_db)):
    return ingredient_service.delete_ingredient(db, ingredient_id)
