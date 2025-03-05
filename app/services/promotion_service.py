from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import models
from app.domain import promotion as domain
from app.utils.error_messages import PROMOTION_NOT_FOUND

def create_promotion(db: Session, promotion: domain.PromotionCreate):
    db_promotion = models.Promotion(**promotion.dict())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

def get_promotion(db: Session, promotion_id: int):
    db_promotion = db.query(models.Promotion).filter(models.Promotion.id == promotion_id).first()
    if db_promotion is None:
        raise HTTPException(status_code=404, detail=PROMOTION_NOT_FOUND)

    # get burger of the promotion
    burger = db.query(models.Burger).filter(
            models.Burger.id == db_promotion.burger_id,
        ).first()

    promotion_res = domain.PromotionResponse(
        burger=burger.name,
        discount=f"-{db_promotion.discount}",
        percentage_discount=f"-{db_promotion.percentage_discount}%",
        start_date=db_promotion.start_date,
        end_date=db_promotion.end_date
    )

    return promotion_res

def update_promotion(db: Session, promotion_id: int, promotion: domain.PromotionCreate):
    db_promotion = db.query(models.Promotion).filter(models.Promotion.id == promotion_id).first()
    if db_promotion is None:
        raise HTTPException(status_code=404, detail=PROMOTION_NOT_FOUND)
    for key, value in promotion.dict().items():
        setattr(db_promotion, key, value)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

def delete_promotion(db: Session, promotion_id: int):
    db_promotion = db.query(models.Promotion).filter(models.Promotion.id == promotion_id).first()
    if db_promotion is None:
        raise HTTPException(status_code=404, detail=PROMOTION_NOT_FOUND)
    db_promotion.status = 0
    db.commit()
    db.refresh(db_promotion)
    return db_promotion