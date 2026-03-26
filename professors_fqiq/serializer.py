from rest_framework import serializers
from .models import Professor, Grade, Course, ProfessorCourse

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'