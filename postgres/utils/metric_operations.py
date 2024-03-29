from postgres.utils.db_operations import close_db_connection, open_db_connection
from postgres.utils.file_operations import save_output_to_file


def calc_course_metric(metric, result_file, fields):
    # TODO: pass course_id
    connection = open_db_connection()
    metric_result = metric(connection)
    close_db_connection(connection)
    save_output_to_file(result_file, metric_result, fields)
    return metric_result


def calc_user_metric(metric, result_file, fields, user_id):
    connection = open_db_connection()
    metric_result = metric(connection, user_id)
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
