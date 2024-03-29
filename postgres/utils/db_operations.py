import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()


def open_db_connection(database=os.environ.get("POSTGRES_DATABASE")):
    try:
        connection = psycopg2.connect(
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host="127.0.0.1",
            port="5432",
            database=database
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Возникла проблема при установлении соединения с PostgreSQL.", error)


def close_db_connection(connection):
    if connection:
        connection.close()
        print("Соединение с PostgreSQL завершено.")


def execute_query(connection, query_text):
    print('Start query execution at ', datetime.now())
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(query_text)
    connection.commit()
    cursor.close()


def execute_query_with_result(connection, query_text, isolation_level=None):
    print('Start query execution at ', datetime.now())
    if isolation_level is not None:
        connection.set_isolation_level(isolation_level)
    cursor = connection.cursor()
    cursor.execute(query_text)
    query_result = cursor.fetchall()
    cursor.close()
    connection.commit()

    print('End query execution at ', datetime.now())
    return query_result


def execute_user_query_with_result(connection, query_text, user_id, isolation_level=None):
    print('Start query execution at ', datetime.now())
    if isolation_level is not None:
        connection.set_isolation_level(isolation_level)
    cursor = connection.cursor()
    cursor.execute(query_text, (user_id,))
    query_result = cursor.fetchall()
    cursor.close()
    connection.commit()

    print('End query execution at ', datetime.now())
    return query_result


def create_database_if_not_exists(database):
    try:
        connection = open_db_connection(database="postgres")
        execute_query(connection,
                      sql.SQL(f"CREATE DATABASE IF NOT EXISTS {sql.Identifier(database)} WITH ENCODING 'UTF8'"))
        connection.close()
        print("Создана база данных " + database)

    except psycopg2.Error as e:
        print("Error:", e)
