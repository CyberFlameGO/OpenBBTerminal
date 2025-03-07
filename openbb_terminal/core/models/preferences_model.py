import os
from typing import Any, Optional

from pydantic import NonNegativeInt, PositiveFloat, PositiveInt
from pydantic.dataclasses import dataclass

from openbb_terminal.core.config.paths import (
    HOME_DIRECTORY,
    USER_DATA_SOURCES_DEFAULT_FILE,
)

# pylint: disable=too-many-instance-attributes, disable=no-member


@dataclass(config=dict(validate_assignment=True, frozen=True))
class PreferencesModel:
    """Data model for preferences."""

    # PLOT
    # Plot backend
    # Examples:
    # "tkAgg" - This uses the tkinter library.  If unsure, set to this
    # "module://backend_interagg" - This is what pycharm defaults to in Scientific Mode
    # "MacOSX" - Mac default.  Does not work with backtesting
    # "Qt5Agg" - This requires the PyQt5 package is installed
    # See more: https://matplotlib.org/stable/tutorials/introductory/usage.html#the-builtin-backends
    PLOT_BACKEND: Optional[str] = None
    PLOT_DPI: PositiveInt = 100
    PLOT_HEIGHT: PositiveInt = 500
    PLOT_WIDTH: PositiveInt = 800
    PLOT_HEIGHT_PERCENTAGE: PositiveFloat = 50.0
    PLOT_WIDTH_PERCENTAGE: PositiveFloat = 70.0
    # Whether to open plot image exports after they are created
    PLOT_OPEN_EXPORT: bool = False

    # FEATURE FLAGS
    SYNC_ENABLED: bool = True
    FILE_OVERWRITE: bool = False
    RETRY_WITH_LOAD: bool = False
    USE_TABULATE_DF: bool = True
    # Use interactive window to display dataframes with options to sort, filter, etc.
    USE_INTERACTIVE_DF = True
    USE_CLEAR_AFTER_CMD: bool = False
    USE_COLOR: bool = True
    USE_DATETIME: bool = True
    # Enable interactive matplotlib mode: change variable name to be more descriptive and delete comment
    USE_ION: bool = True
    USE_WATERMARK: bool = True
    # Enable command and source in the figures: change variable name to be more descriptive and delete comment
    USE_CMD_LOCATION_FIGURE: bool = True
    USE_PROMPT_TOOLKIT: bool = True
    USE_PLOT_AUTOSCALING: bool = False
    ENABLE_THOUGHTS_DAY: bool = False
    ENABLE_QUICK_EXIT: bool = False
    OPEN_REPORT_AS_HTML: bool = True
    ENABLE_EXIT_AUTO_HELP: bool = True
    REMEMBER_CONTEXTS: bool = True
    ENABLE_RICH: bool = True
    ENABLE_RICH_PANEL: bool = True
    ENABLE_CHECK_API: bool = True
    TOOLBAR_HINT: bool = True
    TOOLBAR_TWEET_NEWS: bool = False

    # TOOLBAR
    TOOLBAR_TWEET_NEWS_SECONDS_BETWEEN_UPDATES: PositiveInt = 300
    TOOLBAR_TWEET_NEWS_ACCOUNTS_TO_TRACK: str = (
        "WatcherGuru,unusual_whales,gurgavin,CBSNews"
    )
    TOOLBAR_TWEET_NEWS_KEYWORDS: str = "BREAKING,JUST IN"
    TOOLBAR_TWEET_NEWS_NUM_LAST_TWEETS_TO_READ: PositiveInt = 3

    # GENERAL
    PREVIOUS_USE: bool = False
    TIMEZONE: str = "America/New_York"
    FLAIR: str = ":openbb"
    USE_LANGUAGE: str = "en"
    REQUEST_TIMEOUT: PositiveInt = 5
    MONITOR: NonNegativeInt = 0

    # STYLE
    # Color for `view` command data.  All pyplot colors listed at:
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    VIEW_COLOR: str = "tab:green"
    MPL_STYLE: str = "dark"
    PMF_STYLE: str = "dark"
    RICH_STYLE: str = "dark"

    # PATHS
    PREFERRED_DATA_SOURCE_FILE: str = str(USER_DATA_SOURCES_DEFAULT_FILE)
    GUESS_EASTER_EGG_FILE: str = os.getcwd() + os.path.sep + "guess_game.json"
    USER_DATA_DIRECTORY = HOME_DIRECTORY / "OpenBBUserData"
    USER_EXPORTS_DIRECTORY = USER_DATA_DIRECTORY / "exports"
    USER_CUSTOM_IMPORTS_DIRECTORY = USER_DATA_DIRECTORY / "custom_imports"
    USER_PORTFOLIO_DATA_DIRECTORY = USER_DATA_DIRECTORY / "portfolio"
    USER_ROUTINES_DIRECTORY = USER_DATA_DIRECTORY / "routines"
    USER_PRESETS_DIRECTORY = USER_DATA_DIRECTORY / "presets"
    USER_REPORTS_DIRECTORY = USER_DATA_DIRECTORY / "reports"
    USER_CUSTOM_REPORTS_DIRECTORY = USER_DATA_DIRECTORY / "reports" / "custom reports"
    USER_FORECAST_MODELS_DIRECTORY = USER_DATA_DIRECTORY / "exports" / "forecast_models"
    USER_FORECAST_WHISPER_DIRECTORY = USER_DATA_DIRECTORY / "exports" / "whisper"

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
