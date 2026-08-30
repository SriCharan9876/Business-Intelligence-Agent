from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.config import settings
from app.api.chat import router as chat_router


app = FastAPI(
    title="Skylark Drones BI Agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        settings.FRONTEND_URL
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(
    chat_router
)


@app.get("/")
def health_check():

    return {
        "status": "healthy",
        "service":
            "Skylark Drones BI Agent"
    }