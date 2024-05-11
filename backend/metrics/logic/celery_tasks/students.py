from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.students import StudentsChart, StudentData


def create_students_chart(short_name: str) -> StudentsChart:
    return bulk_create_from_csv(
        f'metric_results/{short_name}/students/students.csv',
        {
            'username': str,
            'total_days': int,
            'total_hours': int,
            'textbook_views': int,
            'solved_tasks': int,
            'average_attempt_count': int,
            'forum_activity': int
        },
        StudentData,
        StudentsChart
    )