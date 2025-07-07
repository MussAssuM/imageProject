from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
import logging
from utils.file_utils import IMAGES_DIR

router = APIRouter(prefix="/images", tags=["images"])
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger("app")

@router.get(
    "/",
    summary="Список изображений",
    description="Показывает ваши загруженные изображения с их URL."
)
async def images_page(request: Request):
    logger.info("Успех: открыта страница сохранённых изображений")
    all_files = sorted(
        IMAGES_DIR.glob("*.*"),
        key = lambda fp: fp.stat().st_mtime,
        reverse = True
    )
    files_ctx = [
        {
            "name": file_path.name,
            "url": f"/images/{file_path.name}",
            "uploaded_at": int(file_path.stat().st_mtime)
        }
         for file_path in all_files
    ]

    return templates.TemplateResponse(
            "images.html",
            {"request": request, "image_files": files_ctx}
    )

@router.delete(
    "/delete/{filename}",
    summary="Удалить изображение",
    description="Удаляет указанный файл из хранилища.",
    responses={404: {"description": "Файл не найден"}}
)
async def delete_image(filename: str):
    target = IMAGES_DIR / filename
    if not target.exists():
        logger.error(f"Попытка удалить несуществующий файл {filename}")
        raise HTTPException(404, f"Ошибка: файл {filename} не найден")

    try:
        target.unlink()
        logger.info(f"Успех: Удалён файл {filename}")
    except Exception as e:
        logger.error(f"Ошибка при удалении {filename}: {e}")
        raise HTTPException(500, "Ошибка удаления")

    return {"success": True, "deleted": filename}
