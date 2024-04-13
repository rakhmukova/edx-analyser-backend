from metrics.queries.postgres.sql_queries import SQL_QUERY_TOTAL_USER_TIME_ON_COURSE
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric
from datetime import datetime

def calculate_total_user_time_on_course(connection, course_id):
    return execute_query_with_result(connection, SQL_QUERY_TOTAL_USER_TIME_ON_COURSE, course_id)



def calculate_time_on_course():
    # Чтение файла и загрузка данных
    with open('../../../../metric_results/existing/students/time_on_course.csv', 'r') as file:
        next(file)
        lines = file.readlines()

    # Создание словаря для хранения сумм разностей времени для каждого пользователя
    user_time_diffs = {}

    # Перебор строк файла
    for line in lines:
        parts = line.strip().split(',')
        user_id = parts[0]
        start_time = datetime.strptime(parts[3], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(parts[4], '%Y-%m-%d %H:%M:%S')

        # Рассчитываем разность времени в секундах
        time_diff_seconds = (end_time - start_time).total_seconds()

        # Добавляем разность времени в секундах в словарь
        if user_id in user_time_diffs:
            user_time_diffs[user_id] += time_diff_seconds
        else:
            user_time_diffs[user_id] = time_diff_seconds

    # Сортировка пользователей по убыванию длительности
    sorted_users = sorted(user_time_diffs.items(), key=lambda x: x[1], reverse=True)

    # Вывод отсортированных пользователей и их длительности
    for user_id, total_time_diff_seconds in sorted_users:
        total_hours = int(total_time_diff_seconds // 3600)  # Количество часов
        total_minutes = int((total_time_diff_seconds % 3600) // 60)  # Оставшиеся минуты
        print(f"Пользователь {user_id}: {total_hours} часов {total_minutes} минут")




def main():
    total_users_time_on_course = calc_course_metric(
        calculate_total_user_time_on_course,
        "students/time_on_course.csv",
        ['username', 'total time on course']
    )
    calculate_time_on_course()


if __name__ == '__main__':
    main()
