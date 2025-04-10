from fastapi import FastAPI

from app.exceptions import map_exceptions
from app.infrastructure.api.router import router

app = FastAPI()
map_exceptions(app)
app.include_router(router)
