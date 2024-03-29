from metrics.queries.postgres.sql_queries import SQL_QUERY_DISTINCT_SCROLLING
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.file_operations import generate_bar_figure
from metrics.utils.metric_operations import calc_course_metric


def unique_views_of_available_pdf(connection):
    return execute_query_with_result(connection, SQL_QUERY_DISTINCT_SCROLLING)


def main():
    result_file = "distinct_pdf_scrolling.csv"
    fields = ['pdf_name', 'scrolling_amount']
    calc_course_metric(
        unique_views_of_available_pdf,
        result_file,
        fields
    )
    generate_bar_figure(result_file, fields, xaxis_title='Название PDF', yaxis_title='Количество прокруток')


if __name__ == '__main__':
    main()
