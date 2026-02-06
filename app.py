from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import board

app = FastAPI(title="Améliorations")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(board.router)
