from datetime import datetime

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from metrics.sql_queries import SQL_QUERY_EVENTS_DISTRIBUTION
from metrics.utils.db_operations import close_db_connection, open_db_connection
from metrics.utils.file_operations import save_output_to_file


def calculate_events_distribution_per_day(connection, user_id):
    print('Start query execution at ', datetime.now())

    get_distribution_events = SQL_QUERY_EVENTS_DISTRIBUTION

    if user_id:
        get_distribution_events += ''' and log_line #>> '{context, user_id}' = \'''' + user_id + '\''

    get_distribution_events += ''' group by time_run, event_name
        order by event_name'''

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(get_distribution_events)
    events_distribution = cursor.fetchall()
    cursor.close()
    connection.commit()

    print('End query execution at ', datetime.now())
    print("Events distribution per day has been calculated")
    return events_distribution


def generate_figure(event_distribution, user_id):
    events_dict = {}
    for event in event_distribution:
        event_name = event[0]
        dates = events_dict.get(event_name)
        if not dates:
            dates = []
        dates.append([event[1], event[2]])
        events_dict[event_name] = dates

    event_length = len(events_dict)
    row_count = event_length // 2 + event_length % 2
    fig = make_subplots(
        rows=row_count, cols=2,
        subplot_titles=(list(events_dict.keys())))

    count = 1
    for key, value in events_dict.items():
        x_axis = []
        y_axis = []
        for val in value:
            x_axis.append(val[0])
            y_axis.append(val[1])
        row_number = count // 2 + count % 2
        col_number = 2 - count % 2
        fig.add_trace(go.Scatter(x=x_axis, y=y_axis, name=key), row=row_number, col=col_number)
        count += 1

    title = "Course activity types, that usees performed, depending on date"
    if user_id:
        title = "User '" + user_id + "' activity types on course depending on day"

    fig.update_layout(height=count * 250, width=1500, title_text=title)
    fig.show()


def main():
    user_id = input("User id: ")
    connection = open_db_connection()
    events_distribution = calculate_events_distribution_per_day(connection, user_id)
    close_db_connection(connection)
    if user_id:
        result_file = user_id + '_user_type_activity_on_course.csv'
    else:
        result_file = "distribution_calculation.csv"
    save_output_to_file(result_file, events_distribution, ['event_name', 'time', 'count'])
    generate_figure(events_distribution, user_id)


if __name__ == '__main__':
    main()
