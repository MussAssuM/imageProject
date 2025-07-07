import pytest
import shutil

from pathlib import Path
from fastapi import HTTPException

import utils.file_utils as fu

# 1) Тест проверки размера файла.
def test_check_file_size_within_limit():
    data = b"x" * fu.MAX_FILE_SIZE
    fu.check_file_size(data)

def test_check_file_size_exceeds_limit():
    data = b"x" * (fu.MAX_FILE_SIZE + 1)
    with pytest.raises(HTTPException) as exc:
        fu.check_file_size(data)
    assert exc.value.status_code == 400
    assert "слишком большой" in exc.value.detail.lower()

#  2)Тест проверки формата файла.
@pytest.mark.parametrize("name", [
    "a.jpg", "b.JPEG", "c.png", "d.GiF",
])
def test_is_allowed_file_valid(name):
    fu.is_allowed_file(name)

@pytest.mark.parametrize("name", [
    "a.txt", "b.bmp", "c.pdf", "noext"
])
def test_is_allowed_file_invalid(name):
    with pytest.raises(HTTPException) as exc:
        fu.is_allowed_file(name)
    assert exc.value.status_code == 400
    assert "неподдерживаемый формат" in exc.value.detail.lower()

#  3) Тест проверки места на диске.
class DummyUsage:
    def __init__(self, total, used, free):
        self.total =total
        self.used = used
        self.free = free

def test_ensure_enough_disk_space_ok(monkeypatch, tmp_path):
    monkeypatch.setattr(shutil, "disk_usage", lambda p: (0, 0, fu.MIN_FREE_SPACE))
    fu.ensure_enough_disk_space(tmp_path)

def test_ensure_enough_disk_space_not_enough(monkeypatch, tmp_path):
    monkeypatch.setattr(shutil, "disk_usage", lambda p: (0, 0, fu.MIN_FREE_SPACE - 1))
    with pytest.raises(HTTPException) as exc:
        fu.ensure_enough_disk_space(tmp_path)
    assert exc.value.status_code == 507
    assert "места" in exc.value.detail.lower()

# 4) Тест присваивания уникального имени
def test_get_unique_name_suffix_preserved():
    p = Path("photo.PNG")
    name = fu.get_unique_name(p)
    assert len(name) == 32 + len(p.suffix)
    assert name.endswith(".png")
    uuid_part = name[:-len(p.suffix)]
    int(uuid_part, 16)