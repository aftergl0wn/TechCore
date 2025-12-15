from http import HTTPStatus

from fastapi import FastAPI

from service import WorkerService

app = FastAPI()


@app.post("/order", status_code=HTTPStatus.ACCEPTED)
def post_order(order_id: int):
    result = WorkerService.process_order.delay(order_id)
    result = result.get()
    return {"message": result}
