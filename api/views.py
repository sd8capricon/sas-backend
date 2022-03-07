from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import AttendanceSerializer, CourseSerializer, CourseViewSerializer, StudentSerializer, TeacherSerializer
from .models import Attendance, Course, Student, Teacher


# Create your views here.

# Get all students and register a student
@api_view(['GET', 'POST'])
def student_details(request):
    if request.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        student = StudentSerializer(data=request.data)
        if student.is_valid():
            student.save()
        return Response(student.data)

# View Teachers


@api_view(['GET', 'POST'])
def teacher_details(request):
    if request.method == 'GET':
        teacher = Teacher.objects.all()
        serializer = TeacherSerializer(teacher, many=True)
        return Response(serializer.data)

# View all courses or Create a Course


@api_view(['GET', 'POST'])
def course(request):
    if request.method == 'GET':
        course = Course.objects.all()
        serialzer = CourseViewSerializer(course, many=True)
        return Response(serialzer.data)
    elif request.method == 'POST':
        try:
            course_name = request.data['course_name']
            taught_by_id = request.data['taught_by']
            taught_by = Teacher.objects.get(pk=taught_by_id)
            course = Course(course_name=course_name, taught_by=taught_by)
            course.save()
            serialzer = CourseViewSerializer(course)
            return Response(serialzer.data)
        except Exception as e:
            print(e)
            return HttpResponse(e)

# View and Mark attendance for a course


@api_view(['GET', 'POST'])
def attendance(request, course_id):
    if request.method == 'GET':
        attendance = Attendance.objects.all().filter(course=course_id)
        serialzer = AttendanceSerializer(attendance, many=True)
        return Response(serialzer.data)
    if request.method == 'POST':
        students = request.data
        for student in students:
            student_id = student['student']
            try:
                s = Student.objects.get(pk=student_id)
                course = Course.objects.get(pk=course_id)
                attendance = Attendance(
                    student_status=student['student_status'], lec_no=student['lec_no'], student=s, course=course)
                attendance.save()
                serialzer = AttendanceSerializer(attendance)
                return Response(serialzer.data)
            except Exception as e:
                print(e)
                return HttpResponse(e)

# 2022-03-06T19:37:20.142275+05:30

# {
# "student": 2,
# "lec_no":  1,
# "student_status": false
# }
