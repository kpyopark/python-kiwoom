# -*- coding: utf-8 -*-
"""
kiwoom.stock_information.client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the Kiwoom stock information API client.
"""

from typing import Optional

from ..core import KiwoomBaseClient
from ..exceptions import KiwoomAPIError
from .models import StockInfo

class StockInformationClient:
    """
    Client for Kiwoom stock information API.
    """

    def __init__(self, core_client: KiwoomBaseClient, access_token: str):
        self.core = core_client
        self._access_token = access_token

    @property
    def _auth_headers(self) -> dict:
        if not self._access_token:
            raise KiwoomAPIError("Access token is not set.")
        return {
            "authorization": f"Bearer {self._access_token}",
        }

    async def get_stock_basic_info(self, stock_code: str) -> StockInfo:
        """
        주식기본정보요청 (ka10001)

        Args:
            stock_code (str): 종목코드 (예: "005930" for 삼성전자)

        Returns:
            StockInfo: 주식기본정보 응답 모델

        Raises:
            KiwoomAPIError: API 호출 실패 시 발생
        """
        path = "/api/dostk/stkinfo"
        headers = {**self._auth_headers, "api-id": "ka10001"}
        data = {"stk_cd": stock_code}
        
        response = await self.core._post(
            path, response_model=StockInfo, headers=headers, json=data
        )

        if response.return_code != 0:
            raise KiwoomAPIError(
                f"API Error (ka10001): {response.message} (Code: {response.return_code})"
            )
        return response
