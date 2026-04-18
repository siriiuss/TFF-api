from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

# This ensures the cache is ready as soon as the app starts
@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

app.include_router(api_router, prefix="/api", tags=["Super League"])

@app.get("/", tags=["General"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "Online",
        "docs": "/docs",
        "message": "For scores: /api/standings",
    }