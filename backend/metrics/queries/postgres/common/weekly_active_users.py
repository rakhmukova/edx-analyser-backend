from metrics.queries.postgres.sql_queries import SQL_QUERY_WEEKLY_ACTIVE_USERS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric

def calc_weekly_active_users(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_WEEKLY_ACTIVE_USERS, (course_id,))


def main():
    result_file = "common/weekly_active_users.csv"
    fields = ['date', 'count']
    calc_course_metric(
        calc_weekly_active_users,
        result_file,
        fields
    )


if __name__ == '__main__':
    main()