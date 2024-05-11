from metrics.queries.postgres.sql_queries import SQL_QUERY_ACTIVITY_IN_SECTIONS
from metrics.utils.db_operations import open_db_connection, close_db_connection
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.file_operations import DEFAULT_COURSE_ID
from metrics.utils.file_operations import save_output_to_file

def calc_activity_in_sections(connection, course_id):
    result = execute_query_with_result(connection, SQL_QUERY_ACTIVITY_IN_SECTIONS, (course_id,))
    activity_dict = {'forum': 0, 'textbook': 0, 'video': 0, 'problem': 0}

    for row in result:
        print(f"row={row}")
        section_type = row[0]
        print(f"section_type={section_type}")
        students_count = row[1]
        print(f"students_count={students_count}")
        activity_dict[section_type] = students_count

    for section_type in activity_dict:
        if activity_dict[section_type] == 0:
            activity_dict[section_type] = 0
    print(activity_dict)
    return activity_dict


def main():
    connection = open_db_connection()
    result_dict = calc_activity_in_sections(connection, course_id=DEFAULT_COURSE_ID)
    result_list = [(key, value) for key, value in result_dict.items()]
    headers = ['section_type', 'students_count']
    save_output_to_file("common/activity_in_sections.csv", result_list, headers)
    close_db_connection(connection)


if __name__ == '__main__':
    main()
