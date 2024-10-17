import asyncio
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = []
    for error in errors:
        formatted_errors.append(
            {
                "field": error["loc"][-1],
                "message": error.get("msg"),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": formatted_errors},
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    errors = exc.errors()
    formatted_errors = []
    for error in errors:
        formatted_errors.append(
            {
                "field": error["loc"][-1],
                "message": error.get("msg"),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": formatted_errors},
    )


app.mount("/static", StaticFiles(directory="./blooddonor/static"), name="static")
# Set all CORS enabled origins
# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
