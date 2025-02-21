from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from seizmeia.db import Base
from seizmeia.beersheet import schemas

class BeerEntry(Base):
    __tablename__ = "beer_entries"

    id = Column(Integer, primary_key=True, index=True)
    at = Column(DateTime, index=True, server_default=func.now())
    user_id = Column(ForeignKey("users.id"))

    user = relationship()

    def drink_beer(db: Session, user_id: int) -> None:
        beer_entry = BeerEntry(user_id=user_id)

        db.add(beer_entry)
        db.commit()

