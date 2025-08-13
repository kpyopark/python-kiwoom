# -*- coding: utf-8 -*-
"""
kiwoom.stock_information.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains Pydantic models for stock information API requests and responses.
"""

from typing import Optional

from pydantic import BaseModel, Field

class BaseKiwoomResponse(BaseModel):
    """
    Base model for all Kiwoom API responses, containing common fields.
    """
    return_code: int = Field(
        ..., alias="return_code", description="리턴 코드 (0: 성공, 0이외: 실패)"
    )
    message: str = Field(..., alias="return_msg", description="응답 메시지")

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
    market_cap_weight: str = Field(None, alias="mac_wght", description="시가총액비중")
    foreign_exhaustion_rate: str = Field(
        ..., alias="for_exh_rt", description="외인소진률"
    )
    substitute_price: str = Field(..., alias="repl_pric", description="대용가")
    per: Optional[str] = Field(None, alias="per", description="PER")
    eps: Optional[str] = Field(None, alias="eps", description="EPS")
    roe: Optional[str] = Field(None, alias="roe", description="ROE")
    pbr: Optional[str] = Field(None, alias="pbr", description="PBR")
    ev: Optional[str] = Field(None, alias="ev", description="EV")
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
    comparison_symbol: Optional[str] = Field(None, alias="pre_sig", description="대비기호")
    previous_day_comparison: Optional[str] = Field(None, alias="pred_pre", description="전일대비")
    fluctuation_rate: Optional[str] = Field(None, alias="flu_rt", description="등락율")
    trading_volume: Optional[str] = Field(None, alias="trde_qty", description="거래량")
    trading_comparison: Optional[str] = Field(None, alias="trde_pre", description="거래대비")
    face_value_unit: Optional[str] = Field(None, alias="fav_unit", description="액면가단위")
    circulating_shares: Optional[str] = Field(None, alias="dstr_stk", description="유통주식")
    circulation_ratio: Optional[str] = Field(None, alias="dstr_rt", description="유통비율")
