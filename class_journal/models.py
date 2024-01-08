import datetime
from datetime import date
from django.db import models
# from class_journal.validators import borders_date_validate


class Subject(models.Model):
    # Таблица учебных предметов

    id = models.AutoField(primary_key=True, db_column="IDsu")
    title = models.CharField(max_length=50, verbose_name="Учебный предмет", db_column="suTitle")

    class Meta:
        managed = False
        verbose_name_plural = "Учебные предметы"
        verbose_name = "Учебный предмет"
        # default_related_name = "subjects"
        db_table = "study_subjects"

    def __str__(self):
        return f"{self.title}"


class Timetable(models.Model):
    WEEK_DAYS = [
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
    ]

    id = models.AutoField(primary_key=True, db_column="IDtt")
    week_day = models.CharField(max_length=11, choices=WEEK_DAYS, verbose_name="День недели", db_column="ttWeekDay")
    time_begin = models.TimeField(verbose_name="Время начала урока", db_column="ttTimeBegin")
    time_end = models.TimeField(verbose_name="Время конца урока", db_column="ttTimeEnd")
    subject = models.ForeignKey('Subject', verbose_name="Предмет", on_delete=models.DO_NOTHING,
                                db_column="suID")
    teacher = models.ForeignKey('users.ProfileTeacher', verbose_name="Учитель", on_delete=models.DO_NOTHING,
                                db_column="tID")
    study_class = models.ForeignKey('StudyClass', verbose_name="Класс", on_delete=models.DO_NOTHING,
                                    db_column="scID")
    study_room = models.ForeignKey('StudyRoom', verbose_name="Кабинет", on_delete=models.DO_NOTHING,
                                   db_column="srID")

    class Meta:
        managed = False
        ordering = ("time_begin",)
        verbose_name_plural = "Расписание"
        verbose_name = "Элемент расписания"
        default_related_name = 'timetable'
        db_table = "timetable"

    def get_time(self):
        return f"{self.time_begin.hour}:{self.time_begin.minute}-{self.time_end.hour}:{self.time_end.minute}"

    def get_teacher(self):
        return f"{self.teacher.user.last_name} {self.teacher.user.first_name} {self.teacher.user.middle_name}"

    # def __str__(self):
    #     return f"{self.day}"


class StudyRoom(models.Model):
    id = models.AutoField(primary_key=True, db_column="IDsr")
    number = models.IntegerField(verbose_name="Номер кабинета", db_column="srNumber", unique=True)

    class Meta:
        managed = False
        db_table = "study_rooms"
        verbose_name_plural = "Кабинеты"
        verbose_name = "Кабинет"

    def __str__(self):
        return f"{self.number}"


# class SubjectInSchedule(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
#     start_time = models.TimeField(verbose_name="Начало урока")
#     end_time = models.TimeField(verbose_name="Конец урока")
#
#     class Meta:
#         verbose_name_plural = "Предметы расписания"
#         verbose_name = "Предмет расписания"
#         default_related_name = 'subjects_in_schedules'
#         ordering = ['start_time']
#
#     def get_time(self):
#         return f"{self.start_time} - {self.end_time}"


class StudyClass(models.Model):
    # NUMBER_CHOICES = [(i, f"{i}") for i in range(1, 12)]
    id = models.AutoField(primary_key=True, db_column="IDsc")
    number_grade = models.CharField(max_length=3, verbose_name="Номер класса", db_column="scNumber", unique=True)
    students = models.ManyToManyField('users.ProfileStudent', blank=True, verbose_name="Список учеников",
                                      through="ClassStudents")
    year_begin = models.DateField(db_column="scYearBegin", blank=True, verbose_name="Год начала обучения")

    def years(self):
        return f"{self.year_begin.year} - {self.year_begin.year + 1}"

    class Meta:
        managed = False
        verbose_name_plural = "Учебные классы"
        verbose_name = "Учебный класс"
        default_related_name = 'study_class'
        db_table = "study_classes"
        ordering = ("year_begin", "number_grade")

    def __str__(self):
        return f"{self.number_grade} класс"


