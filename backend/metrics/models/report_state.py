
class ReportState:
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CREATED = "done"
    FAILED = "failed"
    CHOICES = [
        (NOT_STARTED, "Not started"),
        (IN_PROGRESS, "In progress"),
        (CREATED, "Created"),
        (FAILED, "Failed")
    ]
