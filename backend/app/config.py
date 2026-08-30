from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MONDAY_API_TOKEN: str

    DEALS_BOARD_ID: str

    WORK_ORDERS_BOARD_ID: str

    GEMINI_API_KEY: str

    FRONTEND_URL: str = (
        "http://localhost:5173"
    )

    class Config:

        env_file = ".env"


settings = Settings()