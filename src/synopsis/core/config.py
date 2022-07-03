import glob
import json
import pathlib
from pydantic import BaseModel, BaseSettings
from typing import Any, Dict


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    encoding = settings.__config__.env_file_encoding
    return json.loads(pathlib.Path(glob.glob("config/*.config.json")[0]).read_text(encoding))


class Application(BaseModel):
    mode: str
    name: str


class Database(BaseModel):
    uri: str


class Server(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    reload: bool = True


class Settings(BaseSettings):
    db_uri: str
    dev_mode: bool
    server_port: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return init_settings, env_settings, file_secret_settings
