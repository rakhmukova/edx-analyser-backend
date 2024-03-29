from metrics.queries.postgres.sql_queries import SQL_QUERY_COMPLETED_COURSE_USERS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calculate_users_who_finished_the_course(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_COMPLETED_COURSE_USERS, course_id)


if __name__ == '__main__':
    calc_course_metric(
        calculate_users_who_finished_the_course,
        "completed_course_users.csv",
        ['user_id', 'username']
    )
