# Generated by Django 4.2 on 2023-12-27 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseuser',
            options={'default_related_name': 'user', 'managed': False, 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='profilestudent',
            options={'default_related_name': 'student', 'managed': False, 'verbose_name': 'Ученик', 'verbose_name_plural': 'Ученики'},
        ),
    ]