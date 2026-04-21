from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="production", alias="APP_ENV")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    admin_password: str = Field(default="admin123", alias="ADMIN_PASSWORD")
    database_url: str = Field(default="sqlite:////data/app.db", alias="DATABASE_URL")
    huggingface_api_key: str = Field(default="", alias="HUGGINGFACE_API_KEY")
    hf_model: str = Field(default="facebook/bart-large-mnli", alias="HF_MODEL")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

CATEGORY_LABELS = {
    "office": "Office",
    "study": "Study",
    "programming": "Programming",
    "gaming": "Gaming",
    "video_editing": "Video Editing",
    "design_3d": "3D Design",
}

CATEGORY_CODES = list(CATEGORY_LABELS.keys())
