from metrics.queries.postgres.sql_queries import SQL_QUERY_STARTED_BUT_NOT_COMPLETED_USERS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calculate_users_who_started_but_not_completed(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_STARTED_BUT_NOT_COMPLETED_USERS, course_id)


if __name__ == '__main__':
    calc_course_metric(
        calculate_users_who_started_but_not_completed,
        "started_but_not_completed_course.csv",
        ['user_id', 'username']
    )
