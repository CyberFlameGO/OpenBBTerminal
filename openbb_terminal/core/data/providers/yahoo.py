from datetime import datetime
import os
import pandas as pd
import yfinance as yf

from openbb_terminal.core.data.providers.provider_base import ProviderBase


class YahooProvider(ProviderBase):
    """
    A provider class for loading stock data from the Yahoo Finance API.

    Inherits from ProviderBase.
    """

    def __init__(self, api_key: str = None):
        """
        Initializes a new instance of the YahooProvider class.

        Parameters:
            api_key (str): The API key to use for authentication.
        """
        self.api_key = api_key

    def load_stock_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        weekly: bool,
        monthly: bool,
    ) -> pd.DataFrame:
        """
        Loads stock data from the Yahoo Finance API.

        Parameters:
            symbol (str): The ticker symbol of the stock to load.
            start_date (str): The start date of the data to load, in YYYY-MM-DD format.
            end_date (str): The end date of the data to load, in YYYY-MM-DD format.
            weekly (bool): Whether to load weekly data (True) or daily data (False).
            monthly (bool): Whether to load monthly data (True) or daily data (False).

        Returns:
            pd.DataFrame: A DataFrame containing the loaded stock data.
        """
        int_ = "1d"
        int_string = "Daily"
        if weekly:
            int_ = "1wk"
            int_string = "Weekly"
        if monthly:
            int_ = "1mo"
            int_string = "Monthly"

        # Win10 version of mktime cannot cope with dates before 1970
        if os.name == "nt" and start_date < datetime(1970, 1, 1):
            start_date = datetime(
                1970, 1, 2
            )  # 1 day buffer in case of timezone adjustments

        # Adding a dropna for weekly and monthly because these include weird NaN columns.
        df_stock_candidate = yf.download(
            symbol,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=True,
            actions=True,
            interval=int_,
            ignore_tz=True,
        ).dropna(axis=0)

        # Check that loading a stock was not successful
        if df_stock_candidate.empty:
            return pd.DataFrame()
        df_stock_candidate_cols = [
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
            "Dividends",
            "Stock Splits",
        ]
        df_stock_candidate.index.name = "date", int_string
        df_stock_candidate["Adj Close"] = df_stock_candidate["Close"].copy()
        df_stock_candidate = pd.DataFrame(
            data=df_stock_candidate, columns=df_stock_candidate_cols
        )
        df_stock_candidate["Volume"] = df_stock_candidate["Volume"].astype(float)
        # df_stock_candidate.reset_index(inplace=True)
        # df_stock_candidate = df_stock_candidate.rename(
        #     columns={"(date, Daily)": "date"}
        # )
        df_stock_candidate = df_stock_candidate.rename_axis("date").reset_index()

        return df_stock_candidate

    def load_fundamental_data(
        self, api_key: str, symbol: str, date: str
    ) -> pd.DataFrame:
        """
        Loads fundamental data from the Yahoo Finance API.

        Note: This method is not implemented for this provider.

        Parameters:
            api_key (str): The API key
            symbol (str): The ticker symbol of the stock to load.
            date (str): The date of the data to load, in YYYY-MM-DD format.
        """
        raise NotImplementedError("This method is not implemented for this provider.")
