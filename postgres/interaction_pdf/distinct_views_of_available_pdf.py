from postgres.sql_queries import SQL_QUERY_DISTINCT_VIEWS_OF_AVAILABLE_PDF
from postgres.utils.db_operations import execute_query_with_result
from postgres.utils.file_operations import generate_bar_figure
from postgres.utils.metric_operations import calc_course_metric


def unique_views_of_available_pdf(connection):
    return execute_query_with_result(connection, SQL_QUERY_DISTINCT_VIEWS_OF_AVAILABLE_PDF)


def main():
    result_file = "distinct_views_of_available_pdf.csv"
    fields = ['pdf_name', 'views_amount']
    calc_course_metric(
        unique_views_of_available_pdf,
        result_file,
        fields
    )
    generate_bar_figure(result_file, fields)


if __name__ == '__main__':
    main()