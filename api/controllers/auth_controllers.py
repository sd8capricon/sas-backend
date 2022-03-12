import os
import hashlib

from api.models import Teacher
from api.jwtUtil import signJWT, decodeJWT

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

def verifyToken(request):
    if request.method == 'POST':
        decode = decodeJWT(request)
        return decode