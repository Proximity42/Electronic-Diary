from django.test import TestCase
from class_journal.forms import NewMarkForm
from class_journal.models import StudentsClass
from users.models import BaseUser, ProfileStudent


class TestForms(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = BaseUser.objects.create_user(
            identifier='1000',
            password='test_pass',
            is_student=True,
        )
        students_class = StudentsClass.objects.create(number_grade=1)
        cls.student = ProfileStudent.objects.create(user=user, grade=students_class)

    def test_new_mark_form_valid_data(self):
        form = NewMarkForm(data={
            'value': 5,
            'student': self.student,
            'date': "2022-11-08"
        })

        self.assertTrue(form.is_valid())

    def test_new_mark_form_invalid_value(self):
        form = NewMarkForm(data={
            'value': '1',
            'student': self.student,
            'date': '2022-11-08'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_new_mark_form_invalid_student(self):
        form = NewMarkForm(data={
            'value': 5,
            'student': 'student1',
            'date': '2022-11-08'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_new_mark_form_invalid_date(self):
        form = NewMarkForm(data={
            'value': 5,
            'student': self.student,
            'date': '13-06-2022'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_new_mark_form_invalid_data(self):
        form = NewMarkForm(data={
            'value': '1',
            'student': 'self.student',
            'date': '08-11-2019'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)