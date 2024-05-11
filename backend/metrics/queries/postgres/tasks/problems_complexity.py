from metrics.queries.postgres.sql_queries import SQL_QUERY_CORRECTLY_SOLVED_PROBLEMS
from metrics.utils.db_operations import execute_query_with_result, open_db_connection, close_db_connection
from metrics.utils.file_operations import save_output_to_file
from metrics.utils.metric_operations import DEFAULT_COURSE_ID
from metrics.utils.url_operations import remove_parameters_from_url


def calc_problems_complexity(connection, course_id):
    return process_urls(
        execute_query_with_result(connection, SQL_QUERY_CORRECTLY_SOLVED_PROBLEMS, (course_id, course_id, course_id,)))


def process_urls(result):
    result.sort(key=lambda item: 'xblock' in item[1])

    urls_with_counts = {}
    for item in result:
        video_id = item[0]
        url = remove_parameters_from_url(item[1])
        all_attempts = item[2]
        correct_attempts = item[3]

        if video_id in urls_with_counts:
            urls_with_counts[video_id][1] = all_attempts
            urls_with_counts[video_id][2] = correct_attempts
        else:
            urls_with_counts[video_id] = [url, all_attempts, correct_attempts]

    return list(urls_with_counts.values())


def main():
    connection = open_db_connection()
    pages_urls = calc_problems_complexity(connection, course_id=DEFAULT_COURSE_ID)
    headers = ['problem_link', 'all_attempts', 'successful_attempts']
    save_output_to_file("tasks/problems_complexity.csv", pages_urls, headers)
    close_db_connection(connection)


if __name__ == '__main__':
    main()
