
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from fastapi.exceptions import HTTPException
from logger import log


class RouteErrorHandler(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                response = await original_route_handler(request)

                if response.status_code >= 500:
                    await self.log_body(request)

            except Exception as ex:
                if not isinstance(ex, HTTPException) or ex.status_code > 500:
                    await self.log_body(request)
                raise

        return custom_route_handler

    async def log_body(self, request: Request):
        body = await request.body()

        if not body:
            return

        if "content-type" in request.headers and "json" in request.headers["content-type"]:
            log("request_body", await request.json())
        else:
            log("request_body", str(await request.body()))
