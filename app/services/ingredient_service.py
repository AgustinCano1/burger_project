from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import models
from app.domain import ingredient as domain
from app.utils.error_messages import INGREDIENT_NOT_FOUND

def create_ingredient(db: Session, ingredient: domain.IngredientCreate):
    db_ingredient = models.Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def get_ingredient(db: Session, ingredient_id: int):
    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail=INGREDIENT_NOT_FOUND)
    return db_ingredient

def update_ingredient(db: Session, ingredient_id: int, ingredient: domain.IngredientCreate):
    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail=INGREDIENT_NOT_FOUND)
    for key, value in ingredient.dict().items():
        setattr(db_ingredient, key, value)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def delete_ingredient(db: Session, ingredient_id: int):
    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail=INGREDIENT_NOT_FOUND)
    db_ingredient.status = 0
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient
