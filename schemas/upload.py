from pydantic import BaseModel

class UploadResponse(BaseModel):
    """
    Ответ при успешной загрузке.
    """
    filename: str
    url: str