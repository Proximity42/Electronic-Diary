# Generated by Django 4.2 on 2023-12-26 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedMark',
            fields=[
                ('id', models.AutoField(db_column='IDam', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'assigned_marks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClassStudents',
            fields=[
                ('id', models.AutoField(db_column='IDsc_st', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'class_students',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(db_column='IDm', primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, db_column='mDate', verbose_name='Дата оценки')),
                ('value', models.IntegerField(blank=True, choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5')], db_column='mValue', null=True, verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Оценки',
                'verbose_name_plural': 'Оценки',
                'db_table': 'marks',
                'ordering': ['-date'],
                'managed': False,
                'default_related_name': 'marks',
            },
        ),
        migrations.CreateModel(
            name='StudyClass',
            fields=[
                ('id', models.AutoField(db_column='IDsc', primary_key=True, serialize=False)),
                ('number_grade', models.CharField(db_column='scNumber', max_length=3, verbose_name='Номер класса')),
            ],
            options={
                'verbose_name': 'Учебный класс',
                'verbose_name_plural': 'Учебные классы',
                'db_table': 'study_classes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(db_column='IDsu', primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='suTitle', max_length=50, verbose_name='Учебный предмет')),
            ],
            options={
                'verbose_name': 'Учебный предмет',
                'verbose_name_plural': 'Учебные предметы',
                'db_table': 'study_subjects',
                'managed': False,
            },
        ),
    ]
