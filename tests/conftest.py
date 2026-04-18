import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

@pytest.fixture(autouse=True, scope="session")
def setup_api_testing():
    """
    Global setup for API testing.
    Initializes the cache in-memory to prevent 'init first' errors.
    """
    FastAPICache.init(InMemoryBackend())
    yield
