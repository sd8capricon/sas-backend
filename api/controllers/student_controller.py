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
            student = StudentSerializer(data=req.data)
            if student.is_valid():
                student.save()
            return student.data
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'PATCH':
        # To edit existng student
        pass

# Get Student's Total Attendance
def cal_total_attendance_percentage(req):
    if req.method == 'GET':
        try:
            no_of_students = Student.objects.count()
            lecs = Lec_Stat.objects.all().count()
            for roll_no in range(1, no_of_students+1):
                student_total_attendance_percentage(roll_no, lecs)
            return {'message': 'Student Attendance Percentages calculated'}
        except Exception as e:
            return {'error': str(e)}

def student_total_attendance_percentage(student_roll_no, lecs):
    s = Student.objects.get(pk=student_roll_no)
    # Getting all attendances where student is present
    a = Attendance.objects.filter(student=s, student_status=True).count()
    percentage = (a/lecs) * 100
    s.total_attendance_percentage = percentage
    s.save()
    res = {
        'lecs present': a,
        'lecs absent': lecs-a,
        'percentage attendance': percentage
    }
    # except Exception as e: 
    #     error = {'error': str(e)}
    #     return error 

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