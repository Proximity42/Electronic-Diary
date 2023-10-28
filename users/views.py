from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from users.models import ProfileStudent, ProfileTeacher, BaseUser


class UserProfileView(LoginRequiredMixin, DetailView):
    model = BaseUser
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = kwargs['object']
        context['user'] = user
        if user.is_student:
            student = ProfileStudent.objects.select_related('grade').get(user=user)
            context["study_class"] = student.grade
        if user.is_teacher:
            teacher = ProfileTeacher.objects.select_related('study_class', 'subject').get(user=user)
            context["study_class"] = teacher.study_class
            context["subject"] = teacher.subject
        return context
