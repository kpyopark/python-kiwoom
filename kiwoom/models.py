# -*- coding: utf-8 -*-
"""
kiwoom.models
~~~~~~~~~~~~~

This module contains Pydantic models for API requests and responses.
"""

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseKiwoomResponse(BaseModel):
    """
    Base model for all Kiwoom API responses, containing common fields.
    """
    return_code: int = Field(
        ..., alias="return_code", description="리턴 코드 (0: 성공, 0이외: 실패)"
    )
    message: str = Field(..., alias="return_msg", description="응답 메시지")


class AuthResponse(BaseKiwoomResponse):
    """Authentication API Response Model"""
    token: str = Field(..., description="접근토큰")
    token_type: str = Field(..., description="토큰타입")
    expires_dt: str = Field(..., description="만료일")


class StockInfo(BaseKiwoomResponse):
    """주식기본정보"""
    stock_code: str = Field(..., alias="stk_cd", description="종목코드")
    stock_name: str = Field(..., alias="stk_nm", description="종목명")
    market_type: Optional[str] = Field(None, alias="mrkt_type", description="시장구분")
    settlement_month: str = Field(..., alias="setl_mm", description="결산월")
    face_value: str = Field(..., alias="fav", description="액면가")
    capital: str = Field(..., alias="cap", description="자본금")
    listed_shares: str = Field(..., alias="flo_stk", description="상장주식")
    credit_ratio: str = Field(..., alias="crd_rt", description="신용비율")
    year_high: str = Field(..., alias="oyr_hgst", description="연중최고")
    year_low: str = Field(..., alias="oyr_lwst", description="연중최저")
    market_cap: str = Field(..., alias="mac", description="시가총액")
    market_cap_weight: str = Field(..., alias="mac_wght", description="시가총액비중")
    foreign_exhaustion_rate: str = Field(
        ..., alias="for_exh_rt", description="외인소진률"
    )
    substitute_price: str = Field(..., alias="repl_pric", description="대용가")
    per: str = Field(..., alias="per", description="PER")
    eps: str = Field(..., alias="eps", description="EPS")
    roe: str = Field(..., alias="roe", description="ROE")
    pbr: str = Field(..., alias="pbr", description="PBR")
    ev: str = Field(..., alias="ev", description="EV")
    bps: str = Field(..., alias="bps", description="BPS")
    sales: str = Field(..., alias="sale_amt", description="매출액")
    operating_profit: str = Field(..., alias="bus_pro", description="영업이익")
    net_income: str = Field(..., alias="cup_nga", description="당기순이익")
    high_250: str = Field(..., alias="250hgst", description="250최고")
    low_250: str = Field(..., alias="250lwst", description="250최저")
    opening_price: str = Field(..., alias="open_pric", description="시가")
    high_price: str = Field(..., alias="high_pric", description="고가")
    low_price: str = Field(..., alias="low_pric", description="저가")
    upper_limit_price: str = Field(..., alias="upl_pric", description="상한가")
    lower_limit_price: str = Field(..., alias="lst_pric", description="하한가")
    standard_price: str = Field(..., alias="base_pric", description="기준가")
    expected_conclusion_price: str = Field(
        ..., alias="exp_cntr_pric", description="예상체결가"
    )
    expected_conclusion_quantity: str = Field(
        ..., alias="exp_cntr_qty", description="예상체결수량"
    )
    date_250_high: str = Field(..., alias="250hgst_pric_dt", description="250최고가일")
    rate_250_high: str = Field(
        ..., alias="250hgst_pric_pre_rt", description="250최고가대비율"
    )
    date_250_low: str = Field(..., alias="250lwst_pric_dt", description="250최저가일")
    rate_250_low: str = Field(
        ..., alias="250lwst_pric_pre_rt", description="250최저가대비율"
    )
    current_price: str = Field(..., alias="cur_prc", description="현재가")
    present_price: Optional[str] = Field(None, alias="prpr", description="현재가 (prpr)")
    comparison_symbol: str = Field(..., alias="pre_sig", description="대비기호")
    previous_day_comparison: str = Field(..., alias="pred_pre", description="전일대비")
    fluctuation_rate: str = Field(..., alias="flu_rt", description="등락율")
    trading_volume: str = Field(..., alias="trde_qty", description="거래량")
    trading_comparison: str = Field(..., alias="trde_pre", description="거래대비")
    face_value_unit: str = Field(..., alias="fav_unit", description="액면가단위")
    circulating_shares: str = Field(..., alias="dstr_stk", description="유통주식")
    circulation_ratio: str = Field(..., alias="dstr_rt", description="유통비율")


class Pagination(BaseModel):
    """
    Pagination information for list responses.
    """

    context: str = Field(..., alias="ctx_area_fk", description="연속 조회 키")
    next_page: str = Field(..., alias="ctx_area_nk", description="연속 조회 다음 키")


class PaginatedResponse(BaseKiwoomResponse, Generic[T]):
    """
    Standard paginated API response model.
    """
    data: List[T] = Field(..., description="응답 데이터 목록")
    pagination: Optional[Pagination] = Field(None, description="페이지네이션 정보")
