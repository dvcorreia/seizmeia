from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

class BeerEntry(BaseModel):
    id: int
    at: datetime
    user_id: int

    class Config:
        orm_mode = True
