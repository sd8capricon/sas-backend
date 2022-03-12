from api.serializers import StudentSerializer
from api.models import Student

# View all students
def students_details(request):
    if request.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return serializer.data

# View a student and Register a student
def student(request, roll_no):
    if request.method == 'GET':
        try:
            student = Student.objects.get(pk = roll_no)
            serializer = StudentSerializer(student)
            return serializer.data
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif request.method == 'POST':
        try:
            student = StudentSerializer(data=request.data)
            if student.is_valid():
                student.save()
            return student.data
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif request.method == 'PATCH':
        # To edit existng student
        pass