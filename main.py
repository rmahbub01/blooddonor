import asyncio
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from blooddonor.api.api_v1.api import api_router
from blooddonor.core.config import settings
from blooddonor.db.session import SessionLocal
from blooddonor.helper.scheduler import update_donor_availability

DOCS_URL = settings.DOCS_URL if settings.DOCS_URL == "/docs" else None
REDOC_URL = settings.REDOC_URL if settings.REDOC_URL == "/redoc" else None

scheduler = BackgroundScheduler()


def scheduled_tasks():
    db = SessionLocal()
    asyncio.run(update_donor_availability(db))


scheduler.add_job(scheduled_tasks, trigger="interval", hours=3)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={"persistAuthorization": True},
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
    lifespan=lifespan,
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
