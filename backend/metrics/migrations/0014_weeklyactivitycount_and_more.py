# Generated by Django 4.2.1 on 2024-04-15 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0013_alter_pagespopularity_page_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyActivityCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='commonsectionreport',
            old_name='completion_degree_chart',
            new_name='weekly_activity_chart',
        ),
        migrations.RenameModel(
            old_name='CompletionDegreeChart',
            new_name='WeeklyActivityChart',
        ),
        migrations.DeleteModel(
            name='CompletionDegree',
        ),
        migrations.AddField(
            model_name='weeklyactivitycount',
            name='chart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.weeklyactivitychart'),
        ),
    ]