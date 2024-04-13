from metrics.logic.celery_tasks.util import bulk_create_from_csv
from metrics.models.forum import ForumQuestion, ForumQuestionChart, QuestionType


def create_forum_question_chart(course_id: str) -> ForumQuestionChart:
    return bulk_create_from_csv(
        'metric_results/existing/forum/top_threads.csv',
        {
            'author': str,
            'title': str,
            'body': str,
            'likes_count': str,
            'comments_count': str,
            'question_type': str
        },
        ForumQuestion,
        ForumQuestionChart
    )
