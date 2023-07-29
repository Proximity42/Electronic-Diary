from django.urls import path
from class_journal.views import AddMarkView, DiaryView, TimetableView, JournalView


urlpatterns = [
    path('', TimetableView.as_view(), name='timetable'),
    path('timetable/', TimetableView.as_view(), name='timetable'),
    path('journal/', JournalView.as_view(), name='journal'),
    path('diary/', DiaryView.as_view(), name='diary'),
    path('journal/add_mark', AddMarkView.as_view(), name='add_mark'),
]