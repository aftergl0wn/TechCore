from fastapi import FastAPI

from app.router import router_review

app = FastAPI()

app.include_router(router_review)
