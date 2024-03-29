import plotly.graph_objects as go

from postgres.sql_queries import SQL_QUERY_ENROLLED_USERS_WITHOUT_ACTIVITY
from postgres.utils.db_operations import execute_query_with_result
from postgres.utils.metric_operations import calc_course_metric


def calculate_users_who_enrolled_but_not_started(connection):
    return execute_query_with_result(connection, SQL_QUERY_ENROLLED_USERS_WITHOUT_ACTIVITY)


def generate_figure(users):
    # for every date calculate count
    date_count = {}
    for user in users:
        if user[1]:
            count_for_date = date_count.get(user[2])
            if not count_for_date:
                date_count[user[2]] = 1
            else:
                count_for_date += 1
                date_count[user[2]] = count_for_date

    total_user_count = 0
    x_axis = []
    y_axis = []
    for key in sorted(date_count.keys()):
        total_user_count += date_count[key]
        x_axis.append(key)
        y_axis.append(date_count[key])

    fig = go.Figure(data=go.Scatter(x=x_axis, y=y_axis))

    fig.update_layout(
        height=500,
        width=2000,
        title_text="Distribution of users, who enrolled, but not started the course, "
                   "depending on the enrolment date. Total users: " + str(total_user_count),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="User enrolment date",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Amount of enrolments",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        )
    )

    fig.show()


if __name__ == '__main__':
    enrolled_but_not_started_users = calc_course_metric(
        calculate_users_who_enrolled_but_not_started,
        "enrolled_users_without_activity.csv",
        ['user_id', 'username', 'enrollment_date']
    )
    generate_figure(enrolled_but_not_started_users)
