import logging
import sys
from functools import lru_cache
from typing import Any, Dict, List, Tuple

from loguru import logger
from pydantic_settings import BaseSettings

from whisperhub.core.logging import InterceptHandler


class AppSettings(BaseSettings):
    debug: bool = False
    title: str = "WhisperHub"
    version: str = "0.1.0"

    database_url: str = "whisperhub.db"
    max_connection_count: int = 10
    min_connection_count: int = 10

    api_prefix: str = "/api"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        env_file = ".env"
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()
