from fastapi import FastAPI

app = FastAPI(title="Gateway")


@app.get("/")
async def gateway_get():
    return {"status": "Hello"}
