from datetime import datetime
from venv import logger

from courses.models import Course
from metrics.logic.celery_tasks.generate_report import generate_report, report_cls_by_section_type
from metrics.models.report import SectionReport
from metrics.models.section_type import SectionType


def get_report(course_id: str, user_id: int, section_type: SectionType, force_update: bool = False) -> SectionReport:
    report = _get_existing_report(course_id, user_id, section_type)
    if report is not None:
        report.last_time_accessed = datetime.now()
        report.save()
        logger.info(f"Existing report found {course_id} {section_type}")
        if force_update:
            logger.info(f"Updating report {course_id} {section_type}")
            generate_report.delay(course_id, user_id, section_type)
        return report

    logger.info(f"Generating new report {course_id} {section_type}")
    report = _create_empty_report(course_id, user_id, section_type)
    generate_report.delay(course_id, user_id, section_type)
    return report


def _get_existing_report(course_id: str, user_id: int, section_type: SectionType) -> SectionReport:
    course = Course.objects.available_courses(user_id).filter(course_id=course_id).first()
    return report_cls_by_section_type[section_type].objects.filter(course=course).first()


def _create_empty_report(course_id: str, user_id: int, section_type: SectionType) -> SectionReport:
    course = Course.objects.available_courses(user_id).filter(course_id=course_id).first()
    logger.info("Assigning task to generate report")
    return report_cls_by_section_type[section_type].objects.create(course=course)
