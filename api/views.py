from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import AttendanceSerializer, CourseSerializer, CourseViewSerializer, StudentSerializer, TeacherSerializer
from .models import Attendance, Course, Student, Teacher


# Create your views here.

# View all students
@api_view(['GET', 'POST'])
def students_details(request):
    if request.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)

# View a student and Register a student
@api_view(['GET', 'POST'])
def student(request, roll_no):
    if request.method == 'GET':
        try:
            student = Student.objects.get(pk = roll_no)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)
    elif request.method == 'POST':
        try:
            student = StudentSerializer(data=request.data)
            if student.is_valid():
                student.save()
            return Response(student.data)
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)
    elif request.method == 'PATCH':
        # To edit existng student
        pass

# View all Teachers
@api_view(['GET'])
def teachers_details(request):
    if request.method == 'GET':
        teacher = Teacher.objects.all()
        serializer = TeacherSerializer(teacher, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def teacher(request, teacher_id):
    if request.method == 'GET':
        try:
            teacher = Teacher.objects.get(pk=teacher_id)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)
    elif request.method == 'POST':
        try:
            teacher = TeacherSerializer(data=request.data)
            if teacher.is_valid():
                teacher.save()
            return Response(teacher.data)
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)

# View all courses
@api_view(['GET', 'POST'])
def courses_detail(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseViewSerializer(courses, many=True)
        return Response(serializer.data)

# View a course or Create a Course
@api_view(['GET', 'POST'])
def course(request, course_id):
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=course_id)
            serialzer = CourseViewSerializer(course)
            return Response(serialzer.data)
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)
    elif request.method == 'POST':
        try:
            course_name = request.data['course_name']
            course = Course(course_name=course_name)
            course.save()
            # Check if teacher is assigned to course
            if 'taught_by' in request.data:
                taught_by_id = request.data['taught_by']
                taught_by = Teacher.objects.get(pk=taught_by_id)
                course.taught_by = taught_by
            # Check if enrolled students list is passed
            if 'enrolled_students' in request.data:
                enrolled_students = request.data['enrolled_students']
                for student in enrolled_students:
                    s = Student.objects.get(pk=student)
                    course.enrolled_students.add(s)
            serialzer = CourseViewSerializer(course)
            return Response(serialzer.data)
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)
    elif request.method == 'PATCH':
        # To edit a existing course
        pass
    elif request.method == 'DELETE':
        try:
            course = Course.objects.get(pk=course_id)
            course.delete()
            return Response({"message": "Course Deleted"})
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)

# View and Mark attendance for a course lec
@api_view(['GET', 'POST'])
def attendance(request, course_id, lec_no):
    if request.method == 'GET':
        attendance = Attendance.objects.all().filter(course=course_id)
        serialzer = AttendanceSerializer(attendance, many=True)
        return Response(serialzer.data)
    elif request.method == 'POST':
        students = request.data
        for student in students:
            student_id = student['student']
            try:
                s = Student.objects.get(pk=student_id)
                course = Course.objects.get(pk=course_id)
                attendance = Attendance(
                    student_status=student['student_status'], lec_no=lec_no, student=s, course=course)
                attendance.save()
                serialzer = AttendanceSerializer(attendance)
                return Response(serialzer.data)
            except Exception as e:
                error = {'error': str(e)}
                return Response(error)
    elif request.method == 'PATCH':
        # To edit existing attendance
        pass
    elif request.method == 'DELETE':
        # To Delete attendance
        pass

# 2022-03-06T19:37:20.142275+05:30

# {
# "student": 2,
# "lec_no":  1,
# "student_status": false
# }