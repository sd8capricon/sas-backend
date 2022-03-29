import os, hashlib

from api.models import Teacher
from api.utils.jwtUtil import signJWT, decodeJWT
from api.serializers import TeacherViewSerializer


# Login Route
def login(req):
    if req.method == 'POST':
        data = req.data
        try:
            teacher = Teacher.objects.get(username = data['username'])
            print(data['password'])
            password = (os.environ.get('PASS_SALT')+data['password']).encode('utf-8')
            h = hashlib.sha256(password).hexdigest()
            print(h)
            print(teacher.password)
            if (teacher.password == h):
                token = signJWT(teacher.teacher_id)
                token['teacher'] = TeacherViewSerializer(teacher).data
                try:
                    token['teacher']['course_name'] = teacher.course.course_name
                    token['teacher']['course_id'] = teacher.course.course_id
                except Teacher.course.RelatedObjectDoesNotExist as e:
                    token['teacher']['course_name'] = None
                    token['teacher']['course_id'] = None
                return token
            else:
                return {'error': 'Incorrect Username or Password'}
        except Exception as e:
            error = {'error': str(e)}
            return error

# To verify token
def verifyToken(req):
    if req.method == 'POST':
        decode = decodeJWT(req)
        return decode