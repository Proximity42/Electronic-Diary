from collections import namedtuple
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from class_journal.models import StudentsClass, Subject
from users.models import ProfileStudent, ProfileTeacher


BaseUser = get_user_model()

ы
class TestViews(TestCase):
    ADD_MARK_NAME = 'add_mark'
    JOURNAL_NAME = 'journal'
    TIMETABLE_NAME = 'timetable'
    LOGIN_NAME = 'login'
    STATUS_CODE_OK = 200

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='Русский язык')
        students_class = StudentsClass.objects.create(number_grade=1)
        cls.user_student = BaseUser.objects.create_user(
            identifier='1000',
            password='test_pass1',
            is_student=True,
        )
        student = ProfileStudent.objects.create(user=cls.user_student, grade=students_class)
        cls.authorized_client_student = Client()
        cls.authorized_client_student.force_login(cls.user_student)

        cls.user_teacher = BaseUser.objects.create_user(
            identifier='2000',
            password='test_pass2',
            is_teacher=True,
        )
        teacher = ProfileTeacher.objects.create(user=cls.user_teacher, study_class=students_class, subject=subject)
        cls.authorized_client_teacher = Client()
        cls.authorized_client_teacher.force_login(cls.user_teacher)

        cls.clients = (cls.authorized_client_teacher, cls.authorized_client_student)

        TemplateNames = namedtuple('TemplateNames', 'TeacherTemplate StudentTemplate')
        cls.template_names = {
            cls.JOURNAL_NAME: TemplateNames('teacher_journal.html', 'journal.html'),
            cls.TIMETABLE_NAME: TemplateNames('teacher_timetable.html', 'timetable.html'),
            cls.LOGIN_NAME: TemplateNames('login.html', 'login.html'),
        }

    def test_GET(self):
        for name in self.template_names.keys():
            for client in self.clients:
                with self.subTest():
                    response = self._make_response_for_GET(client, name)
                    self.assertEqual(response.status_code, self.STATUS_CODE_OK)

    def test_pages_uses_correct_template(self):
        for name, templates in self.template_names.items():
            for client, template in zip(self.clients, templates):
                with self.subTest():
                    response = self._make_response_for_GET(client, name)
                    self.assertTemplateUsed(response, template)

    def test_add_mark(self):
        response = self._make_response_for_GET(self.authorized_client_teacher, self.ADD_MARK_NAME)
        self.assertEqual(response.status_code, self.STATUS_CODE_OK)
        self.assertTemplateUsed(response, 'add_mark.html')

    def test_profile(self):
        for client, pk in zip(self.clients, (self.user_student.pk, self.user_teacher.pk)):
            response = self._make_response_for_GET(client, f'/profile/{pk}', False)
            self.assertEqual(response.status_code, self.STATUS_CODE_OK)
            self.assertTemplateUsed(response, 'profile.html')

    def test_journal_POST(self):
        response = self.authorized_client_teacher.post(reverse(self.JOURNAL_NAME))
        self.assertEqual(response.status_code, self.STATUS_CODE_OK)

    @staticmethod
    def _make_response_for_GET(client, url_name, is_reverse=True):
        if is_reverse:
            return client.get(reverse(url_name))
        return client.get(url_name)

    # TODO: Написать тест на POST запрос к add_mark
