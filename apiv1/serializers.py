from rest_framework import serializers
from users.models import *

class StudentDetailSerializer(serializers.ModelSerializer):
    pic = serializers.StringRelatedField()
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'pic']

class SubfieldDetailSerializer(serializers.ModelSerializer):
    field = serializers.StringRelatedField()
    class Meta:
        model = Subfield
        fields = ['title', 'field']

class CarrierDetailSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer(required=True)
    subfield = SubfieldDetailSerializer(required=True)

    class Meta:
        model = Carrier
        fields = ['student', 'subfield', 'entry_year', 'admission_type']

