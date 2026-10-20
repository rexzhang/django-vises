import os
import urllib.parse
from logging import getLogger
from typing import Any

import logfire
from asgiref.typing import (
    ASGI3Application,
    ASGIReceiveCallable,
    ASGISendCallable,
    ASGISendEvent,
    HTTPScope,
    Scope,
)


class ASGIMiddlewareAccessLogging:
    logfire: bool = False

    def __init__(
        self, app: ASGI3Application, remote_addr_header_name: str = "X-Forwarded-For"
    ) -> None:
        self.logger = getLogger("ASGI")
        self.app = app
        # X-Forwarded-For/X-Real-IP
        self.remote_addr_header_name = remote_addr_header_name.lower().encode("latin1")

        # init logfire
        logfire_token = os.getenv("LOGFIRE_TOKEN")
        if logfire_token:
            logfire.configure(token=logfire_token)
            self.logfire = True

    async def __call__(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        data: dict[str, Any] = dict()
        data["response"] = {"status": 500}

        async def inner_send(message: ASGISendEvent) -> None:
            if message["type"] == "http.response.start":
                data["response"] = message
            await send(message)

        try:
            # info["start_time"] = time.time()
            await self.app(scope, receive, inner_send)
        except Exception as e:
            # info["response"]["status"] = 500

            raise e
        finally:
            # info["end_time"] = time.time()
            pass

        if scope["type"] != "http":
            return

        headers = dict(scope["headers"])

        remote_addr = self._get_remote_addr(scope, headers)
        user_agent = headers.get(b"user-agent", b"").decode("utf-8")

        request_method = scope.get("method")
        request_path = scope["path"]
        request_query_string = scope.get("query_string")
        if request_query_string:
            request_path += urllib.parse.unquote_to_bytes(request_query_string).decode(
                "utf-8", "replace"
            )

        status_code = data["response"].get("status")

        self.logger.info(
            f'{remote_addr} - "{request_method} {request_path}" {status_code}'
        )

        if self.logfire:
            logfire.info(
                f"{remote_addr} {request_method} {request_path}",
                remote_addr=remote_addr,
                request_method=request_method,
                request_path=request_path,
                status_code=status_code,
                user_agent=user_agent,
            )

    def _get_remote_addr(self, scope: HTTPScope, headers: dict[bytes, bytes]) -> str:
        remote_addr = headers.get(self.remote_addr_header_name, b"").decode("latin1")

        if remote_addr:
            return remote_addr

        client = scope.get("client")
        if client:
            return f"{client[0]}:{client[1]}"

        return "-"
