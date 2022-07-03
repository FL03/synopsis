from functools import lru_cache

from synopsis.core.config import Settings
from synopsis.utils.standard import timestamp


@lru_cache
def session_settings() -> Settings: return Settings()


class Session(object):
    settings: Settings = session_settings()
    timestamp: str = timestamp()

    def __init__(self, *args, **kwargs):
        self.args = args[:]
        self.kwargs = kwargs
