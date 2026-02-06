from fastapi import FastAPI
from app.routes import router
from app.database import engine, Base

app = FastAPI(title="Python API with uv & PostgreSQL")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router)
