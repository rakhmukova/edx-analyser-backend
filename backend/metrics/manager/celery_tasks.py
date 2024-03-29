from celery import shared_task

# открывать соединение каждый раз или нет


@shared_task
def calc_metric(logs_connection, reports_connection, metric_func):
    result = metric_func(logs_connection)
    # report_connection
#     save to the database with reports?

