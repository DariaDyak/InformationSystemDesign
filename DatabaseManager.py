import psycopg2


class DatabaseManager:
    """
    Singleton класс для управления подключением к базе данных
    с использованием делегации для выполнения запросов
    """

    _instance = None  # статическая переменная, хранящая единственный экземпляр класса

    def __new__(
            cls, dbname="dasha", user="postgres", password="123", host="localhost", port="5433"
    ):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance  # всегда возвращаем один и тот же экземпляр

    def __init__(
            self, dbname="dasha", user="postgres", password="123", host="localhost", port="5433"
    ):
        if not self._initialized:
            self.connection_params = {
                "dbname": dbname,
                "user": user,
                "password": password,
                "host": host,
                "port": port,
            }
            self.connection = None
            self.is_connected = False
            self._initialized = True

    def connect(self):
        """Установить соединение с базой данных"""
        if self.is_connected and self.connection:
            return True

        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.is_connected = True
            print(f"Успешное подключение к базе данных '{self.connection_params['dbname']}'")
            return True
        except Exception as e:
            print(f"Ошибка подключения к базе данных '{self.connection_params['dbname']}': {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """Закрыть соединение с базой данных"""
        if self.connected:
            self.connection.close()
            self.is_connected = False
            print("Соединение с базой данных закрыто")

    def execute_query(self, query, params=None):
        """Делегирование выполнения запроса к базе данных"""
        if not self.is_connected or self.connection is None:
            if not self.connect():
                print("Нет подключения к базе данных. Не удалось подключиться")
                return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)  # делегируем выполнение курсору

                query_upper = query.strip().upper()
                is_select = query_upper.startswith("SELECT")
                has_returning = "RETURNING" in query_upper

                if is_select or has_returning:
                    result = cursor.fetchall()
                    self.connection.commit()
                    return result
                else:
                    self.connection.commit()
                    return cursor.rowcount

        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            print(f"   Запрос: {query}")
            print(f"   Параметры: {params}")
            if self.connection:
                try:
                    self.connection.rollback()
                except Exception as rollback_error:
                    print(f"Ошибка при откате транзакции: {rollback_error}")
            return None

    @property
    def connected(self):
        """Проверка активности соединения"""
        if self.connection and self.is_connected:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                return True
            except Exception:
                self.is_connected = False
                return False
        return False

    def commit(self):
        """Явное подтверждение транзакции"""
        if self.connection and self.is_connected:
            try:
                self.connection.commit()
                return True
            except Exception as e:
                print(f"Ошибка при коммите: {e}")
                return False
        return False

    def rollback(self):
        """Откат транзакции"""
        if self.connection and self.is_connected:
            try:
                self.connection.rollback()
                return True
            except Exception as e:
                print(f"Ошибка при откате: {e}")
                return False
        return False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.disconnect()