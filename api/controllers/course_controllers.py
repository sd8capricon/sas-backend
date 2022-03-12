from django.db.models import Sum

from api.serializers import StatSerializer
from api.models import Course, Lec_Stat

def course_lec_stats(request, course_id):
    if request.method == 'GET':
        try:
            c = Course.objects.get(pk=course_id)
            lecs = Lec_Stat.objects.filter(course=c)
            lecCount = lecs.count()
            if lecCount!=0:
                atten_sum = Lec_Stat.objects.all().aggregate(sum=Sum('attendance_percentage'))
                avg_percentage_attendace = atten_sum['sum']/lecCount
                statSerializer = StatSerializer(lecs, many=True)
                statcpy = statSerializer.data
                for stat in statcpy:
                    stat.pop('course')
                res = {
                    'course_stats': statcpy,
                    'avg_course_attendance': avg_percentage_attendace
                }
                return res
            else:
                return {'error': 'No lectures found'}
        except Exception as e:
            error = {'error': str(e)}
            return error