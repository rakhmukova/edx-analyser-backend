from metrics.models.report import SectionReport
from metrics.models.report_state import ReportState
from metrics.models.section_type import SectionType

from metrics.logic.celery_tasks import generate_report


class ReportManager:

    @staticmethod
    def get_report(course_id: str, section_type: SectionType, should_generate_report: bool = False) -> SectionReport:
        if not should_generate_report:
            report = ReportManager._get_existing_report(course_id, section_type)
            if report is not None:
                return report

        report = SectionReport.objects.create(
            course_id=course_id,
            section_type=section_type,
            report_state=ReportState.NOT_STARTED
        )

        print("Assigning task to generate report")
        generate_report.delay(course_id, section_type)
        return report

    @staticmethod
    def _get_existing_report(course_id: str, section_type: SectionType) -> SectionReport:
        return SectionReport.objects.filter(
            course_id=course_id,
            section_type=section_type,
        ).first()
