from fastapi import FastAPI

from app.routers.router_book import router
from app.routers.router_review import router_review
from app.routers.route_review_book import router_review_book

app = FastAPI()

app.include_router(router_review)
app.include_router(router)
app.include_router(router_review_book)
