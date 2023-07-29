from django.contrib.auth.views import LoginView, LogoutView
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from class_journal.views import TimetableView, JournalView, AddMarkView, DiaryView
from users.views import UserProfileView


class TestURLs(SimpleTestCase):

    def test_url_resolves(self):
        url_names_views = {
            'login': LoginView,
            'logout': LogoutView,
            'timetable': TimetableView,
            'journal': JournalView,
            'add_mark': AddMarkView,
            'diary': DiaryView,
            'profile': UserProfileView
        }

        for name, view in url_names_views.items():
            with self.subTest():
                self.assertEqual(resolve(reverse(name)).func.view_class, view)