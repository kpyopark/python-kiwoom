# -*- coding: utf-8 -*-
"""
tests.stock_information.test_client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains unit tests for the Kiwoom stock information API client.
"""

import pytest
import httpx
from httpx import Response
from pytest_mock import MockerFixture

from kiwoom.client import KiwoomClient
from kiwoom.exceptions import KiwoomAPIError
from kiwoom.stock_information.client import StockInformationClient
from kiwoom.stock_information.models import StockInfo

@pytest.fixture
def mock_kiwoom_client(mocker: MockerFixture):
    """Fixture to mock KiwoomClient."""
    mock_client = mocker.MagicMock(spec=KiwoomClient)
    mock_client.access_token = "test_token" # Set a dummy access token for _auth_headers
    return mock_client

@pytest.fixture
def stock_info_client(mock_kiwoom_client: KiwoomClient):
    """Fixture to create a StockInformationClient instance."""
    return StockInformationClient(client=mock_kiwoom_client)

@pytest.mark.asyncio
async def test_get_stock_basic_info_success(stock_info_client: StockInformationClient, mock_kiwoom_client: KiwoomClient):
    """
    Test get_stock_basic_info with a successful API response.
    """
    mock_response_data = {
        "stk_cd": "005930",
        "stk_nm": "삼성전자",
        "mrkt_type": "KOSPI",
        "setl_mm": "12",
        "fav": "5000",
        "cap": "1311",
        "flo_stk": "25527",
        "crd_rt": "+0.08",
        "oyr_hgst": "+181400",
        "oyr_lwst": "-91200",
        "mac": "24352",
        "mac_wght": "",
        "for_exh_rt": "0.00",
        "repl_pric": "66780",
        "per": "",
        "eps": "",
        "roe": "",
        "pbr": "",
        "ev": "",
        "bps": "-75300",
        "sale_amt": "0",
        "bus_pro": "0",
        "cup_nga": "0",
        "250hgst": "+124000",
        "250lwst": "-66800",
        "open_pric": "-0",
        "high_pric": "95400",
        "low_pric": "0",
        "upl_pric": "20241016",
        "lst_pric": "-47.41",
        "base_pric": "20231024",
        "exp_cntr_pric": "+26.69",
        "exp_cntr_qty": "95400",
        "250hgst_pric_dt": "3",
        "250hgst_pric_pre_rt": "0",
        "250lwst_pric_dt": "0.00",
        "250lwst_pric_pre_rt": "0",
        "cur_prc": "0.00",
        "prpr": "71100",
        "pre_sig": "",
        "pred_pre": "",
        "flu_rt": "0",
        "trde_qty": "0",
        "trde_pre": "0",
        "fav_unit": "0",
        "dstr_stk": "0",
        "dstr_rt": "0",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다"
    }
    mock_kiwoom_client._authenticated_post.return_value = StockInfo(**mock_response_data)

    stock_code = "005930"
    response = await stock_info_client.get_stock_basic_info(stock_code)

    mock_kiwoom_client._authenticated_post.assert_called_once_with(
        "/api/dostk/stkinfo",
        response_model=StockInfo,
        headers={"api-id": "ka10001"},
        json={"stk_cd": stock_code},
    )
    assert isinstance(response, StockInfo)
    assert response.stock_code == "005930"
    assert response.stock_name == "삼성전자"
    assert response.return_code == 0
    assert response.message == "정상적으로 처리되었습니다"

@pytest.mark.asyncio
async def test_get_stock_basic_info_api_error(stock_info_client: StockInformationClient, mock_kiwoom_client: MockerFixture, mocker: MockerFixture):
    """
    Test get_stock_basic_info with an API error response.
    """
    mock_request = mocker.MagicMock(spec=httpx.Request)
    mock_request.url = "http://test.com/api/dostk/stkinfo" # Dummy URL
    mock_response = Response(status_code=400, request=mock_request)
    mock_kiwoom_client._authenticated_post.side_effect = KiwoomAPIError(
        response=mock_response, error_code=-1, error_message="잘못된 종목코드입니다."
    )

    stock_code = "INVALID_CODE"
    with pytest.raises(KiwoomAPIError) as excinfo:
        await stock_info_client.get_stock_basic_info(stock_code)

    mock_kiwoom_client._authenticated_post.assert_called_once_with(
        "/api/dostk/stkinfo",
        response_model=StockInfo,
        headers={"api-id": "ka10001"},
        json={"stk_cd": stock_code},
    )
    assert "잘못된 종목코드입니다." in str(excinfo.value)
    assert "[-1]" in str(excinfo.value)
