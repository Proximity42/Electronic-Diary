# Generated by Django 4.2 on 2024-01-03 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('class_journal', '0003_lesson_studyclasssubjectslist_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'managed': False, 'verbose_name': 'Занятие', 'verbose_name_plural': 'Занятия'},
        ),
        migrations.AlterModelOptions(
            name='studyclasssubjectslist',
            options={'managed': False, 'verbose_name': 'Учебный предмет', 'verbose_name_plural': 'Список предметов'},
        ),
    ]