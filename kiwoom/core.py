# -*- coding: utf-8 -*-
"""
kiwoom.core
~~~~~~~~~~~

This module provides the core functionality for interacting with the Kiwoom API.
"""

import asyncio
from typing import Any, AsyncGenerator, Callable, Coroutine, Dict, Optional, Type, TypeVar

import httpx
import websockets
from pydantic import ValidationError

from .exceptions import KiwoomAPIError, WebSocketError
from .models import BaseKiwoomResponse, PaginatedResponse # Changed APIResponse to BaseKiwoomResponse

T = TypeVar("T")


class KiwoomBaseClient:
    """
    A base client providing low-level methods for interacting with the Kiwoom API.
    """

    def __init__(
        self,
        base_url: str,
        client: httpx.AsyncClient,
        websocket_url: str,
    ):
        self.base_url = base_url
        self._client = client
        self.websocket_url = websocket_url

    async def _request(
        self,
        method: str,
        path: str,
        response_model: Type[T],
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> T:
        """
        Sends an HTTP request and processes the response.
        """
        url = f"{self.base_url}{path}"
        try:
            response = await self._client.request(
                method, url, params=params, data=data, json=json, headers=headers
            )
            response.raise_for_status()
            json_data = response.json()
            # print(f"API Response JSON: {json_data}") # Debugging line removed
            # print(f"API Response Status Code: {response.status_code}") # Debugging line removed

            # API 에러 응답 처리
            if json_data.get("return_code") != 0:
                raise KiwoomAPIError(
                    response=response,
                    error_code=json_data.get("return_code"),
                    error_message=json_data.get("return_msg"),
                )

            return response_model.model_validate(json_data)
        except httpx.HTTPStatusError as e:
            # print(f"HTTP Status Error: {e.response.status_code} - {e.response.text}") # Debugging line removed
            raise KiwoomAPIError(response=e.response) from e
        except ValidationError as e:
            # print(f"Pydantic Validation Error: {e}") # Debugging line removed
            raise KiwoomAPIError(response=response, error_message=str(e)) from e
        except Exception as e:
            # print(f"An unexpected error occurred in _request: {type(e).__name__}: {e}") # Debugging line removed
            raise KiwoomAPIError(response=response, error_message=str(e)) from e

    async def _get(
        self,
        path: str,
        response_model: Type[T],
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> T:
        return await self._request(
            "GET", path, response_model, params=params, headers=headers
        )

    async def _post(
        self,
        path: str,
        response_model: Type[T],
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> T:
        return await self._request(
            "POST", path, response_model, data=data, json=json, headers=headers
        )

    async def _paginated_request(
        self,
        path: str,
        response_model: Type[PaginatedResponse[T]],
        params: Dict[str, Any],
    ) -> AsyncGenerator[T, None]:
        """
        Handles paginated API requests, yielding items one by one.
        """
        while True:
            response = await self._get(path, response_model, params=params)
            if response.data:
                for item in response.data:
                    yield item

            if response.pagination and response.pagination.next_page:
                # 다음 페이지를 위한 파라미터 업데이트
                params["CTX_AREA_FK"] = response.pagination.context
                params["CTX_AREA_NK"] = response.pagination.next_page
            else:
                break

    async def _ws_connect(
        self,
        handler: Callable[[Dict[str, Any]], Coroutine[Any, Any, None]],
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Connects to a WebSocket and handles incoming messages.
        """
        try:
            async with websockets.connect(
                self.websocket_url, extra_headers=headers
            ) as ws:
                while True:
                    try:
                        message = await ws.recv()
                        await handler(message)
                    except websockets.ConnectionClosed:
                        # 재연결 로직 추가 가능
                        raise WebSocketError("Connection closed.")
        except Exception as e:
            raise WebSocketError(f"WebSocket connection failed: {e}") from e
