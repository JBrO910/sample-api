from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.health import router as health_router
from app.core.database import Base, engine
from app.core.models import Task

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Run startup logic here
    Base.metadata.create_all(bind=engine)
    yield
    # Run shutdown logic here if needed


app = FastAPI(title="HR-ON Backend Task", lifespan=lifespan)
app.include_router(health_router)