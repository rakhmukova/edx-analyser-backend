# Generated by Django 4.2.1 on 2024-05-11 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0005_popularinterval'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskcomplexity',
            name='question',
        ),
    ]
