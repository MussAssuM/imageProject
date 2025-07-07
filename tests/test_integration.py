import io, shutil, pytest, logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from fastapi.testclient import TestClient

from app import app, logger  # Захватываем ваш настроенный логгер

client = TestClient(app)

@pytest.fixture(autouse=True)
def isolate_fs(tmp_path, monkeypatch):
    project_root = Path(__file__).resolve().parent.parent

    # переходим в tmp_path
    monkeypatch.chdir(tmp_path)
    (tmp_path / "images").mkdir()
    (tmp_path / "logs").mkdir()

    # копируем шаблоны
    shutil.copytree(project_root / "templates", tmp_path / "templates")

    # ——— ПЕРЕНАСТРОЙКА ЛОГГЕРА ———
    # Убираем старые хэндлеры
    for h in logger.handlers[:]:
        logger.removeHandler(h)

    # Добавляем новый, который будет писать в tmp_path/logs/app.log
    fh = RotatingFileHandler(
        filename=tmp_path / "logs" / "app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    # ——————————————————————————————

    yield

def test_upload_and_list_and_delete():
    # 1) Загрузка валидного файла
    small_png = b"\x89PNG\r\n\x1a\n" + b"x" * 100
    resp1 = client.post(
        "/upload/",
        files={"file": ("test.png", io.BytesIO(small_png), "image/png")}
    )
    assert resp1.status_code == 200

    # 2) Файл появился
    imgs = list(Path("images").glob("*.png"))
    assert len(imgs) == 1
    saved_name = imgs[0].name

    # 3) Листинг
    resp2 = client.get("/images/")
    assert resp2.status_code == 200
    assert saved_name in resp2.text

    # 4) Удаление
    resp3 = client.delete(f"/images/delete/{saved_name}")
    assert resp3.status_code == 200
    assert not (Path("images") / saved_name).exists()

    # 5) Логи
    log_text = (Path("logs") / "app.log").read_text(encoding="utf-8")
    assert "Новая попытка загрузки: test.png" in log_text
    assert f"Успех: test.png → {saved_name}" in log_text
    assert f"Успех: Удалён файл {saved_name}" in log_text

def test_upload_bad_format_and_size():
    # Неподдерживаемый формат
    bad = client.post(
        "/upload/",
        files={"file": ("test.txt", io.BytesIO(b"abc"), "text/plain")}
    )
    assert bad.status_code == 400

    # Слишком большой файл
    huge = client.post(
        "/upload/",
        files={"file": ("big.png", io.BytesIO(b"x" * (5*1024*1024 + 1)), "image/png")}
    )
    assert huge.status_code == 400
