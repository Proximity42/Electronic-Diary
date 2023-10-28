import datetime
from calendar import Calendar
from collections import OrderedDict
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from ElectronicDiary.settings import BEGIN_STUDY_YEAR
from class_journal.models import Mark, Schedule, SubjectInSchedule, Subject
from users.models import ProfileStudent, ProfileTeacher


DAYS_OF_WEEK = {"Понедельник": 0, "Вторник": 1, "Среда": 2, "Четверг": 3, "Пятница": 4, "Суббота": 5}
NUMBERS_OF_MONTHS_IN_TERMS = {"1_term": [9, 10], "2_term": [11, 12], "3_term": [1, 2, 3], "4_term": [4, 5]}


def get_student_journal(request):
    student = ProfileStudent.objects.select_related('grade').get(user=request.user)
    subjects = Subject.objects.filter(study_classes=student.grade)
    marks = Mark.objects.filter(student=student).select_related('subject').only('subject', 'value', 'date')
    context = {"subjects": subjects}
    for key, value in NUMBERS_OF_MONTHS_IN_TERMS.items():
        term = list(filter(lambda mark: mark.date.month in value, marks))
        context[key] = get_subjects_marks_by_term(subjects, term)

    average = []
    if context["4_term"]:
        for i in range(len(subjects)):
            terms_marks = []
            for key in NUMBERS_OF_MONTHS_IN_TERMS.keys():
                terms_marks.append(context[key][i])
            average.append(sum(terms_marks) / len(terms_marks))
    context["average"] = average
    return context


def get_subjects_marks_by_term(subjects, term):
    term_average = []
    for subject in subjects:
        subject_marks = []
        for mark in term:
            if mark.subject == subject:
                subject_marks.append(mark.value)
        if (len(subject_marks)) != 0:
            term_average.append(int(sum(subject_marks) / len(subject_marks)))
    if len(term_average) != len(subjects):
        return []
    return term_average


def get_students_class_by_indx(request, students_classes):
    indx_class = request.POST.get('class_students')
    if indx_class:
        return students_classes[int(indx_class)]
    return students_classes[0]


def get_months_in_term(term):
    return NUMBERS_OF_MONTHS_IN_TERMS[term + "_term"]


def get_dates_lessons(term, student_class, subject):
    schedules = student_class.timetable.all()
    days_of_week = []

    for schedule in schedules:
        if schedule.subjects.filter(subject=subject).exists():
            days_of_week.append(DAYS_OF_WEEK[schedule.day])

    months_in_term = get_months_in_term(term)
    dates = []
    my_calendar = Calendar()
    for month_in_term in months_in_term:
        if month_in_term >= 9 and month_in_term <= 12:
            study_year = BEGIN_STUDY_YEAR
        else:
            study_year = BEGIN_STUDY_YEAR + 1
        for year, month, day, day_of_week in my_calendar.itermonthdays4(study_year, month_in_term):
            if day_of_week in days_of_week and month in months_in_term:
                dates.append(datetime.date(year, month, day))
    dates = list(OrderedDict.fromkeys(dates).keys())
    return dates


def get_lessons_marks_for_subject(subject, dates, student_class):
    subject_marks_all = student_class.marks.filter(subject=subject).select_related('student')
    subject_marks_term = []
    for date in dates:
        for mark in subject_marks_all:
            if mark.date.year == date.year and mark.date.month == date.month and mark.date.day == date.day:
                subject_marks_term.append(mark)
    return subject_marks_term


def get_marks_table(student_class, subject, term):
    dates = get_dates_lessons(term, student_class, subject)
    subject_marks_term = get_lessons_marks_for_subject(subject, dates, student_class)
    students = student_class.students.all()

    data = [["-" for _ in range(len(dates) + 2)] for _ in range(len(students) + 1)]
    data[0][2:] = dates
    data[0][1] = "ФИО"
    data[0][0] = "№"
    for i in range(1, len(data)):
        data[i][0] = i
        data[i][1] = students[i-1]

    for mark in subject_marks_term:
        row_mark = column_mark = 0

        for i in range(1, len(students) + 1):
            if data[i][1] == mark.student:
                row_mark = i
                break

        for j in range(2, len(dates) + 2):
            if data[0][j] == mark.date:
                column_mark = j
                break
        data[row_mark][column_mark] = mark.value

    students = [student.user.get_full_name() for student in students]
    for i in range(1, len(data)):
        data[i][1] = students[i - 1]
    return data


def get_teacher_journal(request):
    teacher = ProfileTeacher.objects.select_related('subject').get(user=request.user)
    subject = teacher.subject
    students_classes = subject.study_classes.prefetch_related(
        Prefetch('students', queryset=ProfileStudent.objects.filter(study_classes__in=subject.study_classes.all()).select_related('user')),
    )
    if students_classes:
        student_class = get_students_class_by_indx(request, students_classes)
        term = request.POST.get('choice')
        if term is None:
            term = "1"
        data = get_marks_table(student_class, subject, term)

        context = {
            "dates": data[0],
            "marks": data[1:],
            "choices": (str(i) for i in range(1, 5)),
            "term": term,
            "grades": students_classes,
            "current_grade": student_class,
            "begin_study_year": BEGIN_STUDY_YEAR,
            "end_study_year": BEGIN_STUDY_YEAR + 1
        }
    else:
        context = {}
    return context


def get_student_schedules(request):
    student = ProfileStudent.objects.select_related('grade').get(user=request.user)
    schedules = Schedule.objects.filter(study_classes=student.grade).prefetch_related(
        Prefetch('subjects', queryset=SubjectInSchedule.objects.all().select_related('subject'))).only('subjects', 'day')
    return schedules


def get_teacher_schedules(request):
    teacher = ProfileTeacher.objects.select_related('subject').prefetch_related('timetable').only('subject', 'timetable').get(user=request.user)
    subject = teacher.subject
    students_classes = subject.study_classes.all()
    subjects_in_schedules = SubjectInSchedule.objects.filter(schedules__in=teacher.timetable.all()).select_related('subject')
    if subjects_in_schedules.count == 0:
        all_subjects_in_schedules = {"понедельник": [], "вторник": [], "среда": [], "четверг": [], "пятница": [],
                                     "суббота": []}
        for schedule in Schedule.objects.filter(study_classes__in=students_classes):
            subjects_in_shedules = schedule.subjects.filter(subject=subject)
            all_subjects_in_schedules[schedule.day.lower()].extend(subjects_in_shedules)

        for schedule in teacher.timetable.all():
            schedule.subjects.set(all_subjects_in_schedules[schedule.day.lower()])

    return teacher.timetable.all().prefetch_related(
        Prefetch('subjects', subjects_in_schedules)
    )


def create_update_or_delete_mark(request, student, date, value):
    teacher = ProfileTeacher.objects.select_related('subject').get(user=request.user)
    subject = teacher.subject
    if value:
        mark, is_created = Mark.objects.update_or_create(student=student, date=date, subject=subject,
                                                         defaults={'value': value})
        if is_created:
            student.grade.marks.add(mark)
    else:
        mark = get_object_or_404(Mark, student=student, date=date, subject=subject)
        mark.delete()