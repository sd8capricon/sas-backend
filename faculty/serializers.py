from pyexpat import model
from rest_framework import serializers
from faculty.models import Faculty


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['user_id', 'f_name', 'l_name',
                  'username', 'password', 'email', 'type']


class FacultyDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['user_id', 'f_name', 'l_name',
                  'username', 'email', 'type']
