from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers import admin, api, web
from app.seed import seed_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
    yield


app = FastAPI(title="PC Finder Mini App", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(web.router)
app.include_router(api.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})
