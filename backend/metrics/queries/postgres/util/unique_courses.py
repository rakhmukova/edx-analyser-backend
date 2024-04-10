from metrics.queries.postgres.sql_queries import SQL_QUERY_UNIQUE_COURSES
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric
import time

def unique_courses(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_UNIQUE_COURSES, course_id)


def main():
    result_file = "unique_courses.csv"
    fields = ['course_id', 'count']
    start_time = time.time()
    calc_course_metric(
        unique_courses,
        result_file,
        fields
    )
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")


if __name__ == '__main__':
    main()