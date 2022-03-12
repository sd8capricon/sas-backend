from datetime import datetime, timedelta
import jwt
from pytz import timezone
secret = 'Pr0ject@2022'

def signJWT(teacher_id):
    payload = {
        'id': teacher_id,
        'iat': datetime.now(tz=timezone("Asia/Kolkata")),
        'exp': datetime.now(tz=timezone("Asia/Kolkata")) + timedelta(days=1)
    }
    token = jwt.encode(payload, secret, algorithm='HS256')
    return {
        'isValid': True,
        'token':token
    }

def decodeJWT(request):
    authHeader = request.headers['Authorization']
    token = authHeader.split(' ')[1]
    try:
        decode = jwt.decode(token, secret, algorithms=['HS256'])
        return {
            'isValid': True,
            'decode': decode
        }
    except jwt.ExpiredSignatureError:
        return {
            'isValid': False,
            'error': 'Token has expired'
        }
    except Exception as e:
        return {
            'isValid': False,
            'error': e
        }