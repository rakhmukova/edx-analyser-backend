from datetime import timedelta

from dateutil import parser

from metrics.sql_queries import SQL_QUERY_PLAY_PAUSE_EVENTS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.file_operations import RESULT_PATH, generate_bar_figure
from metrics.utils.metric_operations import calc_course_metric


def calculate_times_for_users(play_pause_events):
    user_times = {}
    user_played_times = {}

    for event in play_pause_events:
        event_type = event[0]
        username = event[1]
        time = event[2]

        if event_type not in ('play_video', 'pause_video'):
            continue

        cur_time = parser.parse(time)

        if username not in user_times:
            user_times[username] = timedelta()
            user_played_times[username] = cur_time
        elif event_type == "pause_video":
            user_times[username] += cur_time - user_played_times[username]
        else:
            user_played_times[username] = cur_time

    return map(lambda x: (x[0], x[1].seconds), list(user_times.items()))


def calc_play_time(connection):
    play_pause_events = execute_query_with_result(connection, SQL_QUERY_PLAY_PAUSE_EVENTS)
    return calculate_times_for_users(play_pause_events)


def main():
    result_file = "fetch_video_viewing_times.csv"
    calc_course_metric(
        calc_play_time,
        result_file,
        ['username', 'time(sec)']
    )
    generate_bar_figure(RESULT_PATH + result_file, ['username', 'time(sec)'])


if __name__ == '__main__':
    main()
