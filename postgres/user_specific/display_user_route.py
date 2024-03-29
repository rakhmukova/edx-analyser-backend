import plotly.graph_objects as go

from postgres.sql_queries import SQL_QUERY_USER_ROUTE, USER_PAGES_VISITED_AT_TIMEDATE
from postgres.utils.db_operations import open_db_connection, close_db_connection, execute_user_query_with_result, \
    execute_query_with_result
from postgres.utils.file_operations import find_alias, save_output_to_file
from postgres.utils.url_operations import remove_parameters_from_url


def calculate_user_way_of_moving(connection, user_id):
    return execute_user_query_with_result(connection, USER_PAGES_VISITED_AT_TIMEDATE, user_id)


def calculate_urls_and_names_mapping(connection):
    return execute_query_with_result(connection, SQL_QUERY_USER_ROUTE)


def generate_figure(user_way_on_course, urls_and_names_mapping, user_id):
    x_axis = []
    y_axis = []

    y_ticktext = []
    for user in user_way_on_course:
        if user[0]:
            x_axis.append(user[0])
            cleaned_url = remove_parameters_from_url(user[1])
            y_axis.append(cleaned_url)

            alias = find_alias(cleaned_url, urls_and_names_mapping)
            if alias:
                y_ticktext.append(alias)
            else:
                y_ticktext.append(cleaned_url)

    fig = go.Figure(data=go.Scatter(x=x_axis, y=y_axis, line=dict(width=5, color='#b22222'),
                                    mode='lines+markers',
                                    marker_size=15))

    fig.update_layout(
        height=1000,
        width=10000,
        title_text="Way of moving on course per day of the user with id '" + str(user_id) + "'",
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Date of moving",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            ),
            tickmode='array'
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Page URL",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        )
    )

    fig.update_yaxes(
        ticktext=y_ticktext,
        tickvals=y_axis
    )

    fig.show()


def main():
    user_id = input("User id: ")
    connection = open_db_connection()
    user_way_on_course = calculate_user_way_of_moving(connection, user_id)
    urls_and_names_mapping = calculate_urls_and_names_mapping(connection)
    result_file = f"{user_id}_display_user_route.csv"
    save_output_to_file(result_file, user_way_on_course, ['time_access', 'page_url'])
    generate_figure(user_way_on_course, urls_and_names_mapping, user_id)
    close_db_connection(connection)


if __name__ == '__main__':
    main()
