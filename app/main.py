from app.api.router import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
