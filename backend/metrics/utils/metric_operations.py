from typing import Callable, Any

import psycopg2

from metrics.utils.db_operations import close_db_connection, open_db_connection
from metrics.utils.file_operations import save_output_to_file

DEFAULT_COURSE_ID = "course-v1:ITMOUniversity+DATANTECH2035+summer_2022_1"


MetricFuncType = Callable[[psycopg2.extensions.connection, str], Any]
UserMetricFuncType = Callable[[psycopg2.extensions.connection, str, str], Any]


def calc_course_metric(metric: MetricFuncType, result_file: str, fields: list[str],
                       course_id: str = DEFAULT_COURSE_ID):
    connection = open_db_connection()
    metric_result = metric(connection, course_id)
    close_db_connection(connection)
    save_output_to_file(result_file, metric_result, fields)
    return metric_result


def calc_user_metric(metric: UserMetricFuncType, result_file: str, fields: list[str], user_id: str,
                     course_id: str = DEFAULT_COURSE_ID):
    connection = open_db_connection()
    metric_result = metric(connection, user_id, course_id)
    close_db_connection(connection)
    save_output_to_file(f"{user_id}_{result_file}", metric_result, fields)
    return metric_result


def calc_metrics(metrics):
    connection = open_db_connection()
    for metric in metrics:
        metric_func, result_file, fields = metric
        metric_result = metric_func(connection)
        save_output_to_file(result_file, metric_result, fields)
    close_db_connection(connection)
