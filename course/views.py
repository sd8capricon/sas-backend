from functools import partial
from rest_framework.decorators import api_view
from rest_framework.response import Response
from course.models import Course
from faculty.models import Faculty
from course.serializers import CourseSerializer


# Create your views here.
@api_view(['GET'])
def index(request):
    c = Course.objects.all()
    course = CourseSerializer(c, many=True)
    return Response(course.data)


@api_view(['PATCH'])
def update(request, course_id):
    try:
        data = request.data
        c = Course.objects.get(pk=course_id)
        if 'assign' in data:
            faculties = data['assign']
            for faculty in faculties:
                f = Faculty.objects.get(pk=faculty)
                c.taught_by.add(f)
        if 'unassign' in data:
            faculties = data['unassign']
            for faculty in faculties:
                f = Faculty.objects.get(pk=faculty)
                c.taught_by.remove(f)
        c.save()
        course = CourseSerializer(c)
        return Response(course.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
