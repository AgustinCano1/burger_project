from typing import Optional
from pydantic import BaseModel

class StoreBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    is_24hrs: Optional[int] = 0
    has_drive_thru: Optional[int] = 0
    monday: Optional[int] = 0
    tuesday: Optional[int] = 0
    wednesday: Optional[int] = 0
    thursday: Optional[int] = 0
    friday: Optional[int] = 0
    saturday: Optional[int] = 0
    sunday: Optional[int] = 0

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int

    class Config:
        orm_mode = True

class StoreResponse(BaseModel):
    name: str = ""
    latitude: str = ""
    longitude: str = ""
    is_24hrs: str = ""
    has_drive_thru: str = ""
    open_days: list = []
    burgers: list = []

    def __init__(self,
                 name: str = "",
                 latitude: str = "",
                 longitude: str = "",
                 is_24hrs: str = "",
                 has_drive_thru: str = "",
                 open_days: list = None,
                 burgers: list = None,
                 **data):
        super().__init__(**data)
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.is_24hrs = is_24hrs
        self.has_drive_thru = has_drive_thru
        self.open_days = open_days
        self.burgers = burgers