class StudyClassSubjectsList(models.Model):
    id = models.AutoField(primary_key=True, db_column="IDsc_su")
    study_class = models.ForeignKey("StudyClass", on_delete=models.DO_NOTHING, blank=True,
                                    verbose_name="Учебный класс", db_column="scID")
    subject = models.ForeignKey("Subject", on_delete=models.DO_NOTHING, blank=True,
                                verbose_name="Учебный предмет", db_column="suID")

    class Meta:
        managed = False
        verbose_name_plural = "Список предметов"
        verbose_name = "Учебный предмет"
        db_table = "class_subjects_list"

    def __str__(self):
        return f"{self.study_class} - {self.subject}"


class ClassStudents(models.Model):
    id = models.AutoField(primary_key=True, db_column="IDsc_st")
    study_class = models.ForeignKey('StudyClass', on_delete=models.DO_NOTHING,
                                    blank=True, verbose_name="Учебный класс", db_column="scID")
    student = models.ForeignKey('users.ProfileStudent', on_delete=models.DO_NOTHING,
                                blank=True, verbose_name="Ученик", db_column="stID")

    class Meta:
        managed = False
        verbose_name_plural = "Состав класса"
        verbose_name = "Состав класса"
        db_table = "class_students"
        default_related_name = 'students_class'
        ordering = ("study_class", "student")

    def __str__(self):
        return f"{self.student} - {self.study_class}"


class Lesson(models.Model):
    id = models.AutoField(primary_key=True, db_column="IDls")
    date = models.DateTimeField(db_column="lsDate", verbose_name="Дата и время учебного занятия")
    teacher = models.ForeignKey('users.ProfileTeacher', on_delete=models.DO_NOTHING,
                                verbose_name="Учитель", db_column="tID")
    study_class = models.ForeignKey("StudyClass", on_delete=models.DO_NOTHING,
                                verbose_name="Учебный класс", db_column="scID")

    class Meta:
        managed = False
        ordering = ("date", )
        db_table = "lessons"
        verbose_name_plural = "Занятия"
        verbose_name = "Занятие"

    def __str__(self):
        return f"Занятие {self.date} - {self.study_class} - {self.teacher}"


# class Mark(models.Model):
#     MARK_VALUE_CHOICES = [(i, f"{i}") for i in range(2, 6)]
#     id = models.AutoField(primary_key=True, db_column="IDm")
#     # date = models.DateField(blank=True, verbose_name="Дата оценки", validators=[borders_date_validate],
#     #                         db_column="mDate")
#     lesson = models.ForeignKey("Lesson", on_delete=models.DO_NOTHING, db_column="lsID")
#     value = models.IntegerField(choices=MARK_VALUE_CHOICES, blank=True, null=True,
#                                 verbose_name="Оценка", db_column="mValue")
#     students = models.ManyToManyField("users.ProfileStudent", blank=True, through="AssignedMark")
#     subjects = models.ManyToManyField("Subject", blank=True, through="AssignedMark")
#
#     class Meta:
#         managed = False
#         verbose_name_plural = "Оценки"
#         verbose_name = "Оценки"
#         default_related_name = 'marks'
#         # ordering = ["-date"]
#         db_table = "marks"
#
#     def __str__(self):
#         return f"{self.value}"


class Mark(models.Model):
    MARK_VALUE_CHOICES = [(i, f"{i}") for i in range(2, 6)]
    id = models.AutoField(primary_key=True, db_column="IDm")
    subject = models.ForeignKey("Subject", on_delete=models.DO_NOTHING, db_column="suID", verbose_name="Предмет")
    student = models.ForeignKey("users.ProfileStudent", on_delete=models.DO_NOTHING, db_column="stID",
                                verbose_name="Ученик")
    lesson = models.ForeignKey("Lesson", on_delete=models.DO_NOTHING, db_column="lsID", verbose_name="Занятие")
    mark = models.IntegerField(choices=MARK_VALUE_CHOICES, blank=True, null=True, db_column="mValue",
                               verbose_name="Оценка")

    class Meta:
        managed = False
        db_table = "marks"
        verbose_name_plural = "Оценки"
        verbose_name = "Оценка"

    def __str__(self):
        return f"{self.mark} - {self.subject} - {self.student}"
