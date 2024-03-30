import csv
import os
from dataclasses import dataclass

from dotenv import load_dotenv

import pytest as pytest

from metrics.queries.postgres.course_activity.completed_course_users import calculate_users_who_finished_the_course
from metrics.queries.postgres.course_activity.enrolled_users_without_activity import \
    calculate_users_who_enrolled_but_not_started
from metrics.queries.postgres.course_activity.started_but_not_completed_users import \
    calculate_users_who_started_but_not_completed
from metrics.queries.postgres.course_activity.time_on_course import calculate_total_user_time_on_course
# from backend.postgres.decompress_zst import decompress_log_archives
from metrics.queries.postgres.upload_logs_postgresql import upload_logs_postgres
from metrics.queries.postgres.user_specific.user_time_on_course import calculate_user_session_activity_per_day_on_course
from metrics.utils.db_operations import open_db_connection, close_db_connection, create_database_if_not_exists
from metrics.utils.file_operations import save_output_to_file
from metrics.utils.metric_operations import MetricFuncType, DEFAULT_COURSE_ID, UserMetricFuncType

EXPECTED_PATH = "result_files/expected/"
ACTUAL_PATH = "result_files/actual/"

load_dotenv()


@dataclass
class MetricData:
    metric_func: MetricFuncType
    result_file: str
    fields: list[str]


@dataclass
class UserMetricData:
    metric_func: UserMetricFuncType
    result_file: str
    fields: list[str]


@pytest.fixture(scope="session", autouse=True)
def setup_complete():
    # фиксируем состояние тестовой базы данных
    # decompress_log_archives()
    # create_database_if_not_exists(os.getenv("POSTGRES_TESTING_DATABASE"))
    # upload_logs_postgres(database=os.getenv("POSTGRES_TESTING_DATABASE"), logs_dir='../backend/log_files/DATANTECH2035/')
    yield


@pytest.fixture
def course_metrics():
    return [
        MetricData(calculate_users_who_finished_the_course, "completed_course_users.csv", ['user_id', 'username']),
        MetricData(calculate_users_who_enrolled_but_not_started, "enrolled_users_without_activity.csv",
         ['user_id', 'username', 'enrollment_date']),
        MetricData(calculate_users_who_started_but_not_completed, "started_but_not_completed_course.csv",
         ['user_id', 'username']),
        MetricData(calculate_total_user_time_on_course, "distinct_user_time_on_course.csv", ['user_id', 'time_on_course']),
    ]


@pytest.fixture
def specific_student_metrics():
    return [
        (calculate_user_session_activity_per_day_on_course, "user_time_on_course.csv",
         ['user_id', 'session_date', 'time_at_session_per_day'])
    ]


@pytest.fixture
def specific_student_id():
    return "2683038"


def assert_csv_equality(expected, actual):
    with open(expected, 'r', newline='') as f1, open(actual, 'r', newline='') as f2:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)

        size1 = sum(1 for _ in reader1)
        size2 = sum(1 for _ in reader2)

        assert size1 == size2, f"Number of rows is not equal: {size1} != {size2}"

        for row1, row2 in zip(reader1, reader2):
            assert row1 == row2, f"Rows not equal: {row1}, {row2}"


def test_metrics(course_metrics: list[MetricData], specific_student_metrics: list[UserMetricData], specific_student_id):
    connection = open_db_connection(database=os.environ.get("POSTGRES_TESTING_DATABASE"))
    course_id = DEFAULT_COURSE_ID
    for metric in course_metrics:
        metric_result = metric.metric_func(connection, course_id)
        save_output_to_file(metric.result_file, metric_result, metric.fields, result_path=ACTUAL_PATH)

    for metric in specific_student_metrics:
        metric_result = metric.metric_func(connection, specific_student_id, course_id)
        save_output_to_file(f"{specific_student_id}_{metric.result_file}", metric_result, metric.fields,
                            result_path=ACTUAL_PATH)

    close_db_connection(connection)

    result_files = map(lambda x: x[1], course_metrics)
    for file in result_files:
        assert_csv_equality(EXPECTED_PATH + file, ACTUAL_PATH + file)
