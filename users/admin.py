from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from users.models import ProfileStudent, ProfileTeacher
from users.models import BaseUser


@admin.register(BaseUser)
class BaseUserAdmin(UserAdmin):
    fieldsets = ()
    search_fields = ("last_name__startswith", "first_name__startswith")
    filter_horizontal = ("groups", "user_permissions")
    list_filter = ["type", "is_staff"]
    ordering = ("identifier", "last_name", "first_name", "middle_name", "type")
    list_display = ("identifier", "last_name", "first_name", "middle_name", "type", "is_staff")
    exclude = ("last_login", "date_joined",)

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.add_fieldsets[0][1]['fields'] = ('identifier', 'password1', 'password2', 'type',
                                              "last_name", "first_name", "middle_name", "is_student",
                                              "is_teacher", "groups")


@admin.register(ProfileStudent)
class StudentAdmin(ModelAdmin):
    pass


@admin.register(ProfileTeacher)
class TeacherAdmin(ModelAdmin):
    filter_horizontal = ['timetable']
