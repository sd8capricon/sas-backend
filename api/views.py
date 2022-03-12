from django.core.mail import send_mail

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import AttendanceSerializer, CourseSerializer, CourseViewSerializer, StatSerializer, StudentSerializer, TeacherSerializer, TeacherViewSerializer
from api.models import Attendance, Course, Lec_Stat, Student, Teacher

from api.controllers import auth_controllers, attendance_controller, course_controllers, student_controller, teacher_controller

# Create your views here.

# Login Route
@api_view(['POST'])
def login(request):
    res = auth_controllers.login(request)
    return Response(res)

# To verify token
@api_view(['POST'])
def verifyToken(request):
    res = auth_controllers.verifyToken(request)
    return Response(res)

# View all students
@api_view(['GET'])
def students_details(request):
    res = student_controller.students_details(request)
    return Response(res)

# View a student and Register a student
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def student(request, roll_no):
    res = student_controller.student(request, roll_no)
    return Response(res)

# View all Teachers
@api_view(['GET'])
def teachers_details(request):
    res = teacher_controller.teachers_details(request)
    return Response(res)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def teacher(request, teacher_id):
    res = teacher_controller.teacher(request, teacher_id)
    return Response(res)

# View all courses
@api_view(['GET', 'POST'])
def courses_detail(request):
    res = course_controllers.courses_detail(request)
    return Response(res)

# View a course or Create a Course
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def course(request, course_id):
    res = course_controllers.course(request, course_id)
    return Response(res)


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