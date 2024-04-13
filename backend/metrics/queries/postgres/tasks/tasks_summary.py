from collections import defaultdict

from metrics.queries.postgres.sql_queries import SQL_QUERY_PROBLEMS_SUMMARY
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


# TODO: CHECK AND FIX
def calculate_total_user_time_on_course(connection, course_id):
    data = execute_query_with_result(connection, SQL_QUERY_PROBLEMS_SUMMARY, course_id)
    print(data)
    attempts_count = calculate_average_attempts(data)
    print(attempts_count)
    return analyze_attempts_data(attempts_count)


def calculate_average_attempts(data: list[tuple[str, int]]):
    average_attempts = defaultdict(list)
    for task_id, min_attempt in data:
        average_attempts[task_id].append(min_attempt)
    return average_attempts


def analyze_attempts_data(attempts_count: dict[str, list[int]]):
    total_tasks = sum(attempts_count.values())
    solved_counts = defaultdict(int)
    for attempt, count in attempts_count.items():
        solved_counts[attempt] = (count / total_tasks) * 100

    return sorted(solved_counts.items())


def main():
    calc_course_metric(
        calculate_total_user_time_on_course,
        "tasks/problems_summary.csv",
        ['attempt_count', 'percent']
    )

if __name__ == '__main__':
    main()
