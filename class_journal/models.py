from datetime import date
from django.db import models
from class_journal.validators import borders_date_validate


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


# class Schedule(models.Model):
#     DAYS_OF_WEEK = [
#         ('Понедельник', 'понедельник'),
#         ('Вторник', 'вторник'),
#         ('Среда', 'среда'),
#         ('Четверг', 'четверг'),
#         ('Пятница', 'пятница'),
#         ('Суббота', 'суббота'),
#     ]
#
#     day = models.CharField(max_length=11, choices=DAYS_OF_WEEK, verbose_name="День недели")
#     subjects = models.ManyToManyField('SubjectInSchedule', blank=True, verbose_name="Список предметов")
#
#     class Meta:
#         verbose_name_plural = "Расписания"
#         verbose_name = "Расписание"
#         default_related_name = 'schedules'
#
#     def __str__(self):
#         return f"{self.day}"


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
    number_grade = models.CharField(max_length=3, verbose_name="Номер класса", db_column="scNumber")
    students = models.ManyToManyField('users.ProfileStudent', blank=True, verbose_name="Список учеников",
                                      through="ClassStudents")
    year_begin = models.DateField(db_column="scYearBegin", blank=True)

    class Meta:
        managed = False
        verbose_name_plural = "Учебные классы"
        verbose_name = "Учебный класс"
        default_related_name = 'study_class'
        db_table = "study_classes"

    def __str__(self):
        return f"{self.number_grade} класс ( {self.year_begin.year} - {self.year_begin.year + 1} )"


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
        verbose_name_plural = "Состав классов"
        verbose_name = "Состав класса"
        db_table = "class_students"
        default_related_name = 'students_class'

    def __str__(self):
        return f"{self.student} - {self.study_class}"


class Lesson(models.Model):
    id = models.AutoField(primary_key=True, db_column="IDls")
    date = models.DateTimeField(db_column="lsDate", verbose_name="Дата учебного занятия")
    teacher = models.ForeignKey('users.ProfileTeacher', on_delete=models.DO_NOTHING,
                                blank=True, verbose_name="Учитель", db_column="tID")

    class Meta:
        managed = False
        db_table = "lessons"


class Mark(models.Model):
    MARK_VALUE_CHOICES = [(i, f"{i}") for i in range(2, 6)]
    id = models.AutoField(primary_key=True, db_column="IDm")
    # date = models.DateField(blank=True, verbose_name="Дата оценки", validators=[borders_date_validate],
    #                         db_column="mDate")
    lesson = models.ForeignKey("Lesson", on_delete=models.DO_NOTHING, db_column="lsID")
    value = models.IntegerField(choices=MARK_VALUE_CHOICES, blank=True, null=True,
                                verbose_name="Оценка", db_column="mValue")
    students = models.ManyToManyField("users.ProfileStudent", blank=True, through="AssignedMark")
    subjects = models.ManyToManyField("Subject", blank=True, through="AssignedMark")

    class Meta:
        managed = False
        verbose_name_plural = "Оценки"
        verbose_name = "Оценки"
        default_related_name = 'marks'
        # ordering = ["-date"]
        db_table = "marks"

    def __str__(self):
        return f"{self.value}"


class AssignedMark(models.Model):
    id = models.AutoField(primary_key=True, db_column="IDam")
    subject = models.ForeignKey("Subject", on_delete=models.DO_NOTHING, db_column="suID")
    student = models.ForeignKey("users.ProfileStudent", on_delete=models.DO_NOTHING, db_column="stID")
    mark = models.ForeignKey("Mark", on_delete=models.DO_NOTHING, db_column="mID")

    class Meta:
        managed = False
        db_table = "assigned_marks"
        verbose_name_plural = "Выставленные оценки"
        verbose_name = "Выставленная оценка"

    def __str__(self):
        return f"{self.mark} - {self.subject} - {self.student}"