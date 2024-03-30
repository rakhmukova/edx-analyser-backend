from typing import Any

from app.celery import app
from metrics.models.report import SectionReport
from metrics.models.report_state import ReportState
from metrics.models.section_type import SectionType


@app.task(name="generate_report")
def generate_report(course_id: str, section_type: SectionType):
    #  add try-catch here
    report = SectionReport.objects.filter(
        course_id=course_id,
        section_type=section_type,
    ).first()

    if report is None:
        report = SectionReport(
            course_id=course_id,
            section_type=section_type,
            report_state=ReportState.IN_PROGRESS
        )
        report.save()

    try:
        print(f"Generating report for section {section_type}")
        report.report_state = ReportState.IN_PROGRESS
        report.save(update_fields=["report_state"])

        # потенциально долгая операция
        report_data = get_report_data(course_id, section_type)
        report.report_state = ReportState.CREATED
        report.report_data = report_data
        report.save(update_fields=["report_state", "report_data"])
    except Exception as e:
        print("Ошибка при создании отчета:", e)
        # potentially can have here error as well
        report.report_state = ReportState.FAILED
        report.save(update_fields=["report_state"])


def get_report_data(course_id: str, section_type: SectionType) -> Any:
    return {}
