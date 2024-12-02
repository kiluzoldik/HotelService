from typing import Annotated
from fastapi import FastAPI, Form
import uvicorn

from routers import router as router_hotels


app = FastAPI()


app.include_router(router_hotels)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)