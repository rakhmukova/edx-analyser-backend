from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.tasks import TaskComplexityChart, TaskComplexity, TaskSummary, TaskSummaryChart


def create_task_complexity_chart(course_id: str) -> TaskComplexityChart:
    return bulk_create_from_csv(
        f'metric_results/{course_id}/tasks/problems_complexity.csv',
        {
            'problem_link': str,
            'all_attempts': int,
            'successful_attempts': int,
            'question': str,
        },
        TaskComplexity,
        TaskComplexityChart
    )


def create_task_summary_chart(course_id: str) -> TaskSummaryChart:
    return bulk_create_from_csv(
        f'metric_results/{course_id}/tasks/problems_summary.csv',
        {
            'attempt_count': str,
            'percentage': int,
        },
        TaskSummary,
        TaskSummaryChart
    )
