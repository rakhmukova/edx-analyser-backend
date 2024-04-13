from metrics.queries.postgres.sql_queries import SQL_QUERY_VIDEO_INTERACTION, SQL_QUERY_VIDEO_POPULARITY
from metrics.utils.db_operations import execute_query_with_result, open_db_connection, close_db_connection
from metrics.utils.file_operations import save_output_to_file
from metrics.utils.metric_operations import DEFAULT_COURSE_ID
from metrics.utils.url_operations import remove_parameters_from_url

def calculate_pages(connection, course_id):
    return process_urls(execute_query_with_result(connection, SQL_QUERY_VIDEO_INTERACTION, course_id))


def process_urls(result):
    urls_with_counts = {}
    for item in result:
        video_id = item[0]
        url = remove_parameters_from_url(item[1])
        interaction_count = item[2]
        unique_views = item[3]

        # Учитываем ссылки с подстрокой "xblock"
        if 'xblock' in url:
            # Ищем ссылку без параметров для той же video_id
            for key, value in urls_with_counts.items():
                if key == video_id and 'xblock' not in value[0]:
                    urls_with_counts[key][1] += interaction_count
                    urls_with_counts[key][2] = unique_views
                    break
        else:
            if video_id in urls_with_counts:
                urls_with_counts[video_id][1] += interaction_count
                urls_with_counts[video_id][2] = unique_views
            else:
                urls_with_counts[video_id] = [url, interaction_count, unique_views]

    return list(urls_with_counts.values())




def main():
    connection = open_db_connection()
    pages_urls = calculate_pages(connection, course_id=DEFAULT_COURSE_ID)
    headers = ['video_id', 'page_link', 'count_of_visits']
    save_output_to_file("video_popularity.csv", pages_urls, headers)
    close_db_connection(connection)


if __name__ == '__main__':
    main()