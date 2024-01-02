from django.contrib import admin
from django.contrib.admin import ModelAdmin
from class_journal import models


@admin.register(models.Mark)
class MarkAdmin(ModelAdmin):
    pass


@admin.register(models.Lesson)
class LessonAdmin(ModelAdmin):
    pass


# class ClassStudentsInline(admin.StackedInline):
#     model = models.ClassStudents
#     extra = 0


@admin.register(models.AssignedMark)
class AssignedMarkAdmin(ModelAdmin):
    pass


class StudyClassSubjectsListAdmin(admin.TabularInline):
    model = models.StudyClassSubjectsList
    extra = 0


@admin.register(models.StudyClass)
class StudyClassAdmin(ModelAdmin):
    # filter_horizontal = ['students']
    inlines = [StudyClassSubjectsListAdmin]


@admin.register(models.Subject)
class SubjectAdmin(ModelAdmin):
    pass

# @admin.register(models.Schedule)
# class ScheduleAdmin(ModelAdmin):
#     filter_horizontal = ['subjects']
#
# @admin.register(models.SubjectInSchedule)
# class SubjectInScheduleAdmin(ModelAdmin):
#     pass