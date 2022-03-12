import os, hashlib

from api.models import Teacher
from api.jwtUtil import signJWT, decodeJWT


# Login Route
def login(request):
    if request.method == 'POST':
        data = request.data
        try:
            teacher = Teacher.objects.get(username = data['username'])
            password = (os.environ.get('PASS_SALT')+data['password']).encode('utf-8')
            h = hashlib.sha256(password).hexdigest()
            if (teacher.password == h):
                token = signJWT(teacher.teacher_id)
                return token
            else:
                return {'error': 'Incorrect Username or Password'}
        except Exception as e:
            error = {'error': str(e)}
            return error

# To verify token
def verifyToken(request):
    if request.method == 'POST':
        decode = decodeJWT(request)
        return decode