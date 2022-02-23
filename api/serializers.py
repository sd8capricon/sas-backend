from rest_framework import serializers
from .models import Student, Teacher, Course, Attendance

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    #enrolled_students = StudentSerializer()
    class Meta:
        model = Course
        fields = '__all__'

class AttendanceSerialzer(serializers.ModelSerializer):
    course = CourseSerializer()
    student = StudentSerializer()
    class Meta:
        model = Attendance
        fields = ('date', 'course', 'student')