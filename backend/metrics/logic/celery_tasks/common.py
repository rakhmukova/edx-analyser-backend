from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.common import CompletionDegreeChart, SessionTimeChart, SectionActivityChart, CompletionDegree, \
    SessionTime, SectionActivity


def create_completion_degree_chart(course_id: str) -> CompletionDegreeChart:
    return bulk_create_from_csv(
        'metric_results/generated/completion_status_count.csv',
        {
            'completion_degree': str,
            'students_count': int
        },
        CompletionDegree,
        CompletionDegreeChart
    )

def create_session_time_chart(course_id: str) -> SessionTimeChart:
    return bulk_create_from_csv(
        'metric_results/generated/session_average_time.csv',
        {
            'session_type': str,
            'average_time': int
        },
        SessionTime,
        SessionTimeChart
    )

def create_section_activity_chart(course_id: str) -> SectionActivityChart:
    return bulk_create_from_csv(
        'metric_results/generated/section_activity_students_percent.csv',
        {
            'section_type': str,
            'students_percent': int
        },
        SectionActivity,
        SectionActivityChart
    )
