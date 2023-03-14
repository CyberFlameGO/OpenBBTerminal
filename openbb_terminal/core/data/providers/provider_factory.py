from openbb_terminal.core.data.providers.provider_registry import registry


class ApiFactory:
    """
    ApiFactory is a static class that creates instances of data provider classes for a
    given source and API key. It relies on the registry module from
    openbb_terminal.core.data.providers to look up the appropriate data provider class
    based on the specified source.

    Args:
        source (str): A string representing the source of the data provider.
        api_key (str): A string representing the API key to use for authentication.

    Returns:
        An instance of the data provider class that corresponds to the specified source.

    Raises:
        ValueError: If the specified source is not supported by any of the registered
        data provider classes in the registry.
    """

    @staticmethod
    def create(source: str, api_key: str):
        provider_class = registry.get(source)
        if provider_class is None:
            raise ValueError("API not supported")
        return provider_class(api_key=api_key)
