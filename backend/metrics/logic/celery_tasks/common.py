from metrics.models.common import CompletionDegreeChart, SessionTimeChart, SectionActivityChart, CompletionDegree, \
    SessionTime, SectionActivity
from metrics.utils.file_operations import csv_to_json


# todo: get rid of copy paste
def create_completion_degree_chart(course_id: str) -> CompletionDegreeChart:
    chart = CompletionDegreeChart.objects.create()
    chart_objects_json = csv_to_json(
        'metric_results/generated/completion_status_count.csv',
        {
            'completion_degree': str,
            'students_count': int
        })

    models = [CompletionDegree(**item, chart=chart) for item in chart_objects_json]
    CompletionDegree.objects.bulk_create(models)
    return chart

def create_session_time_chart(course_id: str) -> SessionTimeChart:
    chart = SessionTimeChart.objects.create()
    chart_objects_json = csv_to_json(
        'metric_results/generated/session_average_time.csv',
        {
            'session_type': str,
            'average_time': int
        })

    models = [SessionTime(**item, chart=chart) for item in chart_objects_json]
    SessionTime.objects.bulk_create(models)
    return chart

def create_section_activity_chart(course_id: str) -> SectionActivityChart:
    chart = SectionActivityChart.objects.create()
    chart_objects_json = csv_to_json(
        'metric_results/generated/section_activity_students_percent.csv',
        {
            'section_type': str,
            'students_percent': int
        })

    models = [SectionActivity(**item, chart=chart) for item in chart_objects_json]
    SectionActivity.objects.bulk_create(models)
    return chart
