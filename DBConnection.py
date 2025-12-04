from typing import Any, List, Optional, Tuple, Union

import psycopg2


class DBConnection:
    def __init__(
        self,
        dbname: str = "postgres",
        user: str = "postgres",
        password: str = "password",
        host: str = "localhost",
        port: str = "5433",
    ) -> None:
        self.connection_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        self.connection: Any = None
        self.is_connected: bool = False

    def connect(self) -> bool:
        """Установить соединение с базой данных"""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.is_connected = True
            print(f"Успешное подключение к базе данных '{self.connection_params['dbname']}'")
            return True
        except Exception as e:
            print(f"Ошибка подключения к базе данных '{self.connection_params['dbname']}': {e}")
            self.is_connected = False
            return False

    def disconnect(self) -> None:
        """Закрыть соединение с базой данных"""
        if self.connection:
            self.connection.close()
            self.is_connected = False
            print("Соединение с базой данных закрыто")

    def execute_query(
        self, query: str, params: Optional[Tuple[Any, ...]] = None
    ) -> Optional[Union[List[Tuple[Any, ...]], int]]:
        """Выполнить запрос и вернуть результат"""
        if not self.is_connected or self.connection is None:
            print("Нет подключения к базе данных. Сначала вызовите connect()")
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith("SELECT") or "RETURNING" in query.upper():
                    return cursor.fetchall() # извлекает все строки
                else:
                    self.connection.commit()
                    return cursor.rowcount
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            print(f"Запрос: {query}")
            if self.connection:
                try:
                    self.connection.rollback()
                except Exception as rollback_error:
                    print(f"Ошибка при откате транзакции: {rollback_error}")
            return None

    def __enter__(self) -> "DBConnection":
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any],
    ) -> None:
        self.disconnect()
