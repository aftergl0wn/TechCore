import logging
import time

from fastapi import FastAPI, Request

from app.routers.book import router


app = FastAPI()
app.include_router(router)


@app.middleware("http")
async def log_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    logging.info(
        f"Время выполнения {request.method} составило {time.time()-start}"
    )
    return response
