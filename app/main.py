from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routers import board

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(title="Améliorations")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(board.router)
