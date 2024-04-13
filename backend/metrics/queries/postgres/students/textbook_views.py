from metrics.queries.postgres.sql_queries import SQL_QUERY_TEXTBOOK_VIEWS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calculate_total_user_time_on_course(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_TEXTBOOK_VIEWS, course_id)

def main():
    calc_course_metric(
        calculate_total_user_time_on_course,
        "students/textbook_views.csv",
        ['username', 'viewed_chapters']
    )


if __name__ == '__main__':
    main()
