from dataclasses import field
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
    #enrolled_students = serializers.SerializerMethodField('get_enrolled_students')
    enrolled_students = StudentSerializer()

    class Meta:
        model = Course
        # fields = ['course_id', 'course_name', 'course_name', 'taught_by', 'enrolled_students']
        fields = '__all__'

    # def get_enrolled_students(self, course):
    #     enrolled_students = course.enrolled_students.f_name
    #     return enrolled_students

class AttendanceSerialzer(serializers.ModelSerializer):

    course_id = serializers.SerializerMethodField('get_course_id')
    course_name = serializers.SerializerMethodField('get_course_name')
    course_taught_by_fname = serializers.SerializerMethodField('get_course_taught_by_fname')
    course_taught_by_lname = serializers.SerializerMethodField('get_course_taught_by_lname')
    student_fname = serializers.SerializerMethodField('get_student_firstname')
    student_lname = serializers.SerializerMethodField('get_student_lastname')
    
    class Meta:
        model = Attendance
        fields = ['date', 'student_roll_no', 'student_fname', 'student_lname', 'student_status', 'course_id', 'course_name', 'course_taught_by_fname', 'course_taught_by_lname']

    def get_course_id(self, attendance):
        course_id = attendance.course.course_id
        return course_id

    def get_course_name(self, attendance):
        course_name = attendance.course.course_name
        return course_name

    def get_course_taught_by_fname(self, attendance):
        course_taught_by = attendance.course.taught_by.f_name
        return course_taught_by

    def get_course_taught_by_lname(self, attendance):
        course_taught_by = attendance.course.taught_by.l_name
        return course_taught_by
    
    def get_student_firstname(self, attendance):
        fname = attendance.student_roll_no.f_name
        return fname

    def get_student_lastname(self, attendance):
        lname = attendance.student_roll_no.l_name
        return lname
