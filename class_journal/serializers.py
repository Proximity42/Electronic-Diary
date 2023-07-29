from rest_framework.serializers import ModelSerializer

from class_journal.models import Subject, Mark
from users.models import ProfileStudent, ProfileTeacher


class SubjectsSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ProfileStudentsSerializer(ModelSerializer):
    class Meta:
        model = ProfileStudent
        fields = '__all__'


class ProfileTeachersSerializer(ModelSerializer):
    class Meta:
        model = ProfileTeacher
        fields = '__all__'


class MarkSerializer(ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'