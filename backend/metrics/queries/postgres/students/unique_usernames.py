from metrics.queries.postgres.sql_queries import SQL_QUERY_UNIQUE_USERNAMES
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric
import csv

def unique_usernames(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_UNIQUE_USERNAMES, course_id)


def main():
    result_file = "students/unique_usernames.csv"
    fields = ['username']
    calc_course_metric(
        unique_usernames,
        result_file,
        fields
    )


if __name__ == '__main__':
    main()