from metrics.queries.postgres.sql_queries import SQL_QUERY_TOP_THREADS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calc_top_threads(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_TOP_THREADS, course_id)


def main():
    calc_course_metric(
        calc_top_threads,
        "forum/top_threads.csv",
        ['author', 'title', 'body', 'comments_count', 'likes_count']
    )


if __name__ == '__main__':
    main()
