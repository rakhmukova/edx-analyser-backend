from metrics.queries.postgres.sql_queries import SQL_QUERY_COURSE_PAGES_POPULARITY
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric
from metrics.utils.url_operations import remove_parameters_from_url


def calc_course_pages_popularity(connection, course_id):
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
    calc_course_metric(
        calc_course_pages_popularity,
        "pages/course_pages_popularity.csv",
        ['page_link', 'visits_count']
    )


if __name__ == '__main__':
    main()
