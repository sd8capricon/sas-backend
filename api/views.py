from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import AttendanceSerializer, CourseSerializer, StudentSerializer, TeacherSerializer
from .models import Attendance, Course, Student, Teacher


# Create your views here.

@api_view(['GET', 'POST'])
def student_details(request):
    if request.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        student = StudentSerializer(data = request.data)
        if student.is_valid():
            student.save()
        return Response(student.data)

@api_view(['GET', 'POST'])
def teacher_details(request):
    if request.method == 'GET':
        teacher = Teacher.objects.all()
        serializer = TeacherSerializer(teacher, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def course(request):
    if request.method == 'GET':
        course = Course.objects.all()
        serialzer = CourseSerializer(course, many = True)
        return Response(serialzer.data)
    elif request.method == 'POST':
        course = CourseSerializer(data = request.data)
        if course.is_valid():
            course.save()
        return Response(course.data)


@api_view(['GET', 'POST'])
def attendance(request):
    if request.method == 'GET':
        attendance = Attendance.objects.all()
        serialzer = AttendanceSerializer(attendance, many = True)
        return Response(serialzer.data)
    if request.method == 'POST':
        serialzer = AttendanceSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
        else:
            print(serialzer.errors)
            return Response({"error": "err"})
        return Response(serialzer.data)

# {
# "student_roll_no": 2,
# "course":  2,
# "student_status": false
# }