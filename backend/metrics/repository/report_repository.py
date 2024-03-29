from metrics.models.report import CourseReport


class ReportRepository:
    # automatic generation?
    def add(self, report: CourseReport):
        pass

    def update(self, course_id):
        pass

    def get(self, course_id) -> CourseReport:
        pass
