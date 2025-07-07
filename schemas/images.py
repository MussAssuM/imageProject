from pydantic import BaseModel


class ImageInfo(BaseModel):
    """
    Описание одной записи изображения.
    """
    filename: str
    url: str


class ImageListResponse(BaseModel):
    """
    Ответ списка изображений.
    """
    images: list[ImageInfo]