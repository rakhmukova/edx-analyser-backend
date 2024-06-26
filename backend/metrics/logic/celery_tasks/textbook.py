from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.textbook import TextbookViewsCount, WordSearchChart, WordSearchCount, TextbookViewsChart


def create_word_search_chart(course_id: str) -> WordSearchChart:
    return bulk_create_from_csv(
        f'metric_results/{course_id}/textbook/searched_pdf_terms.csv',
        {
            'word': str,
            'search_count': int,
        },
        WordSearchCount,
        WordSearchChart
    )

def create_textbook_views_chart(course_id: str) -> TextbookViewsCount:
    return bulk_create_from_csv(
        f'metric_results/{course_id}/textbook/scrolling_time.csv',
        {
            'pdf_name': str,
            'views_count': int,
            'unique_students_count': int
        },
        TextbookViewsCount,
        TextbookViewsChart
    )
