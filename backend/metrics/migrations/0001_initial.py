# Generated by Django 4.2.1 on 2024-05-09 12:40

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumQuestionChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PagesPopularityChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SectionActivityChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TaskComplexityChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TaskSummaryChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TextbookViewsChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VideoInteractionChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VideoPlayCountChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyActivityChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WordSearchChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WordSearchCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('search_count', models.PositiveIntegerField()),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.wordsearchchart')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyActivityCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('count', models.PositiveIntegerField()),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.weeklyactivitychart')),
            ],
        ),
        migrations.CreateModel(
            name='VideoSectionReport',
            fields=[
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='courses.course')),
                ('last_time_accessed', models.DateTimeField(default=datetime.datetime.now)),
                ('last_time_updated', models.DateTimeField(default=datetime.datetime.now)),
                ('report_state', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default='not_started', max_length=12)),
                ('error_code', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default=None, max_length=50, null=True)),
                ('video_interaction_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.videointeractionchart')),
                ('video_play_count_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.videoplaycountchart')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoPlayCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('count', models.PositiveIntegerField()),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.videoplaycountchart')),
            ],
        ),
        migrations.CreateModel(
            name='VideoInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_link', models.CharField(max_length=250)),
                ('views_count', models.PositiveIntegerField()),
                ('unique_students_count', models.PositiveIntegerField()),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.videointeractionchart')),
            ],
        ),
        migrations.CreateModel(
            name='TextbookViewsCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_name', models.CharField(max_length=200)),
                ('views_count', models.PositiveIntegerField()),
                ('unique_students_count', models.PositiveIntegerField()),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.textbookviewschart')),
            ],
        ),
        migrations.CreateModel(
            name='TextbookSectionReport',
            fields=[
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='courses.course')),
                ('last_time_accessed', models.DateTimeField(default=datetime.datetime.now)),
                ('last_time_updated', models.DateTimeField(default=datetime.datetime.now)),
                ('report_state', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default='not_started', max_length=12)),
                ('error_code', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default=None, max_length=50, null=True)),
                ('textbook_views_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.textbookviewschart')),
                ('word_search_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.wordsearchchart')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_count', models.CharField(choices=[('first', 'First attempt'), ('second', 'Second attempt'), ('more', 'Third attempt and more')])),
                ('percentage', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.tasksummarychart')),
            ],
        ),
        migrations.CreateModel(
            name='TaskSectionReport',
            fields=[
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='courses.course')),
                ('last_time_accessed', models.DateTimeField(default=datetime.datetime.now)),
                ('last_time_updated', models.DateTimeField(default=datetime.datetime.now)),
                ('report_state', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default='not_started', max_length=12)),
                ('error_code', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default=None, max_length=50, null=True)),
                ('task_complexity_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.taskcomplexitychart')),
                ('task_summary_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.tasksummarychart')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskComplexity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_link', models.CharField(max_length=250)),
                ('all_attempts', models.IntegerField()),
                ('successful_attempts', models.IntegerField()),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.taskcomplexitychart')),
            ],
        ),
        migrations.CreateModel(
            name='SectionActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(choices=[('common', 'common'), ('video', 'video'), ('pdf', 'pdf'), ('forum', 'forum'), ('pages', 'pages'), ('tasks', 'tasks')], max_length=10)),
                ('students_count', models.PositiveIntegerField(default=0)),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.sectionactivitychart')),
            ],
        ),
        migrations.CreateModel(
            name='PagesSectionReport',
            fields=[
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='courses.course')),
                ('last_time_accessed', models.DateTimeField(default=datetime.datetime.now)),
                ('last_time_updated', models.DateTimeField(default=datetime.datetime.now)),
                ('report_state', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default='not_started', max_length=12)),
                ('error_code', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default=None, max_length=50, null=True)),
                ('pages_popularity_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.pagespopularitychart')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PagesPopularity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_link', models.CharField(max_length=500)),
                ('visits_count', models.PositiveIntegerField()),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.pagespopularitychart')),
            ],
        ),
        migrations.CreateModel(
            name='ForumSectionReport',
            fields=[
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='courses.course')),
                ('last_time_accessed', models.DateTimeField(default=datetime.datetime.now)),
                ('last_time_updated', models.DateTimeField(default=datetime.datetime.now)),
                ('report_state', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default='not_started', max_length=12)),
                ('error_code', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default=None, max_length=50, null=True)),
                ('forum_question_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.forumquestionchart')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ForumQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField()),
                ('title', models.TextField(blank=True, default='')),
                ('body', models.TextField(blank=True, default='')),
                ('likes_count', models.PositiveIntegerField(default=0)),
                ('comments_count', models.PositiveIntegerField(default=0)),
                ('question_type', models.CharField(choices=[('thread', 'Thread'), ('response', 'Response')])),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='metrics.forumquestionchart')),
            ],
        ),
        migrations.CreateModel(
            name='CommonSectionReport',
            fields=[
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='courses.course')),
                ('last_time_accessed', models.DateTimeField(default=datetime.datetime.now)),
                ('last_time_updated', models.DateTimeField(default=datetime.datetime.now)),
                ('report_state', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default='not_started', max_length=12)),
                ('error_code', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('done', 'Created'), ('failed', 'Failed')], default=None, max_length=50, null=True)),
                ('students_count', models.PositiveIntegerField(default=None, null=True)),
                ('active_students_count', models.PositiveIntegerField(default=None, null=True)),
                ('section_activity_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.sectionactivitychart')),
                ('weekly_activity_chart', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.weeklyactivitychart')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
