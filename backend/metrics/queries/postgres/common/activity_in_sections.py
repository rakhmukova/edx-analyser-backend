from metrics.queries.postgres.sql_queries import SQL_QUERY_ACTIVITY_IN_SECTIONS

from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calc_activity_in_sections(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_ACTIVITY_IN_SECTIONS, course_id)

def main():
    calc_course_metric(
        calc_activity_in_sections,
        "common/activity_in_sections.csv",
        ['section_type', 'students_count']
    )


if __name__ == '__main__':
    main()
