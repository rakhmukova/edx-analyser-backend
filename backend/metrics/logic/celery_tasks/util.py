from typing import Type, Any

from django.db.models import Model

from metrics.utils.file_operations import ColumnType, csv_to_json


def bulk_create_from_csv(
        csv_file_path: str,
        column_types: dict[str, Type[ColumnType]],
        model_class: Type[Model],
        chart_model_class: Type[Model]
) -> Any:
    chart = chart_model_class.objects.create()
    chart_objects_json = csv_to_json(csv_file_path,column_types)
    models = [model_class(**item, chart=chart) for item in chart_objects_json]
    model_class.objects.bulk_create(models)
    return chart
