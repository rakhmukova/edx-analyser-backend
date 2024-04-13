from metrics.queries.postgres.sql_queries import SQL_QUERY_COURSE_PAGES_POPULARITY
from metrics.utils.db_operations import execute_query_with_result, open_db_connection, close_db_connection
from metrics.utils.file_operations import save_output_to_file
from metrics.utils.metric_operations import DEFAULT_COURSE_ID
from metrics.utils.url_operations import remove_parameters_from_url


def calculate_pages(connection, course_id):
    return process_urls(execute_query_with_result(connection, SQL_QUERY_COURSE_PAGES_POPULARITY, course_id))


def process_urls(result):
    urls_without_parameters = {}
    for item in result:
        url = remove_parameters_from_url(item[0])
        interaction_count = urls_without_parameters.get(url)
        if not interaction_count:
            interaction_count = 0
        interaction_count += item[1]
        urls_without_parameters[url] = interaction_count

    return list(urls_without_parameters.items())


def main():
    connection = open_db_connection()
    pages_urls = calculate_pages(connection, course_id=DEFAULT_COURSE_ID)
    save_output_to_file("pages/course_pages_popularity.csv", pages_urls, ['page_link, count_of_visits'])
    close_db_connection(connection)


if __name__ == '__main__':
    main()
