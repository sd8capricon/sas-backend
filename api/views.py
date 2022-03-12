import hashlib
import os

from django.http import HttpResponse
from django.core.mail import send_mail

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import AttendanceSerializer, CourseSerializer, CourseViewSerializer, StatSerializer, StudentSerializer, TeacherSerializer, TeacherViewSerializer
from api.models import Attendance, Course, Lec_Stat, Student, Teacher

from api.controllers import auth_controllers, attendance_controller, course_controllers

# Create your views here.

# Login Route
@api_view(['POST'])
def login(request):
    res = auth_controllers.login(request)
    return res

# To verify token
@api_view(['POST'])
def verifyToken(request):
    res = auth_controllers.verifyToken(request)
    return res

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
        serializer = TeacherViewSerializer(teacher, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def teacher(request, teacher_id):
    if request.method == 'GET':
        try:
            teacher = Teacher.objects.get(pk=teacher_id)
            serializer = TeacherViewSerializer(teacher)
            return Response(serializer.data)
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)
    elif request.method == 'POST':
        try:
            data = request.data
            password = (os.environ.get('PASS_SALT')+data['password']).encode('utf-8')
            h = hashlib.sha256(password).hexdigest()
            t = Teacher(username=data['username'], password=h, f_name=data['f_name'], l_name=data['l_name'])
            t.save()
            serializer = TeacherViewSerializer(t)
            return Response(serializer.data)
        except Exception as e:
            error = {'error': str(e)}
            return Response(error)

# View all courses
@api_view(['GET', 'POST'])
def courses_detail(request):
    res = course_controllers.courses_detail(request)
    return res

# View a course or Create a Course
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def course(request, course_id):
    res = course_controllers.course(request, course_id)
    return res


# View and Mark attendance for a course lec by id
@api_view(['GET', 'POST', 'PATCH'])
def attendance(request, courseId, lec_no):
    res = attendance_controller.attendance(request, courseId, lec_no)
    return Response(res)


# Get avg Course Attendance Percentage and stats
@api_view(['GET'])
def course_lec_stats(request, course_id):
    res = course_controllers.course_lec_stats(request, course_id)
    return Response(res)


# Get Student's Total Attendance
def student_total_attendance_percentage(student_roll_no):
    try:
        s = Student.objects.get(pk=student_roll_no)
        # Getting all attendances where student is present
        a = Attendance.objects.filter(student=s, student_status=True).count()
        # Getting all lecs
        l = Lec_Stat.objects.all().count()
        percentage = (a/l) * 100
        s.total_attendane_percentage = percentage
        s.save()
        res = {
            'lecs present': a,
            'lecs absent': l-a,
            'percentage attendance': percentage
        }
    except Exception as e: 
        error = {'error': str(e)}
        return Response(error) 

# Get Student's Course Attendance
def student_course_attendance_percentage(student_roll_no, course_id):
    try:    
        s = Student.objects.get(pk=student_roll_no)
        c = Course.objects.filter(course_id=course_id)
        # Getting all attendances of a student for a course
        a = Attendance.objects.filter(student=student, course=course, student_status=True).count()
        # Getting count of all lecs of a course
        l = Lec_Stat.objects.filter(course=course).count()
        percentage = (a/l) * 100
        res = {
            'lecs present': a,
            'lecs absent': l-a,
            'Student Course Attendance': percentage
        }
        return Response(res)
    except Exception as e:
        error = {'error': str(e)}
        return Response(error)

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