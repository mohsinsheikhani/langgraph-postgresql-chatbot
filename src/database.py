import os
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver


class DatabaseManager:
    _instance = None
    _pool = None
    _checkpointer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_checkpointer(self):
        if self._checkpointer is None:
            self._initialize_connection()
        return self._checkpointer

    def _initialize_connection(self):
        db_uri = os.getenv("DB_URI")
        if not db_uri:
            raise ValueError("DB_URI environment variable is required")
        
        connection_kwargs = {"autocommit": True, "prepare_threshold": 0}
        self._pool = ConnectionPool(conninfo=db_uri, max_size=15, kwargs=connection_kwargs)
        self._checkpointer = PostgresSaver(self._pool)
        self._checkpointer.setup()

    def close(self):
        if self._pool:
            self._pool.close()
            self._pool = None
            self._checkpointer = None
