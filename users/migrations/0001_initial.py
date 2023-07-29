# Generated by Django 4.2 on 2023-05-20 04:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('class_journal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('type', models.CharField(blank=True, choices=[('УЧЕНИК', 'ученик'), ('УЧИТЕЛЬ', 'учитель')], default='УЧЕНИК', max_length=7)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('identifier', models.CharField(max_length=15, unique=True, verbose_name='Идентификатор')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('middle_name', models.CharField(max_length=30, verbose_name='Отчество')),
                ('last_login', models.DateTimeField(auto_now=True, null=True)),
                ('date_joined', models.DateTimeField(auto_now=True, null=True)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_group', related_query_name='user', to='auth.group', verbose_name='user groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_permission_rel', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfileTeacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('study_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='class_journal.studentsclass')),
                ('subject', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='class_journal.subject')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileStudent',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='class_journal.studentsclass')),
            ],
        ),
    ]