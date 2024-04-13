import os
from datetime import datetime
from typing import Any, Union
from venv import logger

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.sql import SQL

load_dotenv()

QueryType = Union[SQL, str]


def open_db_connection(database=os.environ.get("LOGS_DB_DATABASE")) -> psycopg2.extensions.connection:
    try:
        return psycopg2.connect(
            user=os.environ.get("LOGS_DB_USER"),
            password=os.environ.get("LOGS_DB_PASSWORD"),
            host="localhost", #os.environ.get("LOGS_DB_HOST", "localhost"),
            port=os.environ.get("LOGS_DB_PORT"),
            database=database
        )
    except (Exception, psycopg2.Error) as error:
        logger.error("Возникла проблема при установлении соединения с PostgreSQL.", error)


def close_db_connection(connection: psycopg2.extensions.connection) -> None:
    if connection:
        connection.close()
        logger.info("Соединение с PostgreSQL завершено.")


def execute_query(connection: psycopg2.extensions.connection, query: QueryType) -> None:
    logger.info('Start query execution at ', datetime.now())
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


def execute_query_with_result(connection: psycopg2.extensions.connection, query: QueryType, course_id: str,
                              isolation_level: int = None) -> list[Any]:
    logger.info('Start query execution at ', datetime.now())
    if isolation_level is not None:
        connection.set_isolation_level(isolation_level)
    cursor = connection.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()
    cursor.close()
    connection.commit()

    logger.info('End query execution at ', datetime.now())
    return query_result


def execute_user_query_with_result(connection: psycopg2.extensions.connection, query: QueryType,
                                   course_id: str, user_id: str, isolation_level=None) -> list[Any]:
    logger.info('Start query execution at ', datetime.now())
    if isolation_level is not None:
        connection.set_isolation_level(isolation_level)
    cursor = connection.cursor()
    cursor.execute(query, (user_id,))
    query_result = cursor.fetchall()
    cursor.close()
    connection.commit()

    logger.info('End query execution at ', datetime.now())
    return query_result
