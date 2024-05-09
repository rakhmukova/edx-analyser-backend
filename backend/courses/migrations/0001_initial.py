# Generated by Django 4.2.1 on 2024-05-09 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=150)),
                ('name', models.TextField()),
                ('image_url', models.TextField(null=True)),
                ('short_name', models.TextField()),
                ('visibility', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Private')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('owner', 'course_id')},
            },
        ),
    ]
