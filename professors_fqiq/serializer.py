from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Professor, Grade, Course, ProfessorCourse

User = get_user_model()

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class ProfessorCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorCourse
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


