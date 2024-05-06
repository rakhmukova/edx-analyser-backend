from metrics.queries.postgres.sql_queries import SQL_QUERY_SEARCHED_PDF_TERMS
from metrics.utils.db_operations import execute_query_with_result
from metrics.utils.metric_operations import calc_course_metric
import pandas as pd

def process_search_pdf_terms_result(result):
    # Проверяем, есть ли результат
    if not result or len(result) <= 1:  # Проверяем, что результат не пустой или содержит только заголовок
        return [['word', 'search_count']]  # Возвращаем заголовок как пустой результат

    df = pd.DataFrame(result, columns=['word', 'search_count'])
    df['search_count'] = pd.to_numeric(df['search_count'])
    df = df.sort_values(by='word', ascending=False)
    updated_counts = {}

    def update_counts(row):
        word = row['word']
        count = row['search_count']
        if word in updated_counts:
            updated_counts[word] += count
        else:
            updated_counts[word] = count
        for key in list(updated_counts.keys()):
            if key != word and word in key:
                updated_counts[key] += count
                del updated_counts[word]
                break  # прерываем цикл, чтобы избежать повторного сравнения

    df.apply(update_counts, axis=1)

    # Преобразуем словарь обратно в список списков
    updated_list = [[word, count] for word, count in updated_counts.items()]

    # Сортируем результаты по убыванию счетчика
    updated_list.sort(key=lambda x: x[1], reverse=True)
    print(updated_list)
    return updated_list



def calc_search_pdf_terms(connection, course_id):
    return process_search_pdf_terms_result(execute_query_with_result(connection, SQL_QUERY_SEARCHED_PDF_TERMS, (course_id,)))


def main():
    result_file = "textbook/searched_pdf_terms.csv"
    fields = ['word', 'search_count']
    calc_course_metric(
        calc_search_pdf_terms,
        result_file,
        fields
    )


if __name__ == '__main__':
    main()
