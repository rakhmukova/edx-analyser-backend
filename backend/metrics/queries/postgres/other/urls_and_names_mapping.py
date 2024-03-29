from metrics.queries.postgres.sql_queries import SQL_QUERY_URLS_AND_NAMES_MAPPING
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calculate_urls_and_names_mapping(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_URLS_AND_NAMES_MAPPING, course_id)


if __name__ == '__main__':
    calc_course_metric(
        calculate_urls_and_names_mapping,
        "urls_and_names_mapping.csv",
        ['target_name', 'target_url']
    )
