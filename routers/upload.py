from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import aiofiles
import logging
from utils.file_utils import (
    MAX_FILE_SIZE, check_file_size,
    is_allowed_file, ensure_enough_disk_space,
    get_unique_name, IMAGES_DIR
)

router = APIRouter(prefix="/upload", tags=["upload"])
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger("app")

@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Страница загрузки",
    description="Форма для загрузки изображения"
)
async def upload_page(request: Request, new_file_url: str = None):
    logger.info("Успех: открыта страница загрузки")
    return templates.TemplateResponse(request,
        "upload.html",
        {"request": request,
        "message": "Файл успешно загружен!" if new_file_url else "",
        "current_upload_url": new_file_url or ""
    })

@router.post(
    "/",
    response_class=HTMLResponse,
    summary="Загрузить изображение",
    description="Принимает JPG, JPEG, PNG или GIF до 5 МБ, сохраняет под уникальным именем и возвращает ссылку.",
    responses={
    400: {"description": "Неверный файл (формат или размер)"},
    507: {"description": "Недостаточно места на диске"}
}
)
async def upload_img(request: Request, file: UploadFile = File(...)):
    logger.info(f"Новая попытка загрузки: {file.filename}")
    content = await file.read(MAX_FILE_SIZE + 1)
    try:
        check_file_size(content)
        is_allowed_file(file.filename)
        ensure_enough_disk_space(IMAGES_DIR)
    except HTTPException as ex:
        logger.error(f"Ошибка валидации {file.filename}: {ex.detail}")
        raise

    new_name = get_unique_name(Path(file.filename))
    save_path = IMAGES_DIR / new_name
    async with aiofiles.open(save_path, "wb") as f:
        await f.write(content)

    new_url = f"/images/{new_name}"
    logger.info(f"Успех: {file.filename} → {new_name}")
    return templates.TemplateResponse(request,
        "upload.html",
        {"request": request,
        "message": "Файл успешно загружен!",
        "current_upload_url": new_url
    })