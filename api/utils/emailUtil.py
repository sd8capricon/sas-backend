import os

from django.core.mail import send_mail

from api.models import Student

def email_defaultors(req):
    if req.method == 'POST':
        try:
            defaultors = Student.objects.filter(total_attendance_percentage__lt=70)
            mailingList = []
            for defaultor in defaultors:
                mailingList.append(defaultor.email)
            send_mail(
                'Defaultor',
                'You are recieving this mail for being a defaultor',
                os.environ.get('EMAIL_HOST_USER'),
                mailingList,
                fail_silently=False,
            )
            return {'message': 'success'}
        except Exception as e:
            error = {'error': str(e)}
            return error