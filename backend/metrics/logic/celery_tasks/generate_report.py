from typing import Type, Callable
from venv import logger

from app.celery import app
from courses.models import Course
from metrics.logic.celery_tasks.common import \
    create_section_activity_chart, create_weekly_activity_chart
from metrics.logic.celery_tasks.forum import create_forum_question_chart
from metrics.logic.celery_tasks.pages import create_pages_popularity_chart
from metrics.logic.celery_tasks.tasks import create_task_complexity_chart, create_task_summary_chart
from metrics.logic.celery_tasks.textbook import create_word_search_chart, create_textbook_views_chart
from metrics.logic.celery_tasks.video import create_video_interaction_chart, create_video_play_count_chart
from metrics.models.report import VideoSectionReport, CommonSectionReport, SectionReport, PagesSectionReport, \
    TaskSectionReport, TextbookSectionReport, ForumSectionReport
from metrics.models.section_type import SectionType
from metrics.utils.file_operations import get_single_value_from_csv

report_cls_by_section_type: dict[SectionType, Type[SectionReport]] = {
    SectionType.VIDEO: VideoSectionReport,
    SectionType.COMMON: CommonSectionReport,
    SectionType.PAGES: PagesSectionReport,
    SectionType.TASKS: TaskSectionReport,
    SectionType.PDF: TextbookSectionReport,
    SectionType.FORUM: ForumSectionReport
}


def _create_common_section_report(course_id: str, short_name: str):
    section_activity_chart = create_section_activity_chart(short_name)
    weekly_activity_chart = create_weekly_activity_chart(short_name)
    students_count = get_single_value_from_csv(f'./metric_results/{short_name}/common/students_count.csv')
    active_students_count = get_single_value_from_csv(f'./metric_results/{short_name}/common/active_students_count.csv')
    report = CommonSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.section_activity_chart = section_activity_chart
    report.weekly_activity_chart = weekly_activity_chart
    report.students_count = students_count
    report.active_students_count = active_students_count
    report.save()


def _create_video_section_report(course_id: str, short_name: str):
    video_play_count_chart = create_video_play_count_chart(short_name)
    video_interaction_chart = create_video_interaction_chart(short_name)
    report = VideoSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.video_play_count_chart = video_play_count_chart
    report.video_interaction_chart = video_interaction_chart
    report.save()


def _create_page_section_report(course_id: str, short_name: str):
    pages_popularity_chart = create_pages_popularity_chart(short_name)
    report = PagesSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.pages_popularity_chart = pages_popularity_chart
    report.save()


def _create_textbook_section_report(course_id: str, short_name: str):
    textbook_views_chart = create_textbook_views_chart(short_name)
    word_search_chart = create_word_search_chart(short_name)
    report = TextbookSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.word_search_chart = word_search_chart
    report.textbook_views_chart = textbook_views_chart
    report.save()


def _create_forum_section_report(course_id: str, short_name: str):
    forum_question_chart = create_forum_question_chart(short_name)
    report = ForumSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.forum_question_chart = forum_question_chart
    report.save()


def _create_task_section_report(course_id: str, short_name: str):
    task_complexity_chart = create_task_complexity_chart(short_name)
    task_summary_chart = create_task_summary_chart(short_name)
    report = TaskSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.task_complexity_chart = task_complexity_chart
    report.task_summary_chart = task_summary_chart
    report.save()


create_func_by_section_type: dict[SectionType, Callable[[str, str], None]] = {
    SectionType.COMMON: _create_common_section_report,
    SectionType.VIDEO: _create_video_section_report,
    SectionType.PAGES: _create_page_section_report,
    SectionType.PDF: _create_textbook_section_report,
    SectionType.TASKS: _create_task_section_report,
    SectionType.FORUM: _create_forum_section_report
}


# potentially long operation - need to calc metrics and save them
def _create_report(course_id: str, section_type: SectionType) -> None:
    short_name = Course.objects.get(course_id=course_id).short_name
    create_func_by_section_type[section_type](course_id, short_name)


@app.task(name="generate_report")
def generate_report(course_id: str, section_type: SectionType):
    try:
        logger.info(f"Generating report for section {section_type}")
        _create_report(course_id, section_type)
    except Exception as e:
        # can have this error as well
        logger.error("Ошибка при создании отчета:", e)
        report = report_cls_by_section_type[section_type].objects.filter(
            course_id=course_id
        ).first()
        # handle error
        # value too long for type character varying(100)
        # report.error_reason = str(e)
        report.save()
