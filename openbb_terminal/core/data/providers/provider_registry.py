from openbb_terminal.core.data.providers.polygon import PolygonProvider
from openbb_terminal.core.data.providers.yahoo import YahooProvider

# Registry mapping provider names to their corresponding classes
registry = {"polygon": PolygonProvider, "yahoo": YahooProvider}
