import plotly.graph_objects as go
from plotly.subplots import make_subplots

from metrics.queries.postgres.sql_queries import SQL_QUERY_PAGE_ACTIVITY_PER_DAY, SQL_QUERY_URLS_AND_NAMES_MAPPING
from metrics.utils.db_operations import close_db_connection, open_db_connection, execute_query_with_result
from metrics.utils.file_operations import find_alias, save_output_to_file
from metrics.utils.url_operations import remove_parameters_from_url


def calculate_page_activity_per_day(connection):
    return execute_query_with_result(connection, SQL_QUERY_PAGE_ACTIVITY_PER_DAY)


def calculate_urls_and_names_mapping(connection):
    return execute_query_with_result(connection, SQL_QUERY_URLS_AND_NAMES_MAPPING)


def process_urls(result):
    page_activity_per_day_clean = {}
    for item in result:
        url = remove_parameters_from_url(item[0])
        dates = page_activity_per_day_clean.get(url)
        if not dates:
            dates = {}

        interaction_count = dates.get(item[1])
        if not interaction_count:
            interaction_count = 0

        interaction_count += item[2]
        dates[item[1]] = interaction_count

        page_activity_per_day_clean[url] = dates

    return page_activity_per_day_clean


def generate_figure(page_activity_per_day, urls_and_names_mapping):
    titles = []
    for key in page_activity_per_day.keys():
        alias = find_alias(key, urls_and_names_mapping)
        if alias:
            titles.append(alias + " <br>" + key + "</br>")
        else:
            titles.append(key)

    pages_length = len(page_activity_per_day)
    row_count = pages_length
    fig = make_subplots(
        rows=row_count,
        cols=1,
        subplot_titles=titles)

    count = 1
    for key, value in page_activity_per_day.items():
        x_axis = []
        y_axis = []
        for date in sorted(value.keys()):
            x_axis.append(date)
            y_axis.append(value.get(date))
        row_number = count
        col_number = 1
        fig.add_trace(go.Scatter(x=x_axis, y=y_axis, name=key), row=row_number, col=col_number)
        count += 1

    fig.update_layout(
        height=count * 250,
        width=2500,
        title_text="Page activity on course distributed by day.")
    fig.show()


def main():
    connection = open_db_connection()
    page_activity_per_day = calculate_page_activity_per_day(connection)
    clean_page_activity_per_day = process_urls(page_activity_per_day)
    urls_and_names_mapping = calculate_urls_and_names_mapping(connection)
    result_file = "distributed_by_day_visits_course_page_activity.csv"
    save_output_to_file(result_file, clean_page_activity_per_day, [''])
    generate_figure(clean_page_activity_per_day, urls_and_names_mapping)
    close_db_connection(connection)


if __name__ == '__main__':
    main()
