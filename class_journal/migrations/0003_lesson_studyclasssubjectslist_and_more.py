# Generated by Django 4.2 on 2023-12-28 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_journal', '0002_alter_assignedmark_options_alter_studyclass_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(db_column='IDls', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='lsDate', verbose_name='Дата учебного занятия')),
            ],
            options={
                'db_table': 'lessons',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudyClassSubjectsList',
            fields=[
                ('id', models.AutoField(db_column='IDsc_su', primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Список предметов в классе',
                'verbose_name_plural': 'Списки предметов в классах',
                'db_table': 'class_subjects_list',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='classstudents',
            options={'default_related_name': 'students_class', 'managed': False, 'verbose_name': 'Состав класса', 'verbose_name_plural': 'Состав классов'},
        ),
        migrations.AlterModelOptions(
            name='mark',
            options={'default_related_name': 'marks', 'managed': False, 'verbose_name': 'Оценки', 'verbose_name_plural': 'Оценки'},
        ),
    ]
