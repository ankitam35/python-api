from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import router

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Python API",
    description="A FastAPI application",
    version="1.0.0"
)

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Python API"}
