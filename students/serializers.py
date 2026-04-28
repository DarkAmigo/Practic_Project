from rest_framework import serializers
from .models import Student, Enrollment

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'major']

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source='student.__str__',
        read_only=True
    )

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'term']
