from metrics.queries.postgres.sql_queries import SQL_QUERY_UNIQUE_COURSES
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calc_unique_courses(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_UNIQUE_COURSES)


def main():
    calc_course_metric(
        calc_unique_courses,
        "util/unique_courses.csv",
        ['course_id', 'count']
    )


if __name__ == '__main__':
    main()