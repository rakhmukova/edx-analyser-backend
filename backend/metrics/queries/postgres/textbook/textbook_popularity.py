from metrics.queries.postgres.sql_queries import SQL_QUERY_TEXTBOOK_POPULARITY
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def unique_views_of_available_pdf(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_TEXTBOOK_POPULARITY, (course_id,))


def main():
    result_file = "textbook/textbook_popularity.csv"
    fields = ['chapter', 'views_count', 'unique_students_count']
    calc_course_metric(
        unique_views_of_available_pdf,
        result_file,
        fields
    )

if __name__ == '__main__':
    main()
