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
        fields = ['student', 'subfield', 'entry_year', 'admission_type',
                  'total_credits_taken', 'total_credits_passed', 'average']


class CreditDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credit
        fields = ['practical_units', 'theoritical_units']


class FieldCourseSerializer(serializers.ModelSerializer):
    credit_detail = CreditDetailSerializer(required=True)

    class Meta:
        model = FieldCourse
        fields = ['serial_number', 'title', 'credit', 'credit_detail']


class CourseSummarySerializer(serializers.ModelSerializer):
    field_course = FieldCourseSerializer(required=True)

    class Meta:
        model = Course
        fields = ['section_number', 'grades_status',
                  'grades_average', 'min_grade', 'max_grade', 'field_course']


class AttendSerializer(serializers.ModelSerializer):
    course = CourseSummarySerializer(required=True)

    class Meta:
        model = Attend
        fields = ['course_type_for_carrier', 'grade', 'grade_status',
                  'carrier_course_removal_status', 'carrier_course_status', 'course']


class TermDetailSerializer(serializers.ModelSerializer):
    start_date = serializers.StringRelatedField()
    end_date = serializers.StringRelatedField()

    class Meta:
        model = Term
        fields = ['pk', 'title', 'start_date', 'end_date']


class TermSummarySerializer(serializers.Serializer):
    total_credits_taken = serializers.IntegerField()
    total_credits_passed = serializers.IntegerField()
    carrier_average = serializers.FloatField()
    field_average = serializers.FloatField()
    department_average = serializers.FloatField()
    college_average = serializers.FloatField()


class PreRegistrationSerializer(serializers.ModelSerializer):
    field_course = FieldCourseSerializer(required=True)

    class Meta:
        model = PreliminaryRegistration
        fields = ['field_course']


class DayRangeSerializer(serializers.ModelSerializer):
    start = serializers.StringRelatedField()
    end = serializers.StringRelatedField()

    class Meta:
        model = DayRange
        fields = ['start', 'end']

class ExamDateSerializer(serializers.ModelSerializer):
    day_range = DayRangeSerializer()
    day = serializers.StringRelatedField()

    class Meta:
        model = ExamDate
        fields = ['day_range', 'day']


class CourseInformationSerializer(serializers.ModelSerializer):
    field_course = FieldCourseSerializer(required=True)
    term = serializers.StringRelatedField()
    room = serializers.StringRelatedField()
    midterm_exam_date = ExamDateSerializer()
    final_exam_date = ExamDateSerializer()

    class Meta:
        model = Course
        fields = ['field_course', 'professors_list', 'section_number',
                  'term', 'midterm_exam_date', 'final_exam_date', 'grades_status',
                  'room', 'class_times', 'number_of_students_registered', 'capacity',
                  'genders_allowed', 'subfields_allowed_to_register', 'departments_allowed_to_register']