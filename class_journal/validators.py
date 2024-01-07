from django.core.exceptions import ValidationError
from datetime import date
from ElectronicDiary.settings import BEGIN_STUDY_YEAR


# def borders_date_validate(date):
#     if date.year == date.today().year and date.month < 9:
#         raise ValidationError("Оценки должны проставляться, начиная с сентября.")
#     if date.year == date.today().year + 1 and date.month > 5:
#         raise ValidationError("Оценки должны проставляться, заканчивая маем.")
