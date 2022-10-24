import logging
from fastapi import FastAPI
from route_error_handler import RouteErrorHandler
from logging_middleware import LoggingMiddleware
from starlette_context.middleware import RawContextMiddleware
from pydantic import BaseModel

from fastapi.exceptions import HTTPException

logging.basicConfig(level=logging.INFO)

app = FastAPI(debug=True)

app.router.route_class = RouteErrorHandler

app.add_middleware(LoggingMiddleware)
app.add_middleware(RawContextMiddleware)


@app.get("/")
async def get():
    raise HTTPException(status_code=422)


class Body(BaseModel):
    value: int


@app.post("/")
async def post(body: Body):
    return body
