import datetime
from calendar import Calendar
from collections import OrderedDict
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from class_journal.models import Mark, Subject, ClassStudents, StudyClassSubjectsList, AssignedMark, Lesson, Timetable
from users.models import ProfileStudent, ProfileTeacher


DAYS_OF_WEEK = {"Понедельник": 0, "Вторник": 1, "Среда": 2, "Четверг": 3, "Пятница": 4, "Суббота": 5}
MONTHS_IN_TERMS = {"1": [9, 10], "2": [11, 12], "3": [1, 2, 3], "4": [4, 5]}


def get_student_journal_context(request):
    student = ProfileStudent.objects.get(user=request.user)
    class_students = ClassStudents.objects.get(student=student)
    study_class = class_students.study_class
    study_class_subjects_lists = StudyClassSubjectsList.objects.filter(study_class=study_class)
    subjects = [study_class_subjects_list.subject for study_class_subjects_list in study_class_subjects_lists]
    if len(subjects) > 0:
        # term = request.POST.get('choice')
        # if not term:
        #     term = "1"
        lessons = Lesson.objects.filter(study_class=study_class)
        class_marks = Mark.objects.filter(lesson__in=lessons)
        assigned_marks = AssignedMark.objects.filter(student=student, mark__in=class_marks).prefetch_related("mark")
        marks_in_this_year = [assigned_mark.mark for assigned_mark in assigned_marks]
        # marks_in_this_term = [mark for mark in all_marks if
        #         ((mark.lesson.date.year == study_class.year_begin and mark.lesson.date.month in range(9, 13)) or
        #         (mark.lesson.date.year == study_class.year_begin + 1 and mark.lesson.date.month in range(1, 6))) and
        #         mark.lesson.date.month in MONTHS_IN_TERMS[term]]
        # marks_in_this_term = [mark for mark in marks_in_this_year if mark.lesson.date.month in MONTHS_IN_TERMS[term]]
        # dates = [lesson.dates for lesson in lessons]
        # data = [["" for _ in range(len(lessons) + 1)] for _ in range(len(subjects))]
        data = [[subject] for _, subject in enumerate(subjects)]
        indx_mark = 0
        for i, subject in enumerate(subjects):
            marks_of_subject = []
            while indx_mark < len(marks_in_this_year):
                mark = marks_in_this_year[indx_mark]
                indx_mark += 1
                assigned_mark = AssignedMark.objects.get(mark=mark)
                if assigned_mark.subject == subject:
                    marks_of_subject.append(mark)
                else:
                    marks_of_subject.append(" ")
            indx_mark = 0
            data[i].extend(marks_of_subject)

        # for i in range(len(subjects)):
        #     data[i][0] = subjects[0]

        # for i, student in enumerate(students):
        #     for j, lesson in enumerate(lessons_in_term):
        #         for assigned_mark in assigned_marks:
        #             mark = assigned_mark.mark
        #             if assigned_mark.student == student and mark.lesson == lesson:
        #                 data[i + 1][j + 2] = mark
        #                 assigned_marks.remove(assigned_mark)

        # students = [student.user.get_full_name() for student in students]
        # for i in range(1, len(data)):
        #     data[i][1] = students[i - 1]
        context = {"subjects": subjects,
                   # "dates": dates,
                   "marks": data,
                   # "choices": (str(i) for i in range(1, 5)),
                   # "term": term,
                   "current_grade": study_class,
                   "begin_study_year": study_class.year_begin.year,
                   "end_study_year": study_class.year_begin.year + 1
                   }
        # for key, value in MONTHS_IN_TERMS.items():
        #     term = list(filter(lambda mark: mark.lesson.date.month in value, marks))
        #     context[key] = get_subjects_marks_by_term(subjects, term)

        # average = []
        # if context["4_term"]:
        #     for i in range(len(subjects)):
        #         terms_marks = []
        #         for key in MONTHS_IN_TERMS.keys():
        #             terms_marks.append(context[key][i])
        #         average.append(sum(terms_marks) / len(terms_marks))
        # context["average"] = average
    else:
        context = {}
    return context


def get_elem_from_select(request, subjects, select_name):
    indx_class = request.POST.get(select_name)
    if indx_class:
        return subjects[int(indx_class)]
    return subjects[0]


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


def get_teacher_journal(request):
    teacher = ProfileTeacher.objects.select_related('subject').get(user=request.user)
    subject = teacher.subject
    study_class_subjects_lists = StudyClassSubjectsList.objects.filter(subject=subject)
    study_classes = [study_class_subjects_list.study_class for study_class_subjects_list in study_class_subjects_lists]
    if len(study_classes) > 0:
        study_class = get_elem_from_select(request, study_classes, "class_students")
        term = request.POST.get('choice')
        if not term:
            term = "1"
        data = get_marks_table(study_class, subject, teacher, term)
        context = {
            "dates": data[0],
            "marks": data[1:],
            "choices": (str(i) for i in range(1, 5)),
            "term": term,
            "grades": study_classes,
            "current_grade": study_class,
            "begin_study_year": study_class.year_begin.year,
            "end_study_year": study_class.year_begin.year + 1
        }
    else:
        context = {}
    return context


# def get_students_class_by_indx(request, students_classes):
#     indx_class = request.POST.get('class_students')
#     if indx_class:
#         return students_classes[int(indx_class)]
#     return students_classes[0]


