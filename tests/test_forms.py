from django.test import TestCase
from class_journal.forms import NewMarkForm
from class_journal.models import StudentsClass
from users.models import BaseUser, ProfileStudent


class TestForms(TestCase):

    def setUp(self) -> None:
        user = BaseUser.objects.create_user(
            identifier='1000',
            password='test_password1',
            last_name='Иванов',
            first_name='Иван',
            middle_name='Иванович',
            is_student=True,
        )
        students_class = StudentsClass.objects.create(number_grade=1)
        self.student = ProfileStudent.objects.create(user=user, grade=students_class)

    def test_new_mark_form_valid_data(self) -> None:
        form = NewMarkForm(data={
            'value': 5,
            'student': self.student,
            'date': "2022-11-08"
        })

        self.assertTrue(form.is_valid())