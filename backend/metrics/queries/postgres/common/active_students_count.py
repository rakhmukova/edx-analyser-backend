from metrics.queries.postgres.sql_queries import SQL_QUERY_ACTIVE_STUDENTS_COUNT
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calc_all_users_count(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_ACTIVE_STUDENTS_COUNT, course_id)

def main():
    calc_course_metric(
        calc_all_users_count,
        "common/active_students_count.csv",
        ['active_students_count']
    )


if __name__ == '__main__':
    main()