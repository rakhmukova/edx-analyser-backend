from metrics.queries.postgres.sql_queries import SQL_QUERY_ALL_USERS_COUNT

from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calculate_total_user_time_on_course(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_ALL_USERS_COUNT, course_id)

def main():
    total_users_time_on_course = calc_course_metric(
        calculate_total_user_time_on_course,
        "all_users_count.csv",
        ['all_users_count']
    )
    # generate_total_time_distribution_figure(total_users_time_on_course)


if __name__ == '__main__':
    main()
