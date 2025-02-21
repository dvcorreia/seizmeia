from __future__ import annotations

from typing import Sequence

import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from seizmeia.db import Base, engine
from seizmeia.healthcheck.asynchronous import AsyncHealthcheck
from seizmeia.healthcheck.fastapi import add_healthcheck_handlers
from seizmeia.settings import Settings
from seizmeia.token.route import router as token_router
from seizmeia.user.routes import router as user_router
from seizmeia.version import get_version
from seizmeia.version import router as version_router

config = Settings()

app = FastAPI(
    title="Seizmeia 🍺",
    description="A credit management tool for a beer tap.",
    version=get_version(),
    debug=True,
)

origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

healthchecker = AsyncHealthcheck()
add_healthcheck_handlers(app, healthchecker, tags=["telemetry"])

app.include_router(user_router)
app.include_router(token_router)
app.include_router(version_router)


def main(argv: Sequence[str] | None = None) -> int:
    uvicorn.run(
        "seizmeia._main:app",
        port=config.uvicorn.port,
        host=str(config.uvicorn.host),
        workers=config.uvicorn.workers,
        reload=config.environment.is_dev(),
        loop="asyncio",
    )
    return 0


if __name__ == "__main__":
    main()
