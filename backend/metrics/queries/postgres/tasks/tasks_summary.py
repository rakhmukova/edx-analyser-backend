from collections import defaultdict
from metrics.queries.postgres.sql_queries import SQL_QUERY_TASKS_SUMMARY
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calculate_total_user_time_on_course(connection, course_id):
    data = execute_query_with_result(connection, SQL_QUERY_TASKS_SUMMARY, course_id)
    attempts_count = calculate_average_attempts(data)
    return analyze_attempts_data(attempts_count)


def calculate_average_attempts(data: list[tuple[str, int]]):
    attempts_count = defaultdict(list)
    for task_id, attempt_str in data:
        attempt = int(attempt_str)
        attempts_count[task_id].append(attempt)

    # Добавляем расчет среднего значения и округляем его до ближайшего целого
    for task_id, attempts in attempts_count.items():
        if attempts:
            average_attempt = round(sum(attempts) / len(attempts))
            attempts_count[task_id] = average_attempt

    return attempts_count


def analyze_attempts_data(attempts_count: dict[str, int]):
    first_attempt_count = 0
    second_attempt_count = 0
    other_attempt_count = 0

    # Считаем количество задач, решенных с первой, второй и последующими попытками
    for attempts in attempts_count.values():

        if attempts == 1:
            first_attempt_count += 1
        elif attempts == 2:
            second_attempt_count += 1
        else:
            other_attempt_count += 1

    total_tasks = first_attempt_count + second_attempt_count + other_attempt_count
    print(first_attempt_count, second_attempt_count, other_attempt_count)
    # Вычисляем процент задач для каждой категории попыток
    percent_first_attempt = (first_attempt_count / total_tasks) * 100
    percent_second_attempt = (second_attempt_count / total_tasks) * 100
    percent_other_attempts = (other_attempt_count / total_tasks) * 100

    # Возвращаем результат в формате CSV
    return [
        ("first_attempt", percent_first_attempt),
        ("second_attempt", percent_second_attempt),
        ("other_attempts", percent_other_attempts)
    ]


def main():
    calc_course_metric(
        calculate_total_user_time_on_course,
        "tasks/problems_summary.csv",
        ['attempt_count', 'percent']
    )

if __name__ == '__main__':
    main()
