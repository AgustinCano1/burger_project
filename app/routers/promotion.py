from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.domain import promotion as domain
from app.services import promotion_service
from app.db import connection
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/v1/", response_model=domain.Promotion, status_code=201)
@limiter.limit("5/minute")
async def create_promotion(request: Request, promotion: domain.PromotionCreate, db: Session = Depends(connection.get_db)):
    return promotion_service.create_promotion(db, promotion)

@router.get("/v1/{promotion_id}", response_model=domain.PromotionResponse, status_code=200)
@limiter.limit("15/minute")
async def read_promotion(request: Request, promotion_id: int, db: Session = Depends(connection.get_db)):
    return promotion_service.get_promotion(db, promotion_id)

@router.put("/v1/{promotion_id}", response_model=domain.Promotion, status_code=201)
@limiter.limit("5/minute")
async def update_promotion(request: Request, promotion_id: int, promotion: domain.PromotionCreate, db: Session = Depends(connection.get_db)):
    return promotion_service.update_promotion(db, promotion_id, promotion)

@router.delete("/v1/{promotion_id}", status_code=204)
@limiter.limit("5/minute")
async def delete_promotion(request: Request, promotion_id: int, db: Session = Depends(connection.get_db)):
    return promotion_service.delete_promotion(db, promotion_id)
