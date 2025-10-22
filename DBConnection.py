import psycopg2

class DBConnection:
    def __init__(self, dbname="postgres", user="postgres", password="password", host="localhost", port="5432"):
        self.connection_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.connection = None
        self.is_connected = False

    def connect(self):
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

    def disconnect(self):
        """Закрыть соединение с базой данных"""
        if self.connection:
            self.connection.close()
            self.is_connected = False
            print("Соединение с базой данных закрыто")

    def execute_query(self, query, params=None):
        """Выполнить запрос и вернуть результат"""
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
            print(f"Запрос: {query}")
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