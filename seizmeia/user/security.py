from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError  # type: ignore
from pydantic import ValidationError
from sqlalchemy.orm import Session

from seizmeia.db import get_db
from seizmeia.token.encode import decode_access_token
from seizmeia.token.schemas import TokenData
from seizmeia.user import db, schemas
from seizmeia.user.password import get_password_hash, verify_password

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token", scopes={"me": "Read information about the current user."}
)


def authenticate_user(
    session: Session, username: str, password: str
) -> schemas.User | None:
    hashed_password = db.get_user_password(session, username)
    if not hashed_password:
        return None

    if not verify_password(password, hashed_password):
        return None

    return db.get_user_by_username(session, username)


def create_user_w_hashed_password(
    session: Session, user: schemas.UserCreate
) -> schemas.User:
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    return db.create_user(session, user)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = decode_access_token(token=token)
        username: str | None = str(payload.get("sub", None))
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = db.get_user_by_username(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user
