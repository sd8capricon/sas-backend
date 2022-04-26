from pyexpat import model
from rest_framework import serializers
from course.models import Course
from faculty.serializers import FacultyDisplaySerializer
from student.serializers import StudentSerializer


# TODO: Create Serializers

class CourseSerializer(serializers.ModelSerializer):
    enrolled_students = StudentSerializer(many=True)
    taught_by = FacultyDisplaySerializer(many=True)

    class Meta:
        model = Course
        fields = ['course_id', 'course_name',
                  'course_sem', 'enrolled_students', 'taught_by']
