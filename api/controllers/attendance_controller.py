from django.db.models import Max

from api.serializers import AttendanceSerializer, StatSerializer
from api.models import Attendance, Course, Lec_Stat, Student


# View and Mark attendance for a course lec by id
def attendance(req, courseId, lec_no):
    if req.method == 'GET':
        try:
            no_of_students = Student.objects.count()
            course = Course.objects.get(pk=courseId)
            attendance = Attendance.objects.all().filter(course=courseId, lec_no=lec_no)
            lec = Lec_Stat.objects.get(course=courseId, lec_no=lec_no)
            statSerializer = StatSerializer(lec)
            statcpy = statSerializer.data
            statcpy['class_strength'] = no_of_students
            attenSerialzer = AttendanceSerializer(attendance, many=True)
            res = {
                'stat': statcpy,
                'attendance': attenSerialzer.data
            }
            return res
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'POST':
        students = req.data
        no_of_students = Student.objects.count()
        students_present = no_of_students
        absent_roll_nos = []
        for student in students:
            roll_no = student['student']
            absent_roll_nos.append(roll_no)        
        try:
            course = Course.objects.get(pk=courseId)
            for roll_no in range(1, no_of_students+1):
                s = Student.objects.get(pk=roll_no)
                attendance = Attendance(lec_no=lec_no, student=s, course=course)
                if roll_no in absent_roll_nos:
                    attendance.student_status=False
                    students_present-=1
                attendance.save()
        except Exception as e:
            error = {'error': str(e)}
            return error
        percentage = (students_present/no_of_students) * 100
        stat = Lec_Stat(course=course, lec_no=lec_no, students_present=students_present, attendance_percentage=percentage)
        stat.save()
        statSerializer = StatSerializer(stat)
        statcpy = statSerializer.data
        statcpy['class_strength'] = no_of_students
        return statcpy
    elif req.method == 'PATCH':
        students = req.data
        course = Course.objects.get(pk=courseId)
        stat = Lec_Stat.objects.get(course=course, lec_no=lec_no)
        students_present = stat.students_present
        for student in students:
            student_id = student['student']
            s = Student.objects.get(pk=student_id)
            attendance = Attendance.objects.get(lec_no=lec_no, student=s, course=course)
            if student['student_status'] != attendance.student_status: # Check if incoming status is different
                if student['student_status'] == True: # Incoming change is true ie student present then increment
                    students_present+=1 
                else: # Else incoming change is false ie student absent then decrement
                    students_present-=1
                attendance.student_status = student['student_status']
        no_of_students = Student.objects.count()
        percentage = (students_present/no_of_students) * 100
        stat.students_present = students_present
        stat.attendance_percentage = percentage
        stat.save()
        statSerializer = StatSerializer(stat)
        statcpy = statSerializer.data
        statcpy['class_strength'] = no_of_students
        return statcpy

def get_last_lecnum(req, course_id):
    if req.method == 'GET':
        try:
            lecs = Lec_Stat.objects.filter(course=course_id).aggregate(max=Max('lec_no'))
            lec_no = lecs['max']
            return {
                'last_lec': lec_no
            }
        except Exception as e:
            error = {'error': str(e)}
            return error