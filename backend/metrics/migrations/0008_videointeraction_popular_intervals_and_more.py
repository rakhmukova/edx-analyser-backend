# Generated by Django 4.2.1 on 2024-05-13 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0007_taskcomplexity_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='videointeraction',
            name='popular_intervals',
            field=models.CharField(default=''),
        ),
        migrations.DeleteModel(
            name='PopularInterval',
        ),
    ]
