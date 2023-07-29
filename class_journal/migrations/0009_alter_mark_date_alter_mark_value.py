# Generated by Django 4.2 on 2023-06-07 09:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_journal', '0008_alter_mark_value_alter_schedule_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='date',
            field=models.DateField(default=datetime.date(2023, 6, 7)),
        ),
        migrations.AlterField(
            model_name='mark',
            name='value',
            field=models.IntegerField(choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5')], default=2),
        ),
    ]