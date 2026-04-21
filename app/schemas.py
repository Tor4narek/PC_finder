from pydantic import BaseModel, Field, HttpUrl

from app.config import CATEGORY_CODES


class ClassifyRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)


class ClassifyResponse(BaseModel):
    category: str
    scores: dict[str, float]


class ComputerBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=5)
    price: float = Field(gt=0)
    cpu: str = Field(min_length=2, max_length=120)
    gpu: str | None = Field(default=None, max_length=120)
    ram_gb: int = Field(gt=0, le=1024)
    ssd_gb: int = Field(gt=0, le=8192)
    has_windows: bool = True
    image_url: HttpUrl
    shop_name: str = Field(min_length=2, max_length=120)
    shop_url: HttpUrl
    category_code: str
    is_active: bool = True


class ComputerCreate(ComputerBase):
    pass


class ComputerUpdate(ComputerBase):
    pass


class ComputerOut(ComputerBase):
    id: int

    class Config:
        from_attributes = True


class AdminComputerForm(BaseModel):
    name: str
    description: str
    price: float
    cpu: str
    gpu: str | None = None
    ram_gb: int
    ssd_gb: int
    has_windows: bool = True
    image_url: str
    shop_name: str
    shop_url: str
    category_code: str
    is_active: bool = True

    @classmethod
    def allowed_categories(cls) -> list[str]:
        return CATEGORY_CODES
