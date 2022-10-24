
from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute
from logger import log, log_exception


class RouteErrorHandler(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as ex:
                log_exception(ex)
                await self.log_body(request)
                
                if isinstance(ex, HTTPException):
                    raise ex

                raise HTTPException(status_code=500, detail=str(ex))

        return custom_route_handler

    async def log_body(self, request: Request):
        body = await request.body()

        if not body:
            return

        if "content-type" in request.headers and "json" in request.headers["content-type"]:
            log("request_body", await request.json())
        else:
            log("request_body", str(await request.body()))
