from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from seizmeia.db import get_db
from seizmeia.settings import config
from seizmeia.token.encode import create_access_token
from seizmeia.token.schemas import Token
from seizmeia.user.security import authenticate_user

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )

    token_cfg = config.auth

    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=token_cfg.tokenExpirationTime,
    )

    return Token(access_token=access_token, token_type="bearer")
