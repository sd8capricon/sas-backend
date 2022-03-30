import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils.emailUtil import email_defaultors
from api.controllers import auth_controllers, attendance_controller, course_controllers, student_controller, teacher_controller

# Create your views here.

# Login Route
@api_view(['POST'])
def login(req):
    res = auth_controllers.login(req)
    return Response(res)

# To verify token
@api_view(['POST'])
def verifyToken(req):
    res = auth_controllers.verifyToken(req)
    return Response(res)

# View all students
@api_view(['GET'])
def students_details(req):
    res = student_controller.students_details(req)
    if 'error' in res:
        return Response(res, status=400)
    return Response(res)

# View a student and Register a student
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def student(req, roll_no):
    res = student_controller.student(req, roll_no)
    if 'error' in res:
        return Response(res, status=400)
    return Response(res)

# Cal student total attendance percentage
@api_view(['GET'])
def cal_total_attendance_percentage(req):
    res = student_controller.cal_total_attendance_percentage(req)
    return Response(res)

# View all Teachers
@api_view(['GET'])
def teachers_details(req):
    res = teacher_controller.teachers_details(req)
    if 'error' in res:
        return Response(res, status=400)
    return Response(res)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def teacher(req, teacher_id):
    res = teacher_controller.teacher(req, teacher_id)
    if 'error' in res:
        return Response(res, status=400)
    return Response(res)

# View all courses
@api_view(['GET', 'POST'])
def courses_detail(req):
    res = course_controllers.courses_detail(req)
    if 'error' in res:
        return Response(res, status=400)
    return Response(res)

# View a course or Create a Course
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def course(req, course_id):
    res = course_controllers.course(req, course_id)
    return Response(res)

# Get avg Course Attendance Percentage and stats
@api_view(['GET'])
def course_lec_stats(req, course_id):
    res = course_controllers.course_lec_stats(req, course_id)
    return Response(res)

# View and Mark attendance for a course lec by id
@api_view(['GET', 'POST', 'PATCH'])
def attendance(req, courseId, lec_no):
    res = attendance_controller.attendance(req, courseId, lec_no)
    if 'error' in res:
        return Response(res, status=400)
    return Response(res)

@api_view(['GET'])
def get_last_lecnum(req, course_id):
    res = attendance_controller.get_last_lecnum(req, course_id)
    if 'error' in res:
        return Response(res, status=400)
    return Response(res)

# Email to defaultors
@api_view(['POST'])
def email_defaultors(req):
    res = email_defaultors(req)
    return Response(res)