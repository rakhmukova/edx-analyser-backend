from metrics.queries.postgres.sql_queries import SQL_QUERY_PLAY_VIDEO_TIMES
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.file_operations import RESULT_PATH, generate_line_figure
from metrics.utils.metric_operations import calc_course_metric


def calculate_video_start_times(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_PLAY_VIDEO_TIMES, course_id)


def main():
    result_file = "play_video_count_daily.csv"
    calc_course_metric(
        calculate_video_start_times,
        result_file,
        ['time', 'count']
    )
    generate_line_figure(RESULT_PATH + result_file, ['time', 'count'])


if __name__ == '__main__':
    main()
