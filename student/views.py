import django.core.exceptions as de
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.views import student
from student.models import Student
from student.serializers import StudentSerializer


# Create your views here.
@api_view(['GET'])
def index(request):
    try:
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error':str(e)}, status=400)


@api_view(['GET'])
def read(request, roll_no):
    try:
        student = Student.objects.get(pk=roll_no)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except de.ObjectDoesNotExist as e:
        return Response({'error': 'Roll Number not in system'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
def enroll(request):
    try:
        data = request.data
        student = StudentSerializer(data=data)
        if student.is_valid():
            student.save()
            return Response(student.data)
        return Response(student.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['PATCH'])
def update(request, roll_no):
    try:
        data = request.data
        s = Student.objects.get(pk=roll_no)
        student = StudentSerializer(instance=s,data=data,partial=True)
        if student.is_valid():
            student.save()
            return Response(student.data)
        return Response(student.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET', 'DELETE'])
def remove(request, roll_no):
    if request.method == 'GET':
        try:
            s = Student.objects.get(pk=roll_no)
            student = StudentSerializer(instance=s)
            return Response(student.data)
        except de.ObjectDoesNotExist as e:
            return Response({'error': 'Roll Number not in system'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    if request.method == 'DELETE':
        try:
            s = Student.objects.get(pk=roll_no)
            student = StudentSerializer(instance=s)
            s.delete()
            return Response({'message': 'success', 'student':student.data})
        except de.ObjectDoesNotExist as e:
            return Response({'error': 'Roll Number not in system'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


# TODO: cal total attendance