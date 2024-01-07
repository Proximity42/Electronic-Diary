from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from class_journal.forms import AddMarkForm
from class_journal.services import create_update_or_delete_mark, \
    get_student_journal_context, get_teacher_journal, get_students_timetable, get_teachers_timetable


class JournalView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        context = {'user': user}

        if user.type == "Ученик":
            return self._get_student_context(request, context)

        elif user.type == "Учитель":
            return self._get_teacher_context(request, context)

        elif user.type == "Администратор":
            return redirect('admin/')

    def post(self, request):
        user = request.user
        context = {'user': user}

        if user.type == "Учитель":
            return self._get_teacher_context(request, context)

        elif user.type == "Ученик":
            return self._get_student_context(request, context)

    @staticmethod
    def _get_teacher_context(request, context):
        context.update(get_teacher_journal(request))
        return render(request, 'teacher_journal.html', context)

    @staticmethod
    def _get_student_context(request, context):
        context.update(get_student_journal_context(request))
        return render(request, 'journal.html', context)


class TimetableView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        context = {'user': user}
        if user.type == "Ученик":
            context["timetables"] = get_students_timetable(request)
            return render(request, 'timetable.html', context)

        elif user.type == "Администратор":
            return redirect('admin/')

        elif user.type == "Учитель":
            context["timetables"] = get_teachers_timetable(request)
            return render(request, 'teacher_timetable.html', context)


class AddMarkView(LoginRequiredMixin, View):

    @csrf_exempt
    def get(self, request):
        form = NewMarkForm()
        return render(request, 'add_mark.html', {'form': form})

    @csrf_exempt
    def post(self, request):
        form = AddMarkForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            student = form.cleaned_data['student']
            date = form.cleaned_data['lesson']
            create_update_or_delete_mark(request, student, date, value)

            return redirect('journal')
        else:
            print(form.errors)
            return render(request, 'add_mark.html', {'form': form})


class DiaryView(View):
    def get(self, request):
        return render(request, 'diary.html', {})
