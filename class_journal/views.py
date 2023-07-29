from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from class_journal.forms import NewMarkForm
from class_journal.services import get_student_schedules, get_teacher_schedules, create_update_or_delete_mark, \
    get_journal_for_student, get_teacher_journal



class JournalView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        context = {'user': user}
        if user.groups.filter(name="Ученики").exists():
            context.update(get_journal_for_student(request))
            return render(request, 'journal.html', context)

        elif user.groups.filter(name="Учителя").exists():
            context.update(get_teacher_journal(request))
            return render(request, 'teacher_journal.html', context)

    def post(self, request):
        user = request.user
        context = {'user': user}
        if user.groups.filter(name="Ученики").exists():
            context.update(get_journal_for_student(request))
            return render(request, 'journal.html', context)

        elif user.groups.filter(name="Учителя").exists():
            context.update(get_teacher_journal(request))
            return render(request, 'teacher_journal.html', context)


class TimetableView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        context = {'user': user}
        if user.groups.filter(name="Ученики").exists():
            context["schedules"] = get_student_schedules(request)
            return render(request, 'timetable.html', context)

        elif user.groups.filter(name="Администраторы").exists():
            return redirect('admin/')

        elif user.groups.filter(name="Учителя").exists():
            context["schedules"] = get_teacher_schedules(request)
            return render(request, 'teacher_timetable.html', context)


class DiaryView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'diary.html')


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
