import plotly.graph_objects as go

from postgres.sql_queries import SQL_QUERY_TOTAL_USER_TIME_ON_COURSE
from postgres.utils.db_operations import execute_query_with_result
from postgres.utils.metric_operations import calc_course_metric


def calculate_total_user_time_on_course(connection):
    return execute_query_with_result(connection, SQL_QUERY_TOTAL_USER_TIME_ON_COURSE)


def generate_total_time_distribution_figure(user_time_on_course):
    index = 1
    x_axis = []
    y_axis = []

    for duration in user_time_on_course:
        x_axis.append(index)
        y_axis.append(duration[1].total_seconds() / (60 * 60))
        index += 1

    fig = go.Figure(data=go.Scatter(x=x_axis, y=y_axis))

    fig.update_layout(
        height=500,
        width=2000,
        title_text="User time on course.",
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="User order number",
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
    total_users_time_on_course = calc_course_metric(
        calculate_total_user_time_on_course,
        "distinct_user_time_on_course.csv",
        ['user_id', 'time_on_course']
    )
    generate_total_time_distribution_figure(total_users_time_on_course)


if __name__ == '__main__':
    main()
