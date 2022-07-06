from functools import lru_cache

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from synopsis.core.config import Settings
from synopsis.utils.standard import timestamp


@lru_cache
def session_settings() -> Settings: return Settings()


class Authorization(object):
    algorithm: str = 'HS256'
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    expiration: int = 30
    scheme: OAuth2PasswordBearer

    def __init__(self, settings: Settings):
        token_url = "{}://{}/{}".format("http", f"localhost:{settings.server_port}", "api/oauth/token")
        self.scheme = OAuth2PasswordBearer(tokenUrl=token_url)


class Session(object):
    authorization: Authorization
    settings: Settings = session_settings()
    timestamp: str = timestamp()

    def __init__(self, *args, **kwargs):
        self.authorization = Authorization(self.settings)
        self.args = args[:]
        self.kwargs = kwargs
