from metrics.queries.postgres.sql_queries import SQL_QUERY_TOP_RESPONSES
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calc_top_responses(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_TOP_RESPONSES, (course_id,course_id,course_id,))


def main():
    calc_course_metric(
        calc_top_responses,
        "forum/top_responses.csv",
        ['author', 'title', 'body', 'comments_count', 'likes_count', 'question_type']
    )


if __name__ == '__main__':
    main()