def get_marks_table(study_class, subject, teacher, term):
    # dates = get_dates_lessons(term, student_class, subject)
    # subject_marks_term = get_lessons_marks_for_subject(subject, dates, student_class)
    # students = student_class.students.all()

    all_lessons_of_class_with_this_teacher = Lesson.objects.filter(teacher=teacher, study_class=study_class)
    if len(all_lessons_of_class_with_this_teacher) == 0:
        timetables = Timetable.objects.filter(teacher=teacher, study_class=study_class)
        if len(timetables) == 0:
            return {}
        else:
            for timetable in timetables:
                week_day = timetable.week_day

    lessons_in_term = [lesson for lesson in all_lessons_of_class_with_this_teacher
                       if lesson.date.month in MONTHS_IN_TERMS[term]]
    dates = [lesson.date for lesson in lessons_in_term]
    all_marks_of_class_with_this_teacher_in_this_term = Mark.objects.filter(lesson__in=lessons_in_term)
    classes_of_students = ClassStudents.objects.filter(study_class=study_class)
    students = [class_of_students.student for class_of_students in classes_of_students]
    assigned_marks = list(AssignedMark.objects.filter(mark__in=all_marks_of_class_with_this_teacher_in_this_term, subject=subject))


    data = [["" for _ in range(len(dates) + 2)] for _ in range(len(students) + 1)]
    data[0][2:] = dates
    data[0][1] = "ФИО"
    data[0][0] = "№"
    for i in range(1, len(data)):
        data[i][0] = i
        data[i][1] = students[i-1]

    for i, student in enumerate(students):
        for j, lesson in enumerate(lessons_in_term):
            for assigned_mark in assigned_marks:
                mark = assigned_mark.mark
                if assigned_mark.student == student and mark.lesson == lesson:
                    data[i+1][j+2] = mark
                    assigned_marks.remove(assigned_mark)

    students = [student.user.get_full_name() for student in students]
    for i in range(1, len(data)):
        data[i][1] = students[i - 1]
    return data


def get_dates_lessons(term, student_class, subject):
    schedules = student_class.timetable.all()
    days_of_week = []

    for schedule in schedules:
        if schedule.subjects.filter(subject=subject).exists():
            days_of_week.append(DAYS_OF_WEEK[schedule.day])

    months_in_term = get_months_in_term(term)
    dates = []
    calendar = Calendar()
    for month_in_term in months_in_term:
        if 9 <= month_in_term <= 12:
            study_year = 2023
        else:
            study_year = 2023 + 1
        for year, month, day, day_of_week in calendar.itermonthdays4(study_year, month_in_term):
            if day_of_week in days_of_week and month in months_in_term:
                dates.append(datetime.date(year, month, day))
    dates = list(OrderedDict.fromkeys(dates).keys())
    return dates


def get_months_in_term(term):
    return MONTHS_IN_TERMS[term + "_term"]


def get_lessons_marks_for_subject(subject, dates, student_class):
    subject_marks_all = student_class.marks.filter(subject=subject).select_related('student')
    subject_marks_term = []
    for date in dates:
        for mark in subject_marks_all:
            if mark.date.year == date.year and mark.date.month == date.month and mark.date.day == date.day:
                subject_marks_term.append(mark)
    return subject_marks_term


def get_students_timetable(request):
    student = ProfileStudent.objects.get(user=request.user)
    class_students = ClassStudents.objects.get(student=student)
    study_class = class_students.study_class
    timetables = Timetable.objects.filter(study_class=study_class)
    timetables_by_days_of_week = OrderedDict((key, []) for key in DAYS_OF_WEEK.keys())

    for timetable in timetables:
        for day in timetables_by_days_of_week.keys():
            if timetable.week_day == day:
                timetables_by_days_of_week[day].append(timetable)
                break
    return [(key, value) for key, value in timetables_by_days_of_week.items()]


    # schedules = Schedule.objects.filter(study_classes=student.grade).prefetch_related(
    #     Prefetch('subjects', queryset=SubjectInSchedule.objects.all().select_related('subject'))).only('subjects', 'day')


def get_teachers_timetable(request):
    teacher = ProfileTeacher.objects.get(user=request.user)
    timetables = Timetable.objects.filter(teacher=teacher)
    timetables_by_days_of_week = OrderedDict((key, []) for key in DAYS_OF_WEEK.keys())

    for timetable in timetables:
        for day in timetables_by_days_of_week.keys():
            if timetable.week_day == day:
                timetables_by_days_of_week[day].append(timetable)
                break
    return [(key, value) for key, value in timetables_by_days_of_week.items()]
    # subjects_in_schedules = SubjectInSchedule.objects.filter(schedules__in=teacher.timetable.all()).select_related('subject')
    # if subjects_in_schedules.count == 0:
    #     all_subjects_in_schedules = {"понедельник": [], "вторник": [], "среда": [], "четверг": [], "пятница": [],
    #                                  "суббота": []}
    #     for schedule in Schedule.objects.filter(study_classes__in=students_classes):
    #         subjects_in_shedules = schedule.subjects.filter(subject=subject)
    #         all_subjects_in_schedules[schedule.day.lower()].extend(subjects_in_shedules)
    #
    #     for schedule in teacher.timetable.all():
    #         schedule.subjects.set(all_subjects_in_schedules[schedule.day.lower()])
    #
    # return teacher.timetable.all().prefetch_related(
    #     Prefetch('subjects', subjects_in_schedules)
    # )


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