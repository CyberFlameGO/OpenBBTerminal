from abc import ABC, abstractmethod
import pandas as pd


class ProviderBase(ABC):
    """
    Abstract Base Class for data providers. All data providers should inherit from this class
    and implement the defined abstract methods.
    """

    @abstractmethod
    def load_stock_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        weekly: bool,
        monthly: bool,
    ) -> pd.DataFrame:
        """
        Load stock price data for a given symbol from the provider's data source.

        Parameters
        ----------
        symbol : str
            The stock symbol to load data for.
        start_date : str
            The start date for the time range of data to load, in "YYYY-MM-DD" format.
        end_date : str
            The end date for the time range of data to load, in "YYYY-MM-DD" format.
        weekly : bool
            Whether to load data on a weekly basis.
        monthly : bool
            Whether to load data on a monthly basis.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the loaded stock price data.
        """
        pass

    @abstractmethod
    def load_fundamental_data(
        self, api_key: str, symbol: str, date: str
    ) -> pd.DataFrame:
        """
        Load fundamental data for a given stock symbol and date from the provider's data source.

        Parameters
        ----------
        api_key : str
            The API key to use to authenticate with the provider's API.
        symbol : str
            The stock symbol to load data for.
        date : str
            The date to load data for, in "YYYY-MM-DD" format.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the loaded fundamental data.
        """
        pass
