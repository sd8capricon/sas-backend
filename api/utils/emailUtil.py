import os

from django.core.mail import send_mail

from api.models import Student

def email_util(req):
    if req.method == 'POST':
        try:
            reqBody = req.data
            defaultors = Student.objects.filter(total_attendance_percentage__lt=70)
            mailingList = []
            for defaultor in defaultors:
                mailingList.append(defaultor.email)
            send_mail(
                reqBody['title'],
                reqBody['body'],
                os.environ.get('EMAIL_HOST_USER'),
                mailingList,
                fail_silently=False,
            )
            return {'message': 'success'}
        except Exception as e:
            error = {'error': str(e)}
            return error