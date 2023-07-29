from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Permission, Group, PermissionsMixin
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
    if not str(nm1).startswith("111"):
        nn = '111' + str(nm1)
    else:
        nn = str(nm1)
    return nn


class BaseUser(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        STUDENT = "Ученик", "ученик"
        TEACHER = "Учитель", "учитель"

    type = models.CharField(max_length=7, choices=Types.choices, default=Types.STUDENT, blank=True,
                            verbose_name="Тип пользователя")

    id = AutoField(primary_key=True)
    identifier = models.CharField(max_length=15,
                                  unique=True,
                                  default=make_identifier,
                                  verbose_name='Идентификатор',
                                  )

    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    middle_name = models.CharField(max_length=30, verbose_name='Отчество')
    last_login = models.DateTimeField(auto_now=True, null=True)
    date_joined = models.DateTimeField(auto_now=True, null=True)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'identifier'

    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='user_group',
        blank=True,
        help_text=
        'The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='Группы',
        related_query_name='user'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="user_permission_rel",
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
        related_query_name='user'
    )

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"
        default_related_name = 'users'

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        if self.is_admin:
            return f"Администратор {self.identifier}"
        elif self.is_student:
            return f"Ученик {self.last_name} {self.first_name} {self.middle_name}"
        elif self.is_teacher:
            return f"Учитель {self.last_name} {self.first_name} {self.middle_name}"


class ProfileStudent(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    grade = models.ForeignKey('class_journal.StudentsClass', on_delete=models.CASCADE, verbose_name="Класс")

    class Meta:
        verbose_name_plural = "Ученики"
        verbose_name = "Ученик"
        default_related_name = 'profile_students'

    def __str__(self):
        return f"{self.user} - {self.grade}"


class ProfileTeacher(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    study_class = models.ForeignKey('class_journal.StudentsClass', on_delete=models.CASCADE,
                                    verbose_name="Учебный класс")
    subject = models.OneToOneField('class_journal.Subject', on_delete=models.CASCADE, verbose_name="Учебный предмет")
    timetable = models.ManyToManyField("class_journal.Schedule", blank=True, verbose_name="Расписание")

    class Meta:
        verbose_name_plural = "Учителя"
        verbose_name = "Учитель"
        default_related_name = 'teachers'

    def __str__(self):
        return f"{self.user} - {self.subject}"