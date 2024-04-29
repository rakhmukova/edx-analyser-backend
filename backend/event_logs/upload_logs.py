from venv import logger

from metrics.utils.db_operations import execute_query


def create_logs_table(connection):
    create_table_query = '''
        CREATE UNLOGGED TABLE IF NOT EXISTS logs
        (log_line jsonb NOT NULL)'''

    execute_query(connection, create_table_query)
    logger.info("Table logs has been created")

def insert_lines(cur, lines_array):
    records_list_template = ','.join(['(%s)'] * len(lines_array))
    insert_query = f'INSERT INTO logs(log_line) VALUES {records_list_template}'
    cur.execute(insert_query, lines_array)


def insert_logs(connection, logs_file):
    logger.info('Начинаем загрузку файлов ')
    lines_in_batch = 100
    lines_array = []
    count = 0
    cur = connection.cursor()
    with open(logs_file, encoding="utf-8") as logs:
        for line in logs:
            lines_array.append(line)
            count += 1
            if len(lines_array) >= lines_in_batch:
                insert_lines(cur, lines_array)
                lines_array = []

    if len(lines_array) > 0:
        insert_lines(cur, lines_array)

    logger.info('Лог-файлы загружены ')
    logger.info('Количество загруженных записей: ', count)
