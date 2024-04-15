from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.common import SectionActivityChart, \
    SectionActivity, WeeklyActivityChart, WeeklyActivityCount


def create_section_activity_chart(course_id: str) -> SectionActivityChart:
    return bulk_create_from_csv(
        'metric_results/generated/section_activity_students_percent.csv',
        {
            'section_type': str,
            'students_count': int
        },
        SectionActivity,
        SectionActivityChart
    )


def create_weekly_activity_chart(course_id: str) -> WeeklyActivityChart:
    return bulk_create_from_csv(
        'metric_results/existing/common/weekly_active_users.csv',
        {
            'date': str,
            'count': int
        },
        WeeklyActivityCount,
        WeeklyActivityChart
    )
