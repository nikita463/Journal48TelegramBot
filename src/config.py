from pydantic_settings import BaseSettings
import json
from os import getenv


class Settings(BaseSettings):
    token: str

    class Config:
        arbitrary_types_allowed = True


def load_config(json_path: str) -> Settings:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Settings(**data)


config = load_config(getenv('CONFIG_FILE', 'config.json'))
