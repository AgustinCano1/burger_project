from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import models
from app.domain import store as domain
from app.utils.error_messages import STORE_NOT_FOUND

def create_store(db: Session, store: domain.StoreCreate):
    db_store = models.Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def get_store(db: Session, store_id: int):
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if db_store is None:
        raise HTTPException(status_code=404, detail=STORE_NOT_FOUND)

    # get burgers of the store
    burgers = db.query(models.Burger.name).join(models.StoresBurgers).filter(
            models.StoresBurgers.burger_id == models.Burger.id,
            models.StoresBurgers.store_id == db_store.id
        ).all()

    # get open days of the store
    open_days = []
    if db_store.monday == 1:
        open_days.append("Monday")
    if db_store.tuesday == 1:
        open_days.append("Tuesday")
    if db_store.wednesday == 1:
        open_days.append("Wednesday")
    if db_store.thursday == 1:
        open_days.append("Thursday")
    if db_store.friday == 1:
        open_days.append("Friday")
    if db_store.saturday == 1:
        open_days.append("Saturday")
    if db_store.sunday == 1:
        open_days.append("Sunday")

    store_response = domain.StoreResponse(
        name=db_store.name,
        latitude=str(db_store.latitude),
        longitude=str(db_store.longitude),
        is_24hrs="Yes" if db_store.is_24hrs == 1 else "No",
        has_drive_thru="Yes" if db_store.has_drive_thru == 1 else "No",
        open_days=open_days,
        burgers=[burger.name for burger in burgers]
    )
    
    return store_response

def update_store(db: Session, store_id: int, store: domain.StoreCreate):
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if db_store is None:
        raise HTTPException(status_code=404, detail=STORE_NOT_FOUND)
    for key, value in store.dict().items():
        setattr(db_store, key, value)
    db.commit()
    db.refresh(db_store)
    return db_store

def delete_store(db: Session, store_id: int):
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if db_store is None:
        raise HTTPException(status_code=404, detail=STORE_NOT_FOUND)
    db_store.status = 0
    db.commit()
    db.refresh(db_store)
    return db_store