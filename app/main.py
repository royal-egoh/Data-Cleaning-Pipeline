from app.models import user, dataset
from app.database import create_tables
from fastapi import FastAPI
from app.routers import user, pipeline
create_tables()

app = FastAPI()

app.include_router(user.router)
app.include_router(pipeline.router)