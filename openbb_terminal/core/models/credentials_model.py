from typing import Any, Optional

from pydantic.dataclasses import dataclass

# pylint: disable=too-many-instance-attributes, disable=no-member


@dataclass(config=dict(validate_assignment=True))
class CredentialsModel:
    """Model for credentials."""

    # Data providers
    API_DATABENTO_KEY: str = "REPLACE_ME"
    API_KEY_ALPHAVANTAGE: str = "REPLACE_ME"
    API_KEY_FINANCIALMODELINGPREP: str = "REPLACE_ME"
    API_KEY_QUANDL: str = "REPLACE_ME"
    API_POLYGON_KEY: str = "REPLACE_ME"
    API_FRED_KEY: str = "REPLACE_ME"
    API_NEWS_TOKEN: str = "REPLACE_ME"
    API_CMC_KEY: str = "REPLACE_ME"
    API_FINNHUB_KEY: str = "REPLACE_ME"
    API_IEX_TOKEN: str = "REPLACE_ME"
    API_SENTIMENTINVESTOR_TOKEN: str = "REPLACE_ME"
    API_WHALE_ALERT_KEY: str = "REPLACE_ME"
    API_GLASSNODE_KEY: str = "REPLACE_ME"
    API_COINGLASS_KEY: str = "REPLACE_ME"
    API_ETHPLORER_KEY: str = "REPLACE_ME"
    API_CRYPTO_PANIC_KEY: str = "REPLACE_ME"
    API_BITQUERY_KEY: str = "REPLACE_ME"
    API_SMARTSTAKE_KEY: str = "REPLACE_ME"
    API_SMARTSTAKE_TOKEN: str = "REPLACE_ME"
    API_MESSARI_KEY: str = "REPLACE_ME"
    API_SHROOM_KEY: str = "REPLACE_ME"
    API_SANTIMENT_KEY: str = "REPLACE_ME"
    API_EODHD_KEY: str = "REPLACE_ME"
    API_TOKEN_TERMINAL_KEY: str = "REPLACE_ME"
    API_STOCKSERA_KEY: str = "REPLACE_ME"
    API_INTRINIO_KEY: str = "REPLACE_ME"
    API_TRADIER_TOKEN: str = "REPLACE_ME"

    # Socials
    API_GITHUB_KEY: str = "REPLACE_ME"
    API_REDDIT_CLIENT_ID: str = "REPLACE_ME"
    API_REDDIT_CLIENT_SECRET: str = "REPLACE_ME"
    API_REDDIT_USERNAME: str = "REPLACE_ME"
    API_REDDIT_USER_AGENT: str = "REPLACE_ME"
    API_REDDIT_PASSWORD: str = "REPLACE_ME"
    API_TWITTER_KEY: str = "REPLACE_ME"
    API_TWITTER_SECRET_KEY: str = "REPLACE_ME"
    API_TWITTER_BEARER_TOKEN: str = "REPLACE_ME"

    # Brokers or data providers with brokerage services
    RH_USERNAME: str = "REPLACE_ME"
    RH_PASSWORD: str = "REPLACE_ME"
    DG_USERNAME: str = "REPLACE_ME"
    DG_PASSWORD: str = "REPLACE_ME"
    DG_TOTP_SECRET: Optional[str] = None
    OANDA_ACCOUNT_TYPE: str = "REPLACE_ME"
    OANDA_ACCOUNT: str = "REPLACE_ME"
    OANDA_TOKEN: str = "REPLACE_ME"
    API_BINANCE_KEY: str = "REPLACE_ME"
    API_BINANCE_SECRET: str = "REPLACE_ME"
    API_COINBASE_KEY: str = "REPLACE_ME"
    API_COINBASE_SECRET: str = "REPLACE_ME"
    API_COINBASE_PASS_PHRASE: str = "REPLACE_ME"

    # Others
    OPENBB_PERSONAL_ACCESS_TOKEN: str = "REPLACE_ME"

    def __repr__(self) -> str:
        """Return string representation of model."""
        dataclass_repr = ""
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            dataclass_repr += f"    {key}='{value}', \n"

        return f"{self.__class__.__name__}(\n{dataclass_repr[:-2]}\n)"

    @classmethod
    def get_fields(cls) -> dict[str, Any]:
        """Get dict of fields."""
        return cls.__dataclass_fields__  # type: ignore

    def get_field_value(self, field: str) -> Optional[str]:
        """Get field value."""
        if hasattr(self, field):
            return getattr(self, field)
        return None
