from rest_framework import serializers
from .models import Student, Teacher, Course, Attendance

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('teacher_id', 'f_name', 'l_name')

class CourseViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    taught_by = TeacherSerializer()

    class Meta:
        model = Course
        fields = ('course_id', 'course_name', 'taught_by')

class AttendanceSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    student = StudentSerializer()

    class Meta:
        model = Attendance
        fields = ('date', 'student_status', 'student', 'course')