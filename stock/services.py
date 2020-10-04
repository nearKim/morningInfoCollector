import typing

import yfinance as yf
from pandas import DataFrame

__all__ = ["default_stock_service"]


class StockService:
    def get_stock_data(
        self, tickers: typing.List[str], period: str, interval: str = None
    ) -> DataFrame:
        ticker_string = " ".join(tickers)
        if interval:
            data = yf.download(
                ticker_string, period=period, group_by="ticker", interval=interval
            )
        else:
            data = yf.download(ticker_string, period=period, group_by="ticker")
        return data


default_stock_service = StockService()
