from fastapi import FastAPI

from app.routers.book import router

app = FastAPI()
app.include_router(router)
