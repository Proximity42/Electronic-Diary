from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from users.models import ProfileStudent, ProfileTeacher, BaseUser
from class_journal.models import ClassStudents


class UserProfileView(LoginRequiredMixin, DetailView):
    model = BaseUser
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = kwargs['object']
        context['user'] = user
        if user.type == "Ученик":
            student = ProfileStudent.objects.get(user=user)
            class_students = ClassStudents.objects.get(student=student)
            context["study_class"] = class_students.study_class
        if user.type == "Учитель":
            teacher = ProfileTeacher.objects.select_related('subject').get(user=user)
            context["subject"] = teacher.subject
        return context
