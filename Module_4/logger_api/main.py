import structlog
import time

from fastapi import FastAPI, Request

from app.routers.book import router


app = FastAPI()
app.include_router(router)

logger = structlog.get_logger()


@app.middleware("http")
async def log_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    logger.info(
        "Запрос выполнен",
        method=request.method,
        url=str(request.url),
        time_delta=time.time()-start
    )
    return response
