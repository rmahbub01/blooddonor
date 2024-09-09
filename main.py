from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from blooddonor.api.api_v1.api import api_router
from blooddonor.core.config import settings

DOCS_URL = settings.DOCS_URL if settings.DOCS_URL == "/docs" else None
REDOC_URL = settings.REDOC_URL if settings.REDOC_URL == "/redoc" else None

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={"persistAuthorization": True},
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
)

app.mount("/static", StaticFiles(directory="./blooddonor/static"), name="static")
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
