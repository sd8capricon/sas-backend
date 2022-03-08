from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import AttendanceSerializer, CourseSerializer, CourseViewSerializer, StatSerializer, StudentSerializer, TeacherSerializer
from .models import Attendance, Course, Lec_Stat, Student, Teacher


# Create your views here.

# View all students
@api_view(['GET'])
def students_details(request):
    if request.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)

# View a student and Register a student
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
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

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
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
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

# View a course or Create a Course
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
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
            course.save()
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

# View and Mark attendance for a course lec by id
@api_view(['GET', 'POST', 'PATCH'])
def attendance(request, course_id, lec_no):
    if request.method == 'GET':
        attendance = Attendance.objects.all().filter(course=course_id, lec_no=lec_no)
        serialzer = AttendanceSerializer(attendance, many=True)
        return Response(serialzer.data)
    elif request.method == 'POST':
        students = request.data
        no_of_students = Student.objects.count()
        students_present = no_of_students
        absent_roll_nos = []
        for student in students:
            roll_no = student['student']
            absent_roll_nos.append(roll_no)
        try:
            course = Course.objects.get(pk=course_id)
            for roll_no in range(1, no_of_students+1):
                s = Student.objects.get(pk=roll_no)
                attendance = Attendance(lec_no=lec_no, student=s, course=course)
                if roll_no in absent_roll_nos:
                    attendance.student_status=False
                    students_present-=1
                else:
                    attendance.student_status=True
                attendance.save()
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)
        stat = Lec_Stat(course_id=course, lec_no=lec_no, students_present=students_present)
        stat.save()
        statSerializer = StatSerializer(stat)
        return Response(statSerializer.data)
    elif request.method == 'PATCH':
        students = request.data
        course = Course.objects.get(pk=course_id)
        stat = Lec_Stat.objects.filter(course_id=course, lec_no=lec_no)
        students_present = stat.students_present
        for student in students:
            student_id = student['student']
            s = Student.objects.get(pk=student_id)
            attendance = Attendance.objects.filter(lec_no=lec_no, student=s, course=course)
            if student['student_status'] != s.student_status: # Check if incoming status is different
                if student['student_status'] == True: # Incoming change is true ie student present then increment
                    students_present+=1 
                else: # Else incoming change is false ie student absent then decrement
                    students_present-=1
                s.student_status = student['student_status']

# Email to defaultors
@api_view(['POST'])
def email_defaultors(request):
    if request.method == 'POST':
        defaultors = Student.objects.filter(total_attendance_percentage__lt=70)
        for defaultor in request.data['defaultors']:
            d = Student.objects.get(pk=defaultor)
            defaultors.append(d.email)
        send_mail(
            'Defaultor',
            'You are recieving this mail for being a defaultor',
            'from@example.com',
            defaultors,
            fail_silently=False,
        )