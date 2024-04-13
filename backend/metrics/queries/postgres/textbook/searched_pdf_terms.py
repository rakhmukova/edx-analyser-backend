from metrics.queries.postgres.sql_queries import SQL_QUERY_SEARCHED_PDF_TERMS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calc_search_pdf_terms(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_SEARCHED_PDF_TERMS, course_id)


def main():
    result_file = "textbook/searched_pdf_terms.csv"
    fields = ['word', 'search_count']
    calc_course_metric(
        calc_search_pdf_terms,
        result_file,
        fields
    )


if __name__ == '__main__':
    main()
