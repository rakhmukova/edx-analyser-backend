from metrics.queries.postgres.sql_queries import SQL_QUERY_PLAY_VIDEO_COUNT_DAILY
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.file_operations import RESULT_PATH, generate_line_figure
from metrics.utils.metric_operations import calc_course_metric


def calc_play_video_count_daily(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_PLAY_VIDEO_COUNT_DAILY, course_id)


def main():
    result_file = "video/play_video_count_daily.csv"
    calc_course_metric(
        calc_play_video_count_daily,
        result_file,
        ['date', 'count']
    )
    # generate_line_figure(RESULT_PATH + result_file, ['date', 'count'])


if __name__ == '__main__':
    main()
