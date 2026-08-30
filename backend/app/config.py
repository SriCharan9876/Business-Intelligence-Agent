import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    MONDAY_API_TOKEN = os.getenv(
        "MONDAY_API_TOKEN"
    )

    DEALS_BOARD_ID = os.getenv(
        "DEALS_BOARD_ID"
    )

    WORK_ORDERS_BOARD_ID = os.getenv(
        "WORK_ORDERS_BOARD_ID"
    )

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173"
    )


settings = Settings()