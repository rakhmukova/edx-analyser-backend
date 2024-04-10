from metrics.queries.postgres.sql_queries import SQL_QUERY_DAILY_ACTIVE_USERS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric

def unique_usernames_and_ids(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_DAILY_ACTIVE_USERS, course_id)


def main():
    result_file = "daily_active_users.csv"
    fields = ['date', 'count_of_users']
    calc_course_metric(
        unique_usernames_and_ids,
        result_file,
        fields
    )


if __name__ == '__main__':
    main()