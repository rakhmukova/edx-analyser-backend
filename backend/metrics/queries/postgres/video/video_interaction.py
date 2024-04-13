from metrics.queries.postgres.sql_queries import SQL_QUERY_VIDEO_INTERACTION
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric
from metrics.utils.url_operations import remove_parameters_from_url


def calc_video_popularity(connection, course_id):
    return process_urls(execute_query_with_result(connection, SQL_QUERY_VIDEO_INTERACTION, course_id))


def process_urls(result):
    urls_with_counts = {}
    for item in result:
        video_id = item[0]
        url = remove_parameters_from_url(item[1])
        views_count = item[2]
        unique_views = item[3]

        # Учитываем ссылки с подстрокой "xblock"
        if 'xblock' in url:
            continue
        else:
            if video_id in urls_with_counts:
                urls_with_counts[video_id][1] += views_count
                urls_with_counts[video_id][2] = unique_views
            else:
                urls_with_counts[video_id] = [url, views_count, unique_views]

    return list(urls_with_counts.values())


def main():
    calc_course_metric(
        calc_video_popularity,
        "video/video_popularity.csv",
        ['video_link', 'views_count', 'unique_students_count']
    )


if __name__ == '__main__':
    main()
