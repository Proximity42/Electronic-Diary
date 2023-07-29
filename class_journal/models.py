from django.db import models

from class_journal.validators import borders_date_validate


class Subject(models.Model):
    title = models.CharField(max_length=50, verbose_name="Учебный предмет")

    class Meta:
        verbose_name_plural = "Учебные предметы"
        verbose_name = "Учебный предмет"
        default_related_name = 'subjects'

    def __str__(self):
        return f"{self.title}"


class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Понедельник', 'понедельник'),
        ('Вторник', 'вторник'),
        ('Среда', 'среда'),
        ('Четверг', 'четверг'),
        ('Пятница', 'пятница'),
        ('Суббота', 'суббота'),
    ]

    day = models.CharField(max_length=11, choices=DAYS_OF_WEEK, verbose_name="День недели")
    subjects = models.ManyToManyField('SubjectInSchedule', blank=True, verbose_name="Список предметов")

    class Meta:
        verbose_name_plural = "Расписания"
        verbose_name = "Расписание"
        default_related_name = 'schedules'

    def __str__(self):
        return f"{self.day}"


class SubjectInSchedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    start_time = models.TimeField(verbose_name="Начало урока")
    end_time = models.TimeField(verbose_name="Конец урока")

    class Meta:
        verbose_name_plural = "Предметы расписания"
        verbose_name = "Предмет расписания"
        default_related_name = 'subjects_in_schedules'
        ordering = ['start_time']

    def get_time(self):
        return f"{self.start_time} - {self.end_time}"

class StudentsClass(models.Model):
    NUMBER_CHOICES = [(i, f"{i}") for i in range(1, 12)]
    number_grade = models.IntegerField(choices=NUMBER_CHOICES, verbose_name="Номер класса")
    students = models.ManyToManyField('users.ProfileStudent', blank=True, verbose_name="Список учеников")
    marks = models.ManyToManyField('Mark', blank=True, verbose_name="Список оценок")
    subjects = models.ManyToManyField('Subject', blank=True, verbose_name="Список предметов")
    timetable = models.ManyToManyField("Schedule", blank=True, verbose_name="Расписание")

    class Meta:
        verbose_name_plural = "Учебные классы"
        verbose_name = "Учебный класс"
        default_related_name = 'study_classes'

    def __str__(self):
        return f"{self.number_grade} класс"


class Mark(models.Model):
    MARK_VALUE_CHOICES = [(i, f"{i}") for i in range(2, 6)]
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name="Учебный предмет")
    student = models.ForeignKey('users.ProfileStudent', on_delete=models.CASCADE, blank=True, verbose_name="Ученик")
    date = models.DateField(blank=True, verbose_name="Дата", validators=[borders_date_validate])
    value = models.IntegerField(choices=MARK_VALUE_CHOICES, blank=True, default=2, null=True, verbose_name="Оценка")

    class Meta:
        verbose_name_plural = "Оценки"
        verbose_name = "Оценка"
        default_related_name = 'marks'
        ordering = ["-date"]

    def __str__(self):
        return f"{self.value} ({self.subject}, {self.date}) - {self.student}"








