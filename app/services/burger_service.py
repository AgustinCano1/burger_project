from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import models
from app.domain import burger as domain
from app.utils.error_messages import BURGUER_NOT_FOUND

def get_burgers(db: Session):
    db_burgers = db.query(models.Burger).all()
    return [domain.BurgerBase(
        description=f"{burger.name} - {burger.description}",
        price=f"${burger.price}",
    ) for burger in db_burgers]

def create_burger(db: Session, burger: domain.BurgerCreate):
    db_burger = models.Burger(**burger.dict())
    db.add(db_burger)
    db.commit()
    db.refresh(db_burger)
    return db_burger

def get_burger(db: Session, burger_id: int):
    db_burger = db.query(models.Burger).filter(models.Burger.id == burger_id).first()
    if db_burger is None:
        raise HTTPException(status_code=404, detail=BURGUER_NOT_FOUND)

    # get ingredients of the burger
    ingredients = db.query(models.Ingredient.name).join(models.BurgersIngredients).filter(
            models.BurgersIngredients.burger_id == db_burger.id,
            models.BurgersIngredients.ingredient_id == models.Ingredient.id
        ).all()

    ingredient_names = [ingredient.name for ingredient in ingredients]

    # get stores that sell the burger
    stores = db.query(models.Store.name).join(models.StoresBurgers).filter(
            models.StoresBurgers.burger_id == db_burger.id,
            models.StoresBurgers.store_id == models.Store.id
        ).all()

    stores_names = [store.name for store in stores]

    # get promotions of the burger
    promotions = db.query(models.Promotion).join(models.Burger).filter(
            models.Promotion.burger_id == db_burger.id
        ).all()

    promotions_discounts = [f"-${promotion.discount}" for promotion in promotions
                          if promotion.discount is not None and promotion.discount > 0]

    promotions_p_discounts = [f"-{promotion.percentage_discount}%" for promotion in promotions
                            if promotion.percentage_discount is not None and promotion.percentage_discount > 0]

    burger_res = domain.BurgerResponse(
        description=f"{db_burger.name} - {db_burger.description}",
        price=f"${db_burger.price}",
        ingredients=ingredient_names,
        stores=stores_names,
        promotions=promotions_discounts + promotions_p_discounts
    )
    return burger_res

def update_burger(db: Session, burger_id: int, burger: domain.BurgerCreate):
    db_burger = db.query(models.Burger).filter(models.Burger.id == burger_id).first()
    if db_burger is None:
        raise HTTPException(status_code=404, detail=BURGUER_NOT_FOUND)
    for key, value in burger.dict().items():
        setattr(db_burger, key, value)
    db.commit()
    db.refresh(db_burger)
    return db_burger

def delete_burger(db: Session, burger_id: int):
    db_burger = db.query(models.Burger).filter(models.Burger.id == burger_id).first()
    if db_burger is None:
        raise HTTPException(status_code=404, detail=BURGUER_NOT_FOUND)
    db_burger.status = 0
    db.commit()
    db.refresh(db_burger)
    return db_burger
