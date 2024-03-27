import plotly.graph_objects as go
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from metrics.sql_queries import SQL_QUERY_USER_TIME_ON_COURSE_PER_DAY
from metrics.utils.db_operations import execute_user_query_with_result
from metrics.utils.metric_operations import calc_user_metric


def calculate_user_session_activity_per_day_on_course(connection, user_id):
    return execute_user_query_with_result(
        connection,
        SQL_QUERY_USER_TIME_ON_COURSE_PER_DAY,
        user_id,
        ISOLATION_LEVEL_AUTOCOMMIT
    )


def generate_user_time_distribution_per_day_figure(user_time_on_course_per_day):
    total_time = 0
    user_id = ''
    x_axis = []
    y_axis = []

    for duration in user_time_on_course_per_day:
        user_id = duration[0]
        x_axis.append(duration[1])
        y_axis.append(duration[2].total_seconds() / (60 * 60))
        total_time += duration[2].total_seconds() / (60 * 60)

    fig = go.Figure(data=go.Scatter(x=x_axis, y=y_axis))

    fig.update_layout(
        height=500,
        width=2000,
        title_text="User with id '" + user_id + "' time on course distributed per day. "
                                                "Total time spent '" + str(total_time) + "' hours.",
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Date",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Time in hours",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        ))

    fig.show()


def main():
    user_id = input("User id: ")
    user_time_on_course_per_day = calc_user_metric(
        calculate_user_session_activity_per_day_on_course,
        "user_time_on_course.csv",
        ['user_id', 'session_date', 'time_at_session_per_day'],
        user_id
    )
    generate_user_time_distribution_per_day_figure(user_time_on_course_per_day)


if __name__ == '__main__':
    main()
