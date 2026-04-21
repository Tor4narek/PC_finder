from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.config import CATEGORY_CODES
from app.database import Base


class Computer(Base):
    __tablename__ = "computers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    cpu: Mapped[str] = mapped_column(String(120), nullable=False)
    gpu: Mapped[str | None] = mapped_column(String(120), nullable=True)
    ram_gb: Mapped[int] = mapped_column(Integer, nullable=False)
    ssd_gb: Mapped[int] = mapped_column(Integer, nullable=False)
    has_windows: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    shop_name: Mapped[str] = mapped_column(String(120), nullable=False)
    shop_url: Mapped[str] = mapped_column(String(500), nullable=False)
    category_code: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def validate_category(self):
        if self.category_code not in CATEGORY_CODES:
            raise ValueError("Invalid category code")
