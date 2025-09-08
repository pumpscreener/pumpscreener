from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from .api import router as api_router
from .indexer import init_db, run_forever

app = FastAPI(title="PumpDex")
app.include_router(api_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def _startup():
    init_db()
    asyncio.create_task(run_forever())

@app.get("/", response_class=HTMLResponse)
def home(req: Request):
    return templates.TemplateResponse("pairs.html", {"request": req})

@app.get("/pairs/{pool_id}", response_class=HTMLResponse)
def pair_detail(req: Request, pool_id: int):
    return templates.TemplateResponse("trades.html", {"request": req, "pool_id": pool_id})
