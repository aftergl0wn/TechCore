import logging
import time

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_redoc_html

from app.routers.book import router


app = FastAPI(redoc_url=None)
app.include_router(router)

logging.basicConfig(level=logging.INFO)


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )


@app.middleware("http")
async def log_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    logging.info(
        f"Время выполнения {request.method} {request.url.path} составило {time.time()-start}"
    )
    return response
