# Generated by Django 4.2.1 on 2024-05-10 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0002_studentschart_alter_sectionactivity_section_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdata',
            name='video_views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]