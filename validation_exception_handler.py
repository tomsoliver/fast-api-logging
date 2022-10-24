from pydantic import ValidationError
from starlette.requests import Request
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from logger import log


def setup_exception_handlers(app: FastAPI):
    app.exception_handler(ValidationError)(validation_exception_handler)
    app.exception_handler(Exception)(validation_exception_handler)


async def validation_exception_handler(request: Request, exc: ValidationError):
    log("error", exc)

    body = await request.body()

    if body:
        if "content-type" in request.headers and "json" in request.headers["content-type"]:
            log("request_body", await request.json())

        log("request_body", str(await request.body()))

    return JSONResponse(exc.json(), status_code=422)
