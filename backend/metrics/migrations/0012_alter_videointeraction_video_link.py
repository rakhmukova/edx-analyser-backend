# Generated by Django 4.2.1 on 2024-04-13 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0011_alter_pagespopularity_chart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videointeraction',
            name='video_link',
            field=models.CharField(max_length=250),
        ),
    ]