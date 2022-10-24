import json
import logging
import time
import traceback

from typing import Awaitable
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette_context import context


class LoggingMiddleware(BaseHTTPMiddleware):
    _logger: logging.Logger = logging.getLogger("middleware")
    _headers_not_to_log = set(["Authorization", "X-Api-Key"])

    async def dispatch(self, request: Request, call_next: Awaitable[Response]) -> Response:
        start = time.perf_counter()
        response: Response = None
        exception: Exception = None

        try:
            response: Response = await call_next(request)
        except Exception as exception:
            response = exception if isinstance(exception, HTTPException) else Response(status_code=500)
            raise exception
        finally:
            duration = time.perf_counter() - start
            self.log_request(request, response, duration, exception)

        return response

    def log_request(self, request, response, duration, exception):
        log = json.dumps(self.build_log(request, response, duration, exception), indent=4)

        if response.status_code < 400:
            self._logger.info(log)
        elif response.status_code < 500:
            self._logger.warn(log)
        else:
            self._logger.error(log)

    def build_log(self, request: Request, response, duration, exception):
        log = {
            "duration": duration,
            "status_code": response.status_code,
        }
        
        if "diagnostics" in context.data:
            log = log | context.data["diagnostics"]

        self._add_request_to_log(log, request)
        self._add_exception_to_log(log, exception)

        return log

    def _add_request_to_log(self, log: dict, request: Request):
        log["client"] = request.client.host
        log["host"] = str(request.base_url)
        log["scheme"] = request.url.scheme
        log["path"] = request.url.path
        log["method"] = request.method

        log["headers"] = {
            header: value
            for (header, value) in request.headers.items()
            if header not in self._headers_not_to_log
        }

        if request.url.query:
            log["query"] = request.url.query

    def _add_exception_to_log(self, log: dict, exception: Exception):
        if not exception:
            return

        error_dict = vars(exception)

        message = str(exception)
        if message:
            error_dict["message"] = message

        error_dict["traceback"] = traceback.format_exc()
        log["error"] = error_dict
