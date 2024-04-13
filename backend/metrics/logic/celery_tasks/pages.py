from metrics.models.pages import PagesPopularityChart
from metrics.queries.postgres.pages.course_pages_popularity import calc_course_pages_popularity
from metrics.utils.metric_operations import calc_course_metric


def create_pages_popularity_chart(course_id: str) -> PagesPopularityChart:
    pages_popularity_chart = PagesPopularityChart.objects.create()
    result = calc_course_metric(
        calc_course_pages_popularity,
        "course_pages_popularity.csv",
        ['page_link', 'visits_count']
    )
    return pages_popularity_chart