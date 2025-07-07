import os
import time
import logging
import uvicorn
from logging.handlers import RotatingFileHandler
from pathlib import Path
from tzlocal import get_localzone

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# роутеры
from routers.main import router as main_router
from routers.upload import router as upload_router
from routers.images import router as images_router

# ─── Настройка ТаймЗоны ──────────────────────────────────────────────────────────
os.environ.setdefault("TZDIR", "/usr/share/zoneinfo")
os.environ.setdefault("TZ", os.getenv("TZ", "Asia/Atyrau"))
if hasattr(time, "tzset"):
    time.tzset()
local_tz = get_localzone()

# ─── Логирование ──────────────────────────────────────────────────────────
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / "app.log"

handler = RotatingFileHandler(
    filename=LOG_FILE,
    mode="a",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s: %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info(f"Таймзона сервиса: {local_tz}")

# ─── FastAPI и монтирование статики ────────────────────────────────────────
app = FastAPI(
    title="Image Server",
    version="1.0.0",
    description="Сервис для загрузки, просмотра и удаления изображений",
    contact={
        "name": "Mussa",
        "email": "12345678assumussa@gmail.com",
    },
    license_info={"name": "MIT"},
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Статика для CSS/JS картинок
app.mount("/static", StaticFiles(directory="static"), name="static")
# ─── Подключаем роутеры ────────────────────────────────────────────────────
app.include_router(upload_router)
app.include_router(images_router)
app.include_router(main_router)

# ─── Run ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)