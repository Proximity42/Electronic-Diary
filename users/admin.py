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
    list_filter = ["type"]
    list_display_links = None
    ordering = ("identifier", "last_name", "first_name", "middle_name")
    list_display = ("identifier", "last_name", "first_name", "middle_name", "type")
    list_editable = ()
    exclude = ("groups", "permissions", "last_login")
    filter_horizontal = ()

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.add_fieldsets[0][1]['fields'] = ('identifier', 'password1', 'password2', 'type',
                                              "last_name", "first_name", "middle_name")


@admin.register(ProfileStudent)
class StudentAdmin(ModelAdmin):
    pass
    # fieldsets = ()
    # # search_fields = ("user__last_name__startswith", "user__first_name__startswith")
    # # list_filter = ["type"]
    # list_select_related = ("user", )
    # # ordering = ("user__last_name", "user__first_name", "user__middle_name")
    # # list_display = ("user__last_name", "user__first_name", "user__middle_name", "study_class")
    #
    # # exclude = ("last_login", "date_joined",)
    #
    # def __init__(self, model, admin_site):
    #     super().__init__(model, admin_site)
    #     # self.add_fieldsets[0][1]['fields'] = ('identifier', 'password1', 'password2', 'type',
    #     #                                       "last_name", "first_name", "middle_name")


@admin.register(ProfileTeacher)
class TeacherAdmin(ModelAdmin):
    # filter_horizontal = ['timetable']
    pass