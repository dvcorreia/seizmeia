from __future__ import annotations

from datetime import datetime, timedelta

from jose import jwt  # type: ignore

from seizmeia.settings import config


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    token_cfg = config.auth

    encoded_jwt = jwt.encode(
        to_encode,
        token_cfg.secretKey,
        algorithm=token_cfg.encryptionAlgorithm.value,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    token_cfg = config.auth

    return jwt.decode(
        token=token,
        key=token_cfg.secretKey,
        algorithms=[token_cfg.encryptionAlgorithm.value],
    )
