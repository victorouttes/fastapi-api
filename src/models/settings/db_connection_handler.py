import os
import ssl

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    def __init__(self) -> None:
        from dotenv import load_dotenv
        load_dotenv()
        self.__host = os.environ.get("PG_HOST")
        self.__port = os.environ.get("PG_PORT")
        self.__db = os.environ.get("PG_DB")
        self.__user = os.environ.get("PG_USER")
        self.__password = os.environ.get("PG_PASSWORD")

        self.__ssl_context = ssl.create_default_context()
        self.__ssl_context.check_hostname = False
        self.__ssl_context.verify_mode = ssl.CERT_NONE
        self.__engine = create_async_engine(
            url=f"postgresql+asyncpg://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__db}",
            connect_args={"ssl": self.__ssl_context},
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            echo=False
        )

    def get_engine(self):
        return self.__engine

    def get_session(self) -> AsyncSession:
        return sessionmaker(
            self.__engine,
            class_=AsyncSession,
            expire_on_commit=True
        )

db_connection_handler = DBConnectionHandler()
