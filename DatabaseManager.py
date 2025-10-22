import psycopg2

class DatabaseManager:
    """
    Singleton класс для управления подключением к базе данных
    с использованием делегации для выполнения запросов
    """
    _instance = None

    def __new__(cls, dbname="postgres", user="postgres", password="password",
                host="localhost", port="5432"):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, dbname="postgres", user="postgres", password="password",
                 host="localhost", port="5432"):
        if not self._initialized:
            self.connection_params = {
                "dbname": dbname,
                "user": user,
                "password": password,
                "host": host,
                "port": port
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
        if self.connection:
            self.connection.close()
            self.is_connected = False
            print("Соединение с базой данных закрыто")

    def execute_query(self, query, params=None):
        """Делегирование выполнения запроса к базе данных"""
        if not self.is_connected or self.connection is None:
            print("Нет подключения к базе данных. Сначала вызовите connect()")
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith('SELECT') or 'RETURNING' in query.upper():
                    return cursor.fetchall()
                else:
                    self.connection.commit()
                    return cursor.rowcount
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            print(f"   Запрос: {query}")
            if self.connection:
                try:
                    self.connection.rollback()
                except:
                    pass
            return None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()