import os
from dotenv import load_dotenv
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    # These are set through environment variables automatically
    # See https://docs.pydantic.dev/usage/settings/
    host_es: str
    port_es: int
    # tika_log_file: str

    __annotations__ = {
        'host_es': str,
        'port_es': int,
    }


try: 
    settings = Settings()
    print(settings)
except Exception: 
    load_dotenv()
    settings = Settings()
    print(settings)
