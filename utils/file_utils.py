import shutil
import uuid
from PIL import Image
from pathlib import Path
from fastapi import HTTPException

# ─── КОНСТАНТЫ ────────────────────────────────────────────────────────────────
ALLOW_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
MAX_FILE_SIZE     = 5 * 1024 * 1024
MIN_FREE_SPACE    = MAX_FILE_SIZE
IMAGES_DIR = Path("images")

# ─── ПРОВЕРКИ ────────────────────────────────────────────────────────────────
def ensure_enough_disk_space(directory: Path):
    total, used, free = shutil.disk_usage(directory)
    if free < MIN_FREE_SPACE:
        raise HTTPException(507, "Недостаточно места на диске.")

def check_file_size(content: bytes):
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "Файл слишком большой.")

def is_allowed_file(filename: str):
    if Path(filename).suffix.lower() not in ALLOW_EXTENSIONS:
        raise HTTPException(400, "Неподдерживаемый формат.")

# ─── УТИЛИТЫ ────────────────────────────────────────────────────────────────
def get_unique_name(filename: Path) -> str:
    return f"{uuid.uuid4().hex}{filename.suffix.lower()}"