from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routes import *
from core.logger import setup_logger
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = setup_logger("Listify")
    logger.debug("Starting Listify application...")

    yield

    logger.debug("Shutting down Listify application...")


app = FastAPI(
    title="Listify",
    version="1.0.0",
    lifespan=lifespan,
)


origins = ["http://localhost", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(
    queue_management_router, prefix="/api/queue", tags=["Queue Management"]
)
app.include_router(
    fetch_management_router, prefix="/api/content", tags=["Content Management"]
)
