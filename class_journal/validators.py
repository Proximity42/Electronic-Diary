from django.core.exceptions import ValidationError
from ElectronicDiary.settings import BEGIN_STUDY_YEAR


def borders_date_validate(date):
    if date.year == BEGIN_STUDY_YEAR and date.month < 9:
        raise ValidationError("Оценки должны проставляться, начиная с сентября.")
    if date.year == BEGIN_STUDY_YEAR + 1 and date.month > 5:
        raise ValidationError("Оценки должны проставляться, заканчивая маем.")
