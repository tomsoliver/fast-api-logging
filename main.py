import logging
import requests
from fastapi import FastAPI
from route_error_handler import RouteErrorHandler
from validation_exception_handler import setup_exception_handlers
from logging_middleware import LoggingMiddleware
from starlette_context.middleware import RawContextMiddleware
from pydantic import BaseModel

from fastapi.exceptions import HTTPException

logging.basicConfig(level=logging.INFO)

app = FastAPI(debug=True)

app.router.route_class = RouteErrorHandler

app.add_middleware(LoggingMiddleware)
app.add_middleware(RawContextMiddleware)

setup_exception_handlers(app)

@app.get("/")
async def get():
    raise HTTPException(status_code=500)


class Body(BaseModel):
    value: int


@app.post("/")
async def post(body: Body):
    return body
