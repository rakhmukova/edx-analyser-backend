from typing import Type
from venv import logger

from app.celery import app
from metrics.logic.celery_tasks.common import create_completion_degree_chart, create_session_time_chart, \
    create_section_activity_chart
from metrics.logic.celery_tasks.pages import create_pages_popularity_chart
from metrics.logic.celery_tasks.video import create_video_interaction_chart, create_video_play_count_chart
from metrics.models.report import VideoSectionReport, CommonSectionReport, SectionReport, PagesSectionReport
from metrics.models.section_type import SectionType


def _create_common_section_report(course_id: str):
    completion_degree_chart = create_completion_degree_chart(course_id)
    session_time_chart = create_session_time_chart(course_id)
    section_activity_chart = create_section_activity_chart(course_id)
    report = CommonSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.completion_degree_chart = completion_degree_chart
    report.session_time_chart = session_time_chart
    report.section_activity_chart = section_activity_chart
    report.save()


def _create_video_section_report(course_id: str):
    video_play_count_chart = create_video_play_count_chart(course_id)
    video_interaction_chart = create_video_interaction_chart(course_id)
    report = VideoSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.video_play_count_chart = video_play_count_chart
    report.video_interaction_chart = video_interaction_chart
    report.save()

def _create_page_section_report(course_id: str):
    pages_popularity_chart = create_pages_popularity_chart(course_id)
    report = PagesSectionReport.objects.filter(
        course_id=course_id,
    ).first()
    report.pages_popularity_chart = pages_popularity_chart
    report.save()

create_func_by_section_type = {
    SectionType.COMMON: _create_common_section_report,
    SectionType.VIDEO: _create_video_section_report
}

report_cls_by_section_type: dict[SectionType, Type[SectionReport]] = {
    SectionType.VIDEO: VideoSectionReport,
    SectionType.COMMON: CommonSectionReport,
    SectionType.PAGES: PagesSectionReport
}

# potentially long operation - need to calc metrics and save them
def _create_report(course_id: str, section_type: SectionType) -> None:
    create_func_by_section_type[section_type](course_id)

@app.task(name="generate_report")
def generate_report(course_id: str, section_type: SectionType):
    try:
        logger.info(f"Generating report for section {section_type}")
        _create_report(course_id, section_type)
    except Exception as e:
        # can have this error as well
        logger.error("Ошибка при создании отчета:", e)
        report = report_cls_by_section_type[section_type].objects.filter(
            course_id = course_id
        ).first()
        # handle error
        # value too long for type character varying(100)
        report.error_reason = str(e)
        report.save()
