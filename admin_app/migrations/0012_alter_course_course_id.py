# Generated by Django 5.1.1 on 2024-09-30 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0011_course_course_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.CharField(default='COURSE000', max_length=8),
        ),
    ]