from typing import List, Dict, Union

from pymysql import connect
from pymysql.err import OperationalError


class UseDatabase:
    """ Класс для работы с бд"""
    def __init__(self, config: dict):
        self.config = config

    def __enter__(self):
        err_mas = {1045: "Не верный логин или пароль",
                   2003: "Не верный хост"}
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] in err_mas:
                print(err_mas[err.args[0]])
                return None

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_type is None:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        else:
            if exc_value.args[0] == 1146:
                print("Неверное имя таблицы")
            elif exc_value.args[0] == 1054:
                print(
                    "Неверное имя столбца")
        return True


def work_with_db(dbconfig, _SQL):
    """


    Args:
        dbconfig: dict
        _SQL: str
    Returns:
        .list
    """
    result = []
    with UseDatabase(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('No connetect')
        cursor.execute(_SQL)
        schema = [column[0] for column in cursor.description]
        for str in cursor.fetchall():
            result.append(dict(zip(schema, str)))
    return result


def make_update(dbconfig, _SQL):
    """
    Выполняет обновление в базе данных с помощью sql-запроса

    Args:
            dbconfig: dict. Параметры подключения к бд
            _SQL: str. Sql-запрос для выполнения обновления

    Returns:
        .bool
    """
    with UseDatabase(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('No connetect')
        a = cursor.execute(_SQL)
    return True
