from collections import namedtuple
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse
from class_journal.models import StudentsClass, Subject
from users.models import ProfileStudent, ProfileTeacher


BaseUser = get_user_model()


class TestViews(TestCase):
    ADD_MARK_NAME = 'add_mark'
    JOURNAL_NAME = 'journal'
    TIMETABLE_NAME = 'timetable'
    LOGIN_NAME = 'login'
    LOGOUT_NAME = 'logout'
    PROFILE_NAME = 'profile'


    def setUp(self):
        subject = Subject.objects.create(title='Русский язык')
        students_class = StudentsClass.objects.create(number_grade=1)
        group_students = Group.objects.create(name='Ученики')
        group_teachers = Group.objects.create(name='Учителя')
        user_student = BaseUser.objects.create_user(
            identifier='1000',
            password='test_password1',
            last_name='Иванов',
            first_name='Иван',
            middle_name='Иванович',
            is_student=True,
        )
        user_student.groups.add(group_students)

        student = ProfileStudent.objects.create(user=user_student, grade=students_class)
        self.authorized_client_student = Client()
        self.authorized_client_student.force_login(user_student)

        user_teacher = BaseUser.objects.create_user(
            identifier='2000',
            password='test_password2',
            last_name='Вишневская',
            first_name='Вера',
            middle_name='Давидовна',
            is_teacher=True,
        )
        user_teacher.groups.add(group_teachers)
        teacher = ProfileTeacher.objects.create(user=user_teacher, study_class=students_class, subject=subject)
        self.authorized_client_teacher = Client()
        self.authorized_client_teacher.force_login(user_teacher)


    @staticmethod
    def get_response(client, url_name):
        return client.get(reverse(url_name))

    def test_add_mark_GET(self):
        response = self.get_response(self.authorized_client_teacher, self.ADD_MARK_NAME)
        self.assertEqual(response.status_code, 200)

    def test_add_mark_correct_templates(self):
        response = self.get_response(self.authorized_client_teacher, self.ADD_MARK_NAME)
        self.assertTemplateUsed(response, 'add_mark.html')

    def test_pages_uses_correct_template(self):
        TemplateNames = namedtuple('TemplateNames', 'TeacherTemplate StudentTemplate')

        template_pages_names = {
            self.JOURNAL_NAME: TemplateNames('teacher_journal.html', 'journal.html'),
            self.TIMETABLE_NAME: TemplateNames('teacher_timetable.html', 'timetable.html'),
            self.LOGIN_NAME: TemplateNames('login.html', 'login.html'),
            self.LOGOUT_NAME: TemplateNames('logout.html', 'logout.html'),
            self.PROFILE_NAME: TemplateNames('profile.html', 'profile.html'),
        }

        for name, template in template_pages_names.items():
            with self.subTest():
                response = self.get_response(self.authorized_client_teacher, name)
                self.assertTemplateUsed(response, template.TeacherTemplate)

            with self.subTest():
                response = self.get_response(self.authorized_client_student, name)
                self.assertTemplateUsed(response, template.StudentTemplate)

    def test_GET(self):
        clients = (self.authorized_client_student, self.authorized_client_teacher)
        url_names = (self.JOURNAL_NAME, self.TIMETABLE_NAME, self.LOGIN_NAME, self.LOGOUT_NAME, self.PROFILE_NAME)

        for client in clients:
            for name in url_names:
                with self.subTest():
                    response = self.get_response(client, name)
                    self.assertEqual(response.status_code, 200)

    # def test_add_mark_POST_adds_new_mark(self):
    #     response = self.authorized_client_teacher.post(reverse('add_mark'))
