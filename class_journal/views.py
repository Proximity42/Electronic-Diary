from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from class_journal.forms import NewMarkForm
from class_journal.services import get_student_schedules, get_teacher_schedules, create_update_or_delete_mark, \
    get_student_journal, get_teacher_journal


class JournalView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        context = {'user': user}

        if user.is_student:
            return self._get_student_context(request, context)

        elif user.is_teacher:
            return self._get_teacher_context(request, context)

    def post(self, request):
        user = request.user
        context = {'user': user}

        if user.is_teacher:
            return self._get_teacher_context(request, context)

    def _get_teacher_context(self, request, context):
        context.update(get_teacher_journal(request))
        return render(request, 'teacher_journal.html', context)

    def _get_student_context(self, request, context):
        context.update(get_student_journal(request))
        return render(request, 'journal.html', context)


class TimetableView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        context = {'user': user}
        if user.is_student:
            context["schedules"] = get_student_schedules(request)
            return render(request, 'timetable.html', context)

        elif user.is_admin:
            return redirect('admin/')

        elif user.is_teacher:
            context["schedules"] = get_teacher_schedules(request)
            return render(request, 'teacher_timetable.html', context)


class AddMarkView(LoginRequiredMixin, View):

    @csrf_exempt
    def get(self, request):
        form = NewMarkForm()
        return render(request, 'add_mark.html', {'form': form})

    @csrf_exempt
    def post(self, request):
        form = NewMarkForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            student = form.cleaned_data['student']
            date = form.cleaned_data['date']
            create_update_or_delete_mark(request, student, date, value)

            return redirect('journal')
        else:
            print(form.errors)
            return render(request, 'add_mark.html', {'form': form})


class DiaryView(View):
    def get(self, request):
        return render(request, 'diary.html', {})