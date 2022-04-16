from rest_framework.decorators import api_view
from rest_framework.response import Response
from course.models import Course


# Create your views here.
@api_view(['GET'])
def index():
    c = Course.objects.all()
    
    return Response('All courses')
