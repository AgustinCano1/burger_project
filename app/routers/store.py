from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.domain import store as domain
from app.services import store_service
from app.db import connection
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/v1/", response_model=domain.Store, status_code=201)
@limiter.limit("5/minute")
async def create_store(request: Request, store: domain.StoreCreate, db: Session = Depends(connection.get_db)):
    return store_service.create_store(db, store)

@router.get("/{store_id}", response_model=domain.StoreResponse, status_code=200)
@limiter.limit("15/minute")
async def read_store(request: Request, store_id: int, db: Session = Depends(connection.get_db)):
    return store_service.get_store(db, store_id)

@router.put("/{store_id}", response_model=domain.Store, status_code=201)
@limiter.limit("5/minute")
async def update_store(request: Request, store_id: int, store: domain.StoreCreate, db: Session = Depends(connection.get_db)):
    return store_service.update_store(db, store_id, store)

@router.delete("/{store_id}", status_code=204)
@limiter.limit("5/minute")
async def delete_store(request: Request, store_id: int, db: Session = Depends(connection.get_db)):
    return store_service.delete_store(db, store_id)