# Generated by Django 5.1 on 2024-09-25 17:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='users',
        ),
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.PositiveIntegerField(help_text='Duration in hours', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.BooleanField(default=True, help_text='Toggle to activate/deactivate the course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('users', models.ManyToManyField(related_name='courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='admin_app.course')),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='admin_app.trainer'),
        ),
    ]