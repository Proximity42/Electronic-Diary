from django import forms
from class_journal.models import Mark


# class NewMarkForm(forms.ModelForm):
#
#     class Meta:
#         model = Mark
#         fields = ["value"]
#         # help_texts = {'date': 'Введите дату проставления оценки в формате "день.месяц.год (Пример. 15.04.23)"'}

class AddMarkForm(forms.Form):
    MARK_VALUE_CHOICES = [(i, f"{i}") for i in range(2, 6)]

    value = forms.ChoiceField(choices=MARK_VALUE_CHOICES)
