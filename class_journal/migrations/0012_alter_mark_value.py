# Generated by Django 4.2 on 2023-06-07 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_journal', '0011_alter_mark_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='value',
            field=models.IntegerField(blank=True, choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5')], default=2),
        ),
    ]