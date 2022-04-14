from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['GET'])
def index(request):
    print(request)
    return Response('GET all')


@api_view(['GET'])
def read(request, roll_no):
    return Response('GET')


@api_view(['POST'])
def enroll(request):
    print(request.data)
    return Response('POST')


@api_view(['PATCH'])
def update(request, roll_no):
    print(request.data)
    return Response('PATCH')


@api_view(['DELETE'])
def remove(request, roll_no):
    print(request.data)
    return Response('DELETE')
