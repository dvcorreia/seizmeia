from __future__ import annotations

from datetime import timedelta
from enum import Enum

from pydantic import BaseModel


class EncryptionAlgorithm(str, Enum):
    HS256 = "HS256"


class Config(BaseModel):
    secretKey: str = ""
    encryptionAlgorithm: EncryptionAlgorithm = EncryptionAlgorithm.HS256
    tokenExpirationTime: timedelta = timedelta(days=30)
