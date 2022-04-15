from rest_framework.decorators import api_view
from rest_framework.response import Response
from faculty.models import Faculty
from faculty.serializers import RegisterSerializer, DisplaySerializer


# Create your views here.
@api_view(['GET'])
def index(request):
    try:
        faculties = Faculty.objects.all()
        faculties = DisplaySerializer(faculties, many=True)
        return Response(faculties.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
def register(request):
    try:
        data = request.data
        faculty = RegisterSerializer(data=data)
        if faculty.is_valid():
            faculty.save()
            return Response(faculty.data)
        return Response(faculty.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['PATCH'])
def update():
    return Response('')


@api_view(['DELETE'])
def remove():
    return Response('')
