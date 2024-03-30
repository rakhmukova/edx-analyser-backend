import os
from datetime import datetime
from typing import Any, Union

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.sql import SQL

load_dotenv()

QueryType = Union[SQL, str]


def open_db_connection(database=os.environ.get("POSTGRES_DATABASE")) -> psycopg2.extensions.connection:
    try:
        return psycopg2.connect(
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host="127.0.0.1",
            port="5432",
            database=database
        )
    except (Exception, psycopg2.Error) as error:
        print("Возникла проблема при установлении соединения с PostgreSQL.", error)


def close_db_connection(connection: psycopg2.extensions.connection) -> None:
    if connection:
        connection.close()
        print("Соединение с PostgreSQL завершено.")


def create_database_if_not_exists(database) -> None:
    try:
        connection = open_db_connection(database="postgres")
        create_database_query = sql.SQL(
            f"CREATE DATABASE IF NOT EXISTS {sql.Identifier(database)} WITH ENCODING 'UTF8'")
        execute_query(connection, create_database_query)
        connection.close()
        print("Создана база данных " + database)

    except psycopg2.Error as e:
        print("Error:", e)


def execute_query(connection: psycopg2.extensions.connection, query: QueryType) -> None:
    print('Start query execution at ', datetime.now())
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


def execute_query_with_result(connection: psycopg2.extensions.connection, query: QueryType, course_id: str,
                              isolation_level: int = None) -> list[Any]:
    print('Start query execution at ', datetime.now())
    if isolation_level is not None:
        connection.set_isolation_level(isolation_level)
    cursor = connection.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()
    cursor.close()
    connection.commit()

    print('End query execution at ', datetime.now())
    return query_result


def execute_user_query_with_result(connection: psycopg2.extensions.connection, query: QueryType,
                                   course_id: str, user_id: str, isolation_level=None) -> list[Any]:
    print('Start query execution at ', datetime.now())
    if isolation_level is not None:
        connection.set_isolation_level(isolation_level)
    cursor = connection.cursor()
    cursor.execute(query, (user_id,))
    query_result = cursor.fetchall()
    cursor.close()
    connection.commit()

    print('End query execution at ', datetime.now())
    return query_result
