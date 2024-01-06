import sqlite3

from fastapi import FastAPI
from loguru import logger

from whisperhub.core.config import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to SQLite")

    app.state.db = sqlite3.connect(settings.database_url)

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    app.state.db.close()

    logger.info("Connection closed")
