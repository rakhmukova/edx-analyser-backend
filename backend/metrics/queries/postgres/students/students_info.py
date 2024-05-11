from metrics.queries.postgres.sql_queries import SQL_QUERY_STUDENTS_INFO
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calculate_total_user_time_on_course(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_STUDENTS_INFO,
                                     (course_id, course_id, course_id, course_id, course_id,))


def main():
    calc_course_metric(
        calculate_total_user_time_on_course,
        "students/students.csv",
        ['username', 'total_days', 'video_views', 'textbook_views', 'solved_tasks', 'forum_activity']
    )


if __name__ == '__main__':
    main()
