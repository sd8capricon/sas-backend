from rest_framework import serializers
from .models import Lec_Stat, Student, Teacher, Course, Attendance

class StudentSerializer(serializers.ModelSerializer):
    # enrolled_courses = CourseViewSerializer()
    
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('teacher_id', 'f_name', 'l_name')

class CourseViewSerializer(serializers.ModelSerializer):
    enrolled_students = StudentSerializer(many=True)
    taught_by = TeacherSerializer()
    class Meta:
        model = Course
        fields = ('course_id', 'course_name', 'taught_by', 'enrolled_students')

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
        fields = ('date', 'lec_no', 'student_status', 'student', 'course')

class StatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lec_Stat
        fields = '__all__'