# -*- coding: utf-8 -*-
"""
kiwoom.client
~~~~~~~~~~~~~

This module implements the Kiwoom API client.
"""

import os
from typing import Optional

import httpx
from dotenv import load_dotenv

from .core import AuthenticatedKiwoomBaseClient
from .exceptions import AuthenticationError
from .models import AuthResponse
from .stock_information.client import StockInformationClient


class KiwoomClient(AuthenticatedKiwoomBaseClient):
    """
    The main client for interacting with the Kiwoom API.
    """

    def __init__(
        self,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        api_server_type: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        load_dotenv()  # Load environment variables from .env file

        self.app_key = app_key or os.getenv("KIWOOM_APP_KEY")
        self.app_secret = app_secret or os.getenv("KIWOOM_SECRET_KEY")
        self.api_server_type = api_server_type or os.getenv("KIWOOM_API_SERVER_TYPE", "real")

        if not self.app_key or not self.app_secret:
            raise ValueError(
                "KIWOOM_APP_KEY and KIWOOM_SECRET_KEY must be provided either as arguments or in the .env file."
            )

        if self.api_server_type == "real":
            base_url = "https://api.kiwoom.com"
            websocket_url = "wss://api.kiwoom.com:10000"
        elif self.api_server_type == "mock":
            base_url = "https://mockapi.kiwoom.com"  # Example mock URL
            websocket_url = "wss://mock-api.kiwoom.com:10000" # Example mock URL
        else:
            raise ValueError(
                "KIWOOM_API_SERVER_TYPE must be 'real' or 'mock'."
            )

        self._client = httpx.AsyncClient()
        super().__init__(
            base_url=base_url,
            client=self._client,
            websocket_url=websocket_url,
            access_token=access_token,
        )
        self.stock_information = StockInformationClient(client=self)

    async def fetch_access_token(self):
        """
        Fetches and sets the access token.
        """
        token_path = "/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.app_secret,
        }

        auth_response = await self._post(
            token_path, response_model=AuthResponse, json=data
        )
        if auth_response.return_code == 0 and auth_response.token:
            self.access_token = auth_response.token
        else:
            error_message = f"Failed to fetch access token. Response: {auth_response.message}"
            raise AuthenticationError(error_message)

async def main():
    """
    Main function to demonstrate authentication and API call.
    """
    try:
        async with KiwoomClient() as client:
            print("Fetching access token...")
            await client.fetch_access_token()
            print("Access token fetched successfully.")

            samsung_stock_code = "005930"  # Samsung Electronics stock code
            print(f"Requesting basic stock info for {samsung_stock_code} (Samsung Electronics)...")
            stock_info_response = await client.stock_information.get_stock_basic_info(samsung_stock_code)

            print("Stock Information:")
            print(f"  Stock Name: {stock_info_response.stock_name}")
            print(f"  Stock Code: {stock_info_response.stock_code}")
            print(f"  Market Type: {stock_info_response.market_type}")
            print(f"  Current Price (prpr): {stock_info_response.present_price}")

    except AuthenticationError as e:
        print(f"Authentication Error: {e}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {type(e).__name__}: {e}")


if __name__ == "__main__":
    import asyncio
    import sys
    import os

    # Add the parent directory to the Python path to allow package-relative imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    asyncio.run(main())
