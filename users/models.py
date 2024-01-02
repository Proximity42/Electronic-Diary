from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import AutoField
from users.managers import UserManager


def make_identifier():
    nm = BaseUser.objects.all()
    nm1 = 1
    for i1 in nm:
        if int(i1.identifier) > nm1:
            nm1 = int(i1.identifier)
    nm1 += 1
    if not str(nm1).startswith("1111"):
        nn = '1111' + str(nm1)
    else:
        nn = str(nm1)
    return nn


class BaseUser(AbstractBaseUser):
    class Types(models.TextChoices):
        STUDENT = "Ученик", "ученик"
        TEACHER = "Учитель", "учитель"
        ADMIN = "Администратор", "администратор"

    id = AutoField(primary_key=True, db_column="IDbu")
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', db_column="buLastName")
    first_name = models.CharField(max_length=50, verbose_name='Имя', db_column="buFirstName")
    middle_name = models.CharField(max_length=50, verbose_name='Отчество', db_column="buMiddleName")

    identifier = models.CharField(max_length=15, default=make_identifier,
                                verbose_name='Идентификатор', db_column="buIdentifier", unique=True)

    password = models.CharField(max_length=128, verbose_name='Пароль', db_column="buPassword")
    type = models.CharField(max_length=15, choices=Types.choices, default=Types.STUDENT, blank=True,
                            verbose_name="Тип пользователя", db_column="buType")

    is_active = models.BooleanField(default=True, db_column="buIsActive")
    is_admin = models.BooleanField(default=False, db_column="buIsAdmin")
    is_staff = models.BooleanField(default=False, db_column="buIsStaff")
    is_superuser = models.BooleanField(default=False, db_column="buIsSuperUser")
    last_login = models.DateTimeField(db_column="buLastLogin", null=True, blank=True)

    USERNAME_FIELD = 'identifier'

    objects = UserManager()

    REQUIRED_FIELDS = ['last_name', 'first_name', 'middle_name']

    class Meta:
        managed = False
        verbose_name_plural = "Все пользователи"
        verbose_name = "Пользователь"
        default_related_name = 'user'
        db_table = "base_users"

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f"{self.type} {self.get_full_name()}"
        # if self.is_admin:
        #     return f"Администратор {self.identifier}"
        # elif self.is_student:
        #     return f"Ученик {self.last_name} {self.first_name} {self.middle_name}"
        # elif self.is_teacher:
        #     return f"Учитель {self.last_name} {self.first_name} {self.middle_name}"


class ProfileStudent(models.Model):
    id = models.AutoField(primary_key=True, db_column="IDst")
    user = models.OneToOneField("BaseUser", on_delete=models.DO_NOTHING,
                                verbose_name="Пользователь", db_column="buID")
    subjects = models.ManyToManyField("class_journal.Subject", blank=True, through="class_journal.AssignedMark")
    #grade = models.ForeignKey('class_journal.StudentsClass', on_delete=models.CASCADE, verbose_name="Класс")

    class Meta:
        managed = False
        verbose_name_plural = "Ученики"
        verbose_name = "Ученик"
        default_related_name = 'student'
        db_table = "students"

    def __str__(self):
       return f"{self.user}"


class ProfileTeacher(models.Model):
    id = models.AutoField(primary_key=True, db_column="IDt")
    user = models.OneToOneField(BaseUser, on_delete=models.DO_NOTHING, verbose_name="Пользователь", db_column="buID")
    # study_class = models.ForeignKey('class_journal.StudentsClass', on_delete=models.DO_NOTHING,
    #                                 verbose_name="Учебный класс", db_column="tS")
    subject = models.ForeignKey('class_journal.Subject', on_delete=models.DO_NOTHING,
                                verbose_name="Учебный предмет", db_column="suID")
    # timetable = models.ManyToManyField("class_journal.Schedule", blank=True, verbose_name="Расписание")

    class Meta:
        managed = False
        verbose_name_plural = "Учителя"
        verbose_name = "Учитель"
        default_related_name = 'teachers'
        db_table = "teachers"

    def __str__(self):
        return f"{self.user} - {self.subject}"