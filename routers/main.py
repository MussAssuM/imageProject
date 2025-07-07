from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging

router = APIRouter(tags=["main"])
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger("app")

@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Главная страница",
    description="Отображает форму для загрузки изображения."
)
async def index(request: Request):
    """
    Рендерит index.html с формой загрузки.
    """
    logger.info("Успех: открыта главная страница")
    return templates.TemplateResponse(request,
        "index.html", {"request": request})
