from re import search
from django.db import IntegrityError
from api.serializers import StudentSerializer
from api.models import Attendance, Course, Lec_Stat, Student

# View all students
def students_details(req):
    if req.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return serializer.data

# View a student and Register a student
def student(req, roll_no):
    if req.method == 'GET':
        try:
            student = Student.objects.get(pk = roll_no)
            serializer = StudentSerializer(student)
            return serializer.data
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'POST':
        try:
            data = req.data
            s = Student.objects.filter(pk=data['roll_no']).count()
            if s>0:
                return {'error': 'Roll Number already assigned'}
            student = Student(roll_no=data['roll_no'], f_name=data['f_name'], l_name=data['l_name'], email=data['email'])
            student.save()
            serializer = StudentSerializer(student)
            return serializer.data
        except IntegrityError as e:
            error = {'error': 'Email is already in use'}
            return error
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'PATCH':
        try:
            data = req.data
            student = Student.objects.get(pk=roll_no)
            student.f_name = data['f_name']
            student.l_name = data['l_name']
            student.email = data['email']
            student.save()
            lecs = Lec_Stat.objects.all().count()
            cal_total_attendance_percentage
            student_total_attendance_percentage(student, lecs)
            serializer = StudentSerializer(student)
            return serializer.data
        except IntegrityError as e:
            error = {'error': 'Email is already in use'}
            return error
        except Exception as e:
            error = {'error': str(e)}
            return error
        pass
    elif req.method == 'DELETE':
        try:
            s = Student.objects.get(pk=roll_no)
            s.delete()
            return {"message": "Student Removed"}
        except Exception as e:
            error = {'error': str(e)}
            return error

# Get Student's Total Attendance
def cal_total_attendance_percentage(req):
    if req.method == 'GET':
        try:
            students = Student.objects.all()
            lecs = Lec_Stat.objects.all().count()
            for student in students:
                student_total_attendance_percentage(student, lecs)
            return {'message': 'Student Attendance Percentages calculated'}
        except Exception as e:
            return {'error': str(e)}

def student_total_attendance_percentage(student, lecs):
    # Getting all attendances where student is present
    a = Attendance.objects.filter(student=student, student_status=True).count()
    student.total_attendance_percentage = "{:.2f}".format((a/lecs) * 100) if lecs!=0 else 0
    student.save()

# Get Student's Course Attendance
def student_course_attendance_percentage(student_roll_no, course_id):
    try:    
        s = Student.objects.get(pk=student_roll_no)
        c = Course.objects.filter(course_id=course_id)
        # Getting all attendances of a student for a course
        a = Attendance.objects.filter(student=student, course=c, student_status=True).count()
        # Getting count of all lecs of a course
        l = Lec_Stat.objects.filter(course=c).count()
        percentage = (a/l) * 100
        res = {
            'lecs present': a,
            'lecs absent': l-a,
            'Student Course Attendance': percentage
        }
        return res
    except Exception as e:
        error = {'error': str(e)}
        return error