# Generated by Django 4.2.1 on 2024-04-15 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0017_remove_commonsectionreport_error_reason_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonsectionreport',
            name='active_students_count',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
    ]