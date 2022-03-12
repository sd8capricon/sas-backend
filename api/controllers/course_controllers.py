from django.db.models import Sum

from api.serializers import CourseSerializer, CourseViewSerializer, StatSerializer
from api.models import Course, Lec_Stat, Student, Teacher

def courses_detail(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return serializer.data

def course(request, course_id):
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=course_id)
            serialzer = CourseViewSerializer(course)
            return serialzer.data
        except Exception as e:
            error = {'error': str(e)}
            return error
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
            return serialzer.data
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif request.method == 'PATCH':
        # To edit a existing course
        pass
    elif request.method == 'DELETE':
        try:
            course = Course.objects.get(pk=course_id)
            course.delete()
            return {"message": "Course Deleted"}
        except Exception as e:
            error = {'error': str(e)}
            return error

def course_lec_stats(request, course_id):
    if request.method == 'GET':
        try:
            c = Course.objects.get(pk=course_id)
            lecs = Lec_Stat.objects.filter(course=c)
            lecCount = lecs.count()
            if lecCount!=0:
                atten_sum = Lec_Stat.objects.all().aggregate(sum=Sum('attendance_percentage'))
                avg_percentage_attendace = atten_sum['sum']/lecCount
                statSerializer = StatSerializer(lecs, many=True)
                statcpy = statSerializer.data
                for stat in statcpy:
                    stat.pop('course')
                res = {
                    'course_stats': statcpy,
                    'avg_course_attendance': avg_percentage_attendace
                }
                return res
            else:
                return {'error': 'No lectures found'}
        except Exception as e:
            error = {'error': str(e)}
            return error