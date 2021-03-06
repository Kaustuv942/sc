# Generated by Django 3.0.5 on 2020-06-19 07:29

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
            name='config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_day', models.IntegerField()),
                ('q_no', models.IntegerField()),
                ('quiz_start', models.DateTimeField()),
                ('quiz_endtime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=550)),
                ('day', models.IntegerField()),
                ('question_no', models.IntegerField()),
                ('answer', models.CharField(max_length=100)),
                ('audio', models.FileField(blank=True, upload_to='media/audios')),
                ('image', models.ImageField(blank=True, upload_to='media/images')),
                ('hint', models.CharField(default='na', max_length=555)),
            ],
            options={
                'ordering': ['day', 'question_no'],
            },
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, null=True)),
                ('score', models.IntegerField(default=0)),
                ('rank', models.IntegerField(null=True)),
                ('current_question', models.IntegerField()),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-score', 'last_modified'],
            },
        ),
    ]
