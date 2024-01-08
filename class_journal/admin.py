from django.contrib import admin
from django.contrib.admin import ModelAdmin
from class_journal import models


# @admin.register(models.Mark)
# class MarkAdmin(ModelAdmin):
#     pass


@admin.register(models.Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ("date", "subject", "study_class", "get_teacher")

    def subject(self, obj):
        return f"{obj.teacher.subject}"

    subject.short_description = "Предмет"
    subject.admin_order_field = "teacher__subject"

    def get_teacher(self, obj):
        return f"{obj.teacher.user.last_name} {obj.teacher.user.first_name} {obj.teacher.user.middle_name}"

    get_teacher.short_description = "Учитель"
    get_teacher.admin_order_field = "teacher__user__last_name"


class ClassStudentsListAdmin(admin.TabularInline):
    model = models.ClassStudents
    extra = 0


@admin.register(models.Mark)
class MarkAdmin(ModelAdmin):
    list_display = ("mark", "subject", "student", "study_class", "date_and_time")

    def date_and_time(self, obj: models.Mark):
        lesson = obj.lesson
        return f"{lesson.date.day}.{lesson.date.month}.{lesson.date.year} {lesson.date.hour}:{lesson.date.minute}"

    def study_class(self, obj: models.Mark):
        study_class = models.ClassStudents.objects.get(student=obj.student).study_class
        return f"{study_class}"

    date_and_time.short_description = "Дата и время занятия"
    study_class.short_description = "Класс"


class StudyClassSubjectsListAdmin(admin.TabularInline):
    model = models.StudyClassSubjectsList
    extra = 0


@admin.register(models.StudyClass)
class StudyClassAdmin(ModelAdmin):
    # filter_horizontal = ['students']
    inlines = [StudyClassSubjectsListAdmin, ClassStudentsListAdmin]
    ordering = ['number_grade']
    list_display = ("number_grade", "years_")

    def years_(self, obj):
        return obj.years()

    years_.short_description = "Годы обучения"


@admin.register(models.Subject)
class SubjectAdmin(ModelAdmin):
    pass


@admin.register(models.Timetable)
class TimetableAdmin(ModelAdmin):
    list_display = ("week_day", "time", "subject", "study_class", "get_teacher", "study_room")

    def time(self, obj):
        return f"{obj.get_time()}"

    time.short_description = "Время урока"

    def get_teacher(self, obj):
        return f"{obj.get_teacher()}"

    get_teacher.short_description = "Учитель"


@admin.register(models.StudyRoom)
class StudyRoomAdmin(ModelAdmin):
    list_display = ("number", )

