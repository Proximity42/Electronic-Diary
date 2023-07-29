from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from class_journal import models


@admin.register(models.Mark)
class MarkAdmin(ModelAdmin):
    pass


@admin.register(models.StudentsClass)
class StudentsClassAdmin(ModelAdmin):
    filter_horizontal = ['subjects', 'students', 'timetable', 'marks']


@admin.register(models.Subject)
class SubjectAdmin(ModelAdmin):
    pass

@admin.register(models.Schedule)
class ScheduleAdmin(ModelAdmin):
    filter_horizontal = ['subjects']

@admin.register(models.SubjectInSchedule)
class SubjectInScheduleAdmin(ModelAdmin):
    pass