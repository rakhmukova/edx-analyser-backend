from metrics.queries.postgres.sql_queries import SQL_QUERY_TOTAL_USER_TIME_ON_COURSE
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calc_time_on_course(connection, course_id):
    result = execute_query_with_result(connection, SQL_QUERY_TOTAL_USER_TIME_ON_COURSE, course_id)
    return calculate_time_on_course(result)

def calculate_time_on_course(user_sessions):
    user_time_diffs = {}

    for session in user_sessions:
        username,_,_,start_time,end_time = session
        time_diff_seconds = int((end_time - start_time).total_seconds())
        if username in user_time_diffs:
            user_time_diffs[username] += time_diff_seconds
        else:
            user_time_diffs[username] = time_diff_seconds

    sorted_users = sorted(user_time_diffs.items(), key=lambda x: x[1], reverse=True)
    return sorted_users


def main():
    calc_course_metric(
        calc_time_on_course,
        "students/time_on_course.csv",
        ['username', 'time_on_course']
    )


if __name__ == '__main__':
    main()
