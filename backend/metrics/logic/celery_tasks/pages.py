from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.pages import PagesPopularityChart, PagesPopularity


def create_pages_popularity_chart(course_id: str) -> PagesPopularityChart:
    # result = calc_course_metric(
    #     calc_course_pages_popularity,
    #     "course_pages_popularity.csv",
    #     ['page_link', 'visits_count']
    # )
    return bulk_create_from_csv(
        'metric_results/existing/pages/course_pages_popularity.csv',
        {
            'page_link': str,
            'visits_count': int,
        },
        PagesPopularity,
        PagesPopularityChart
    )
