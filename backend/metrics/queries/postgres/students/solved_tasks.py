from metrics.queries.postgres.sql_queries import SQL_QUERY_SOLVED_TASKS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calculate_total_user_time_on_course(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_SOLVED_TASKS, course_id)

def main():
    total_users_time_on_course = calc_course_metric(
        calculate_total_user_time_on_course,
        "students/solved_tasks.csv",
        ['username', 'number of solved tasks']
    )


if __name__ == '__main__':
    main()
