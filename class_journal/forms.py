from django import forms
from class_journal.models import Mark


class NewMarkForm(forms.ModelForm):

    class Meta:
        model = Mark
        fields = ["value", "student", "date"]
        help_texts = {'date': 'Введите дату проставления оценки в формате "день.месяц.год (Пример. 15.04.23)"'}
