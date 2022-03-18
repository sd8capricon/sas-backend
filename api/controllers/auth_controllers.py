import os, hashlib

from api.models import Teacher
from api.jwtUtil import signJWT, decodeJWT


# Login Route
def login(req):
    if req.method == 'POST':
        data = req.data
        try:
            teacher = Teacher.objects.get(username = data['username'])
            try:
                course_taught_id = teacher.course.course_id
            except Teacher.course.RelatedObjectDoesNotExist as e:
                course_taught_id = None
            print(course_taught_id)
            password = (os.environ.get('PASS_SALT')+data['password']).encode('utf-8')
            h = hashlib.sha256(password).hexdigest()
            if (teacher.password == h):
                token = signJWT(teacher.teacher_id)
                token['course_taught'] = course_taught_id
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