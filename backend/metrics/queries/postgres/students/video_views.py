from metrics.queries.postgres.sql_queries import SQL_QUERY_VIDEO_VIEWS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calc_video_views(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_VIDEO_VIEWS, course_id)

def main():
    calc_course_metric(
        calc_video_views,
        "students/video_views.csv",
        ['username', 'viewed_videos']
    )


if __name__ == '__main__':
    main()
