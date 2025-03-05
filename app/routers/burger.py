from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.domain import burger as domain
from app.services import burger_service
from app.db import connection
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/", response_model=List[domain.BurgerBase], status_code=200)
@limiter.limit("15/minute")
async def read_burgers(request: Request, db: Session = Depends(connection.get_db)):
    return burger_service.get_burgers(db)

@router.post("/v1/", response_model=domain.Burger, status_code=201)
@limiter.limit("5/minute")
async def create_burger(request: Request, burger: domain.BurgerCreate, db: Session = Depends(connection.get_db)):
    return burger_service.create_burger(db, burger)

@router.get("/v1/{burger_id}", response_model=domain.BurgerResponse, status_code=200)
@limiter.limit("15/minute")
async def read_burger(request: Request, burger_id: int, db: Session = Depends(connection.get_db)):
    return burger_service.get_burger(db, burger_id)

@router.put("/v1/{burger_id}", response_model=domain.Burger, status_code=201)
@limiter.limit("5/minute")
async def update_burger(request: Request, burger_id: int, burger: domain.BurgerCreate, db: Session = Depends(connection.get_db)):
    return burger_service.update_burger(db, burger_id, burger)

@router.delete("/v1/{burger_id}", status_code=204)
@limiter.limit("5/minute")
async def delete_burger(request: Request, burger_id: int, db: Session = Depends(connection.get_db)):
    return burger_service.delete_burger(db, burger_id)
