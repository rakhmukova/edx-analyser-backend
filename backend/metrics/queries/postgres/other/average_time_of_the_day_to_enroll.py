from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric
from metrics.queries.postgres.sql_queries import SQL_QUERY_AVERAGE_TIME_OF_THE_DAY_TO_ENROLL


def get_enrollment_distribution(connection):
    return execute_query_with_result(connection, SQL_QUERY_AVERAGE_TIME_OF_THE_DAY_TO_ENROLL)


if __name__ == '__main__':
    calc_course_metric(
        get_enrollment_distribution,
        "average_time_of_the_day_to_enroll.csv",
        ['course_id', 'enroll_time']
    )
