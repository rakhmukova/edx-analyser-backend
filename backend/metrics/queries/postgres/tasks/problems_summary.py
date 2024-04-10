import csv
from collections import defaultdict

from metrics.queries.postgres.sql_queries import SQL_QUERY_PROBLEMS_SUMMARY
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric


def calculate_total_user_time_on_course(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_PROBLEMS_SUMMARY, course_id)


def read_csv_file(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем первую строку
        for row in reader:
            task_id = row[0]
            attempts = int(row[1])
            data.append((task_id, attempts))
    return data


def calculate_average_attempts(data):
    average_attempts = defaultdict(list)
    for task_id, attempts in data:
        average_attempts[task_id].append(attempts)
    return average_attempts


def write_average_attempts_to_csv(data, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for task_id, attempts_list in data.items():
            average = round(sum(attempts_list) / len(attempts_list))
            # print(task_id, average)
            writer.writerow([task_id, average])


def process_attempts_data(file):
    # Читаем данные из CSV файла
    data = read_csv_file(file)

    # Вычисляем и записываем среднее число попыток
    average_attempts = calculate_average_attempts(data)
    write_average_attempts_to_csv(average_attempts, file)


def analyze_attempts_data(input_file):
    attempts_count = defaultdict(int)
    with open(input_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            attempt = int(row[1])
            attempt = min(attempt, 3)
            attempts_count[attempt] += 1

    total_tasks = sum(attempts_count.values())
    solved_counts = defaultdict(int)
    for attempt, count in attempts_count.items():
        solved_counts[attempt] = (count / total_tasks) * 100

    print("Процент решенных задач с каждой попытки:")
    for attempt, percentage in sorted(solved_counts.items()):
        print(f"{attempt}-я попытка: {percentage:.2f}%")


def main():
    total_users_time_on_course = calc_course_metric(
        calculate_total_user_time_on_course,
        "problems_summary.csv",
        ['problem_id', 'attempt']
    )
    file_path = "../../../../metric_results/existing/problems_summary.csv"

    # Обработка данных и запись среднего числа попыток в файл
    process_attempts_data(file_path)

    # Анализ данных о попытках
    analyze_attempts_data(file_path)

if __name__ == '__main__':
    main()
